import hashlib

text = "JohnMic11G41"
hash_object = hashlib.sha256(text.encode())
sha256_hash = hash_object.hexdigest()

print("SHA-256:", sha256_hash)
