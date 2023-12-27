use log::*;
use pyo3::prelude::*;

#[cfg(target_os = "macos")]
mod posix_macos;
#[cfg(target_family = "windows")]
mod posix_windows;

#[derive(Debug)]
pub struct ServerError {
    pub code: i64,
    pub description: String,
}

#[derive(Debug)]
pub enum ProvisioningError {
    InvalidResponse,
    ServerError(ServerError),
}

#[derive(Debug)]
pub enum ADIError {
    Unknown(i32),
    ProvisioningError(ProvisioningError),
}

impl ADIError {
    pub fn resolve(error_number: i32) -> ADIError {
        ADIError::Unknown(error_number)
    }
}

use android_loader::android_library::AndroidLibrary;
use android_loader::sysv64_type;
use android_loader::{hook_manager, sysv64};
use anyhow::Result;
use std::collections::HashMap;
use std::ffi::{c_char, CString};
use std::path::PathBuf;

#[pyclass]
pub struct SynchronizeData {
    pub mid: Vec<u8>,
    pub srm: Vec<u8>,
}
#[pyclass]
pub struct StartProvisioningData {
    pub cpim: Vec<u8>,
    pub session: u32,
}

#[pyclass]
pub struct RequestOTPData {
    pub otp: Vec<u8>,
    pub mid: Vec<u8>,
}

#[pyclass]
pub struct StoreServicesCoreADIProxy {
    #[allow(dead_code)]
    store_services_core: AndroidLibrary<'static>,

    local_user_uuid: String,
    device_identifier: String,

    adi_set_android_id: sysv64_type!(fn(id: *const u8, length: u32) -> i32),
    adi_set_provisioning_path: sysv64_type!(fn(path: *const u8) -> i32),

    adi_provisioning_erase: sysv64_type!(fn(ds_id: i64) -> i32),
    adi_synchronize: sysv64_type!(
        fn(
            ds_id: i64,
            sim: *const u8,
            sim_length: u32,
            out_mid: *mut *const u8,
            out_mid_length: *mut u32,
            out_srm: *mut *const u8,
            out_srm_length: *mut u32,
        ) -> i32
    ),
    adi_provisioning_destroy: sysv64_type!(fn(session: u32) -> i32),
    adi_provisioning_end: sysv64_type!(
        fn(session: u32, ptm: *const u8, ptm_length: u32, tk: *const u8, tk_length: u32) -> i32
    ),
    adi_provisioning_start: sysv64_type!(
        fn(
            ds_id: i64,
            spim: *const u8,
            spim_length: u32,
            out_cpim: *mut *const u8,
            out_cpim_length: *mut u32,
            out_session: *mut u32,
        ) -> i32
    ),
    adi_get_login_code: sysv64_type!(fn(ds_id: i64) -> i32),
    adi_dispose: sysv64_type!(fn(ptr: *const u8) -> i32),
    adi_otp_request: sysv64_type!(
        fn(
            ds_id: i64,
            out_mid: *mut *const u8,
            out_mid_size: *mut u32,
            out_otp: *mut *const u8,
            out_otp_size: *mut u32,
        ) -> i32
    ),
}

#[pymethods]
impl StoreServicesCoreADIProxy {
    #[new]
    pub fn new(library_path: String, provisioning_path: String) -> PyResult<Self> {
        Self::with_custom_provisioning_path(library_path, provisioning_path)
    }

    #[staticmethod]
    pub fn with_custom_provisioning_path(
        library_path: String,
        provisioning_path: String,
    ) -> Result<Self, PyErr> {
        let lib_path = PathBuf::from(library_path);
        let prov_path = PathBuf::from(provisioning_path);

        info!(
            "Initializing StoreServicesCoreADIProxy with library path {} and provisioning path {}",
            lib_path.to_str().unwrap(),
            prov_path.to_str().unwrap(),
        );

        // Should be safe if the library is correct.
        unsafe {
            LoaderHelpers::setup_hooks();

            if !lib_path.exists() {
                warn!(
                    "Library path {} does not exist, creating it",
                    lib_path.to_str().unwrap()
                );

                std::fs::create_dir_all(&lib_path)
                    .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("{}", e)))?;
            }

