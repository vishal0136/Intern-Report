"""Week 4: authenticated encryption demo. Do not hard-code real keys in production."""
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# AES-GCM provides confidentiality and integrity/authenticity when used correctly.
key = AESGCM.generate_key(bit_length=256)
aesgcm = AESGCM(key)
nonce = os.urandom(12)  # A nonce must never be reused with the same key.
plaintext = b"batch_id=B-1001;quality_status=approved"
associated_data = b"food-processing-demo:v1"
ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
recovered = aesgcm.decrypt(nonce, ciphertext, associated_data)

assert recovered == plaintext
print("Round-trip encryption/decryption passed.")
print("Plaintext bytes:", len(plaintext))
print("Ciphertext + authentication tag bytes:", len(ciphertext))
# Production requirements: protect/rotate keys in KMS/HSM or a secret manager;
# never log keys or plaintext; define access, rotation, backup, and recovery procedures.
