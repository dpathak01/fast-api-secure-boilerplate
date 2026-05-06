#!/usr/bin/env python3
"""
Generate secure random keys for production use.

Usage:
    python scripts/generate_keys.py
"""

import secrets
import sys
from pathlib import Path


def generate_jwt_secret():
    """Generate a secure JWT secret key."""
    return secrets.token_urlsafe(32)


def generate_database_password():
    """Generate a secure database password."""
    return secrets.token_urlsafe(24)


def main():
    """Generate and display security keys."""
    print("=" * 50)
    print("Security Keys Generator")
    print("=" * 50)
    print()
    
    # JWT Secret
    jwt_secret = generate_jwt_secret()
    print("JWT Secret Key:")
    print(f"  {jwt_secret}")
    print()
    
    # Database Password
    db_password = generate_database_password()
    print("Database Password:")
    print(f"  {db_password}")
    print()
    
    print("=" * 50)
    print("Add these to your .env.prod file:")
    print("=" * 50)
    print(f"JWT_SECRET_KEY={jwt_secret}")
    print(f"# If using MongoDB Atlas with new user:")
    print(f"# Create user with password: {db_password}")
    print()


if __name__ == "__main__":
    main()
