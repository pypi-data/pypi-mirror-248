import logging
import storeservices
import os
import hashlib
import uuid

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('storeservices').setLevel(logging.DEBUG)

adi_proxy = storeservices.StoreServicesCoreADIProxy(
    "/workspaces/apple-private-apis/applemusic", "/workspaces/apple-private-apis/applemusic/adi-data")

print(dir(adi_proxy))
# Create random device ID (16 bytes) using Python's os.urandom()
device_id = os.urandom(16)

# result = adi_proxy.get_serial_number()
# 
# let mut local_user_uuid_hasher = Sha256::new();
# local_user_uuid_hasher.update(identifier);

local_user_uuid_hasher = hashlib.sha256()
local_user_uuid_hasher.update(device_id)

# result = adi_proxy.is_machine_provisioned(-2)
# print(uuid.UUID(bytes=device_id).hex.upper())
result = adi_proxy.set_provisioning_path(
    "/workspaces/apple-private-apis/applemusic/adi-data"
)

print(result == 0)

result = adi_proxy.set_device_identifier(
    uuid.UUID(bytes=device_id).hex.upper()
)

print(result == 0)

result = adi_proxy.set_local_user_uuid(
    local_user_uuid_hasher.hexdigest().upper()
)

print(result == 0)


# adi_proxy.set_device_identifier(
#     uuid::Uuid::from_bytes(identifier)
#         .to_string()
#         .to_uppercase(),
# )?; // UUID, uppercase
# adi_proxy
    # .set_local_user_uuid(hex::encode(local_user_uuid_hasher.finalize()).to_uppercase()); // 64 uppercase character hex

# 
otp = adi_proxy.request_otp(-2)
print(otp)
