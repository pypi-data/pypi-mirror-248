"""Secrets Utils
"""
import secrets


def create_application_secret(nb_bytes: int = 32):
    """
    Creates a new application secret.
    """
    return secrets.token_hex(nbytes=nb_bytes)