            if !prov_path.exists() {
                warn!(
                    "Provisioning path {} does not exist, creating it",
                    prov_path.to_str().unwrap()
                );

                std::fs::create_dir_all(&lib_path)
                    .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("{}", e)))?;
            }

            let library_path = lib_path
                .canonicalize()
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("{}", e)))?;

            #[cfg(target_arch = "x86_64")]
            const ARCH: &str = "x86_64";
            #[cfg(target_arch = "x86")]
            const ARCH: &str = "x86";
            #[cfg(target_arch = "arm")]
            const ARCH: &str = "armeabi-v7a";
            #[cfg(target_arch = "aarch64")]
            const ARCH: &str = "arm64-v8a";

            let native_library_path = library_path.join("lib").join(ARCH);

            let path = native_library_path.join("libstoreservicescore.so");
            let path_str = path.to_str().ok_or_else(|| {
                PyErr::new::<pyo3::exceptions::PyValueError, _>("Path conversion failed")
            })?;

            let store_services_core = AndroidLibrary::load(path_str).map_err(|_e| {
                PyErr::new::<pyo3::exceptions::PyIOError, _>(format!(
                    "Failed to load Android Library for arch {} on path {}",
                    ARCH, path_str
                ))
            })?;

            let adi_load_library_with_path: sysv64_type!(fn(path: *const u8) -> i32) =
                std::mem::transmute(store_services_core.get_symbol("kq56gsgHG6").ok_or(
                    PyErr::new::<pyo3::exceptions::PyValueError, _>(
                        "Failed to get symbol kq56gsgHG6",
                    ),
                )?);

            let adi_set_provisioning_path: sysv64_type!(fn(path: *const u8) -> i32) =
                std::mem::transmute(store_services_core.get_symbol("nf92ngaK92").ok_or(
                    PyErr::new::<pyo3::exceptions::PyValueError, _>(
                        "Failed to get symbol nf92ngaK92",
                    ),
                )?);

            let native_lib_path =
                CString::new(native_library_path.to_str().ok_or(PyErr::new::<
                    pyo3::exceptions::PyValueError,
                    _,
                >(
                    "Failed to convert path to string",
                ))?)
                .unwrap();

            let prov_lib_path = CString::new(prov_path.to_str().ok_or(PyErr::new::<
                pyo3::exceptions::PyValueError,
                _,
            >(
                "Failed to convert path to string",
            ))?)
            .unwrap();

            assert_eq!(
                (adi_load_library_with_path)(native_lib_path.as_ptr() as *const u8),
                0
            );

            assert_eq!(
                (adi_set_provisioning_path)(prov_lib_path.as_ptr() as *const u8),
                0
            );

            let adi_set_android_id =
                store_services_core
                    .get_symbol("Sph98paBcz")
                    .ok_or(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                        "Failed to get symbol Sph98paBcz",
                    ))?;

            let adi_provisioning_erase =
                store_services_core
                    .get_symbol("p435tmhbla")
                    .ok_or(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                        "Failed to get symbol p435tmhbla",
                    ))?;

            let adi_synchronize =
                store_services_core
                    .get_symbol("tn46gtiuhw")
                    .ok_or(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                        "Failed to get symbol tn46gtiuhw",
                    ))?;

            let adi_provisioning_destroy =
                store_services_core
                    .get_symbol("fy34trz2st")
                    .ok_or(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                        "Failed to get symbol fy34trz2st",
                    ))?;

            let adi_provisioning_end =
                store_services_core
                    .get_symbol("uv5t6nhkui")
                    .ok_or(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                        "Failed to get symbol uv5t6nhkui",
                    ))?;

            let adi_provisioning_start =
                store_services_core
                    .get_symbol("rsegvyrt87")
                    .ok_or(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                        "Failed to get symbol rsegvyrt87",
                    ))?;

            let adi_get_login_code =
                store_services_core
                    .get_symbol("aslgmuibau")
                    .ok_or(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                        "Failed to get symbol aslgmuibau",
                    ))?;

            let adi_dispose = store_services_core
                .get_symbol("jk24uiwqrg")
                .ok_or(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                    "Failed to get symbol jk24uiwqrg",
                ))?;

            let adi_otp_request =
                store_services_core
                    .get_symbol("qi864985u0")
                    .ok_or(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                        "Failed to get symbol qi864985u0",
                    ))?;

            let proxy = StoreServicesCoreADIProxy {
                store_services_core,

                local_user_uuid: String::new(),
                device_identifier: String::new(),

                adi_set_android_id: std::mem::transmute(adi_set_android_id),
                adi_set_provisioning_path: std::mem::transmute(adi_set_provisioning_path),

                adi_provisioning_erase: std::mem::transmute(adi_provisioning_erase),
                adi_synchronize: std::mem::transmute(adi_synchronize),
                adi_provisioning_destroy: std::mem::transmute(adi_provisioning_destroy),
                adi_provisioning_end: std::mem::transmute(adi_provisioning_end),
                adi_provisioning_start: std::mem::transmute(adi_provisioning_start),
                adi_get_login_code: std::mem::transmute(adi_get_login_code),
                adi_dispose: std::mem::transmute(adi_dispose),
                adi_otp_request: std::mem::transmute(adi_otp_request),
            };

            Ok(proxy)
        }
    }

    fn erase_provisioning(&mut self, ds_id: i64) -> PyResult<()> {
        let result = (self.adi_provisioning_erase)(ds_id);
        if result == 0 {
            Ok(())
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
                "Failed to erase provisioning: {}",
                result
            )))
        }
    }

    fn synchronize(&mut self, ds_id: i64, sim: &[u8]) -> PyResult<SynchronizeData> {
        unsafe {
            let sim_size = sim.len() as u32;
            let sim_ptr = sim.as_ptr();

            let mut mid_size: u32 = 0;
            let mut mid_ptr: *const u8 = std::ptr::null();
            let mut srm_size: u32 = 0;
            let mut srm_ptr: *const u8 = std::ptr::null();

            let result = (self.adi_synchronize)(
                ds_id,
                sim_ptr,
                sim_size,
                &mut mid_ptr,
                &mut mid_size,
                &mut srm_ptr,
                &mut srm_size,
            );

            match result {
                0 => {
                    let mut mid = vec![0; mid_size as usize];
                    let mut srm = vec![0; srm_size as usize];

                    mid.copy_from_slice(std::slice::from_raw_parts(mid_ptr, mid_size as usize));
                    srm.copy_from_slice(std::slice::from_raw_parts(srm_ptr, srm_size as usize));

                    (self.adi_dispose)(mid_ptr);
                    (self.adi_dispose)(srm_ptr);

                    Ok(SynchronizeData { mid, srm })
                }
                err => Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
                    "{:#?}",
                    err
                ))),
            }
        }
    }

    fn destroy_provisioning_session(&mut self, session: u32) -> PyResult<()> {
        let result = (self.adi_provisioning_destroy)(session);
        if result == 0 {
            Ok(())
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
                "Failed to destroy provisioning session: {}",
                result
            )))
        }
    }

    fn end_provisioning(&mut self, session: u32, ptm: &[u8], tk: &[u8]) -> PyResult<()> {
        let ptm_size = ptm.len() as u32;
        let ptm_ptr = ptm.as_ptr();

        let tk_size = tk.len() as u32;
        let tk_ptr = tk.as_ptr();

        let result = (self.adi_provisioning_end)(session, ptm_ptr, ptm_size, tk_ptr, tk_size);
        if result == 0 {
            Ok(())
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
                "Failed to end provisioning: {}",
                result
            )))
        }
    }

    fn start_provisioning(&mut self, ds_id: i64, spim: &[u8]) -> PyResult<StartProvisioningData> {
        unsafe {
            let spim_size = spim.len() as u32;
            let spim_ptr = spim.as_ptr();

            let mut cpim_size: u32 = 0;
            let mut cpim_ptr: *const u8 = std::ptr::null();

            let mut session: u32 = 0;

            let result = (self.adi_provisioning_start)(
                ds_id,
                spim_ptr,
                spim_size,
                &mut cpim_ptr,
                &mut cpim_size,
                &mut session,
            );

            match result {
                0 => {
                    let mut cpim = vec![0; cpim_size as usize];

                    cpim.copy_from_slice(std::slice::from_raw_parts(cpim_ptr, cpim_size as usize));

                    (self.adi_dispose)(cpim_ptr);

                    Ok(StartProvisioningData { cpim, session })
                }
                err => Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
                    "{:#?}",
                    err
                ))),
            }
        }
    }

    fn is_machine_provisioned(&self, ds_id: i64) -> bool {
        (self.adi_get_login_code)(ds_id) == 0
    }

    fn request_otp(&self, ds_id: i64) -> PyResult<RequestOTPData> {
        unsafe {
            let mut mid_size: u32 = 0;
            let mut mid_ptr: *const u8 = std::ptr::null();
            let mut otp_size: u32 = 0;
            let mut otp_ptr: *const u8 = std::ptr::null();

            let result = (self.adi_otp_request)(
                ds_id,
                &mut mid_ptr,
                &mut mid_size,
                &mut otp_ptr,
                &mut otp_size,
            );

            match result {
                0 => {
                    let mut mid = vec![0; mid_size as usize];
                    let mut otp = vec![0; otp_size as usize];

                    mid.copy_from_slice(std::slice::from_raw_parts(mid_ptr, mid_size as usize));
                    otp.copy_from_slice(std::slice::from_raw_parts(otp_ptr, otp_size as usize));

                    (self.adi_dispose)(mid_ptr);
                    (self.adi_dispose)(otp_ptr);

                    Ok(RequestOTPData { mid, otp })
                }
                err => Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
                    "{:#?}",
                    err
                ))),
            }
        }
    }

    fn set_local_user_uuid(&mut self, local_user_uuid: String) {
        self.local_user_uuid = local_user_uuid;
    }

    fn set_device_identifier(&mut self, device_identifier: String) -> PyResult<()> {
        self.set_identifier(&device_identifier[0..16]);
        self.device_identifier = device_identifier;
        Ok(())
    }

    fn get_local_user_uuid(&self) -> String {
        self.local_user_uuid.clone()
    }

    fn get_device_identifier(&self) -> String {
        self.device_identifier.clone()
    }

    fn get_serial_number(&self) -> String {
        arc4random().to_string()
    }

    fn set_identifier(&mut self, identifier: &str) -> PyResult<()> {
        let result = (self.adi_set_android_id)(identifier.as_ptr(), identifier.len() as u32);

        if result == 0 {
            debug!("Set identifier to {}", identifier);
            Ok(())
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
                "Failed to set identifier: {}",
                result
            )))
        }
    }

    fn set_provisioning_path(&mut self, path: &str) -> PyResult<()> {
        let path = CString::new(path).unwrap();

        let result = (self.adi_set_provisioning_path)(path.as_ptr() as *const u8);

        if result == 0 {
            Ok(())
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
                "Failed to set provisioning path: {}",
                result
            )))
        }
    }
}

