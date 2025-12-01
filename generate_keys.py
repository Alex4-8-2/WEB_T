from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Generar clave privada
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Obtener clave privada en formato PEM
priv = key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

# Obtener clave pública en formato PEM
pub = key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Guardar claves
with open("D:\\WEB_T\\LOGIN\\secrets\\private_key.pem", "wb") as f:
    f.write(priv)

with open("D:\\WEB_T\\LOGIN\\secrets\\public_key.pem", "wb") as f:
    f.write(pub)

print("Keys generated successfully!")