from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

# Generar las claves
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

# Serializar la clave privada
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
).decode('utf-8')

# Serializar la clave pública
public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode('utf-8')

print("Clave Pública:")
print(public_key_pem)
print("\nClave Privada:")
print(private_key_pem)