#[pyfunction]
fn log_something() {
    info!("Something!");
}

#[pymodule]
fn storeservices(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    pyo3_log::init();

    m.add_class::<StoreServicesCoreADIProxy>()?;
    m.add_wrapped(wrap_pyfunction!(log_something))?;

    // Add other classes or functions to the module
    Ok(())
}
struct LoaderHelpers;

use rand::Rng;

#[cfg(all(target_family = "unix", not(target_os = "macos")))]
use libc::{
    chmod, close, free, fstat, ftruncate, gettimeofday, lstat, malloc, mkdir, open, read, strncpy,
    umask, write,
};
#[cfg(target_os = "macos")]
use posix_macos::*;

static mut ERRNO: i32 = 0;

#[allow(unreachable_code)]
#[sysv64]
unsafe fn __errno_location() -> *mut i32 {
    ERRNO = std::io::Error::last_os_error().raw_os_error().unwrap_or(0);
    &mut ERRNO
}

#[sysv64]
fn arc4random() -> u32 {
    rand::thread_rng().gen()
}

#[sysv64]
unsafe fn __system_property_get(_name: *const c_char, value: *mut c_char) -> i32 {
    *value = '0' as c_char;
    return 1;
}

#[cfg(target_family = "windows")]
use posix_windows::*;

impl LoaderHelpers {
    pub fn setup_hooks() {
        let mut hooks = HashMap::new();
        hooks.insert("arc4random".to_owned(), arc4random as usize);
        hooks.insert("chmod".to_owned(), chmod as usize);
        hooks.insert(
            "__system_property_get".to_owned(),
            __system_property_get as usize,
        );
        hooks.insert("__errno".to_owned(), __errno_location as usize);
        hooks.insert("close".to_owned(), close as usize);
        hooks.insert("free".to_owned(), free as usize);
        hooks.insert("fstat".to_owned(), fstat as usize);
        hooks.insert("ftruncate".to_owned(), ftruncate as usize);
        hooks.insert("gettimeofday".to_owned(), gettimeofday as usize);
        hooks.insert("lstat".to_owned(), lstat as usize);
        hooks.insert("malloc".to_owned(), malloc as usize);
        hooks.insert("mkdir".to_owned(), mkdir as usize);
        hooks.insert("open".to_owned(), open as usize);
        hooks.insert("read".to_owned(), read as usize);
        hooks.insert("strncpy".to_owned(), strncpy as usize);
        hooks.insert("umask".to_owned(), umask as usize);
        hooks.insert("write".to_owned(), write as usize);

        hook_manager::add_hooks(hooks);
    }
}

#[cfg(test)]
mod tests {
    use crate::store_services_core::StoreServicesCoreADIProxy;

    use anyhow::{Ok, Result};
    use log::info;
    use std::path::PathBuf;

    #[test]
    fn setup_test() -> Result<()> {
        let path = String::from("anisette_test");
        let other_path = String::from("anisette_test");

        let ssc_adi_proxy = StoreServicesCoreADIProxy::new(path, other_path).unwrap();

        let result = (ssc_adi_proxy.adi_get_login_code)(-2);

        info!("Result: {}", result);
        Ok(())
        // ssc_adi_proxy.set_device_identifier("test".to_string())?;
    }
}
