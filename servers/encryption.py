"""
Utilidades de encriptación para credenciales SSH
"""
from cryptography.fernet import Fernet
from django.conf import settings
import base64
import hashlib


def get_encryption_key():
    """
    Obtiene o genera la clave de encriptación desde settings
    """
    if hasattr(settings, 'ENCRYPTION_KEY') and settings.ENCRYPTION_KEY:
        return settings.ENCRYPTION_KEY.encode()
    
    # Si no existe, generar una clave basada en SECRET_KEY (no recomendado para producción)
    key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
    return base64.urlsafe_b64encode(key)


def encrypt_password(plain_password):
    """
    Encripta una contraseña usando Fernet
    
    Args:
        plain_password (str): Contraseña en texto plano
        
    Returns:
        str: Contraseña encriptada
    """
    if not plain_password:
        return ''
    
    key = get_encryption_key()
    f = Fernet(key)
    encrypted = f.encrypt(plain_password.encode())
    return encrypted.decode()


def decrypt_password(encrypted_password):
    """
    Desencripta una contraseña
    
    Args:
        encrypted_password (str): Contraseña encriptada
        
    Returns:
        str: Contraseña en texto plano
    """
    if not encrypted_password:
        return ''
    
    try:
        key = get_encryption_key()
        f = Fernet(key)
        decrypted = f.decrypt(encrypted_password.encode())
        return decrypted.decode()
    except Exception as e:
        # Si falla la desencriptación, puede ser que la contraseña no esté encriptada
        # o que la clave haya cambiado
        return encrypted_password
