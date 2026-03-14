#!/usr/bin/env python3
"""
persona-vault publish.py
Encrypts and bundles persona files into a single encrypted bundle.
"""

import argparse
import gzip
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from argon2.low_level import hash_secret_raw, Type
except ImportError:
    print("Error: argon2-cffi is required. Install with: pip install argon2-cffi")
    sys.exit(1)

try:
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
except ImportError:
    print("Error: pycryptodome is required. Install with: pip install pycryptodome")
    sys.exit(1)


EXCLUDED_DIRS = {".git", "archive", "proposals", ".claude", "__pycache__", "node_modules", "venv"}
EXCLUDED_FILES = {".env", ".gitkeep", ".DS_Store", "Thumbs.db"}
EXCLUDED_EXTENSIONS = {".key", ".pem", ".p12", ".pfx", ".log", ".pyc", ".tmp"}
VERSION_BYTE = 0x01
SALT_LEN = 16
IV_LEN = 12
TAG_LEN = 16
KDF_TIME_COST = 3
KDF_MEMORY_COST = 65536
KDF_PARALLELISM = 4
KEY_LEN = 32


def collect_files(source_dir: Path) -> list[dict]:
    """Recursively collect all files from source_dir, excluding certain directories."""
    files = []
    for root, dirs, filenames in os.walk(source_dir):
        # Filter out excluded directories in-place
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]

        for filename in sorted(filenames):
            if filename in EXCLUDED_FILES:
                continue
            if Path(filename).suffix.lower() in EXCLUDED_EXTENSIONS:
                continue
            filepath = Path(root) / filename
            rel_path = filepath.relative_to(source_dir).as_posix()
            try:
                content = filepath.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError) as e:
                print(f"  Skipping {rel_path}: {e}")
                continue
            files.append({"path": rel_path, "content": content})

    return files


def derive_key(secret: str, salt: bytes) -> bytes:
    """Derive a 256-bit key from the secret using Argon2id."""
    return hash_secret_raw(
        secret=secret.encode("utf-8"),
        salt=salt,
        time_cost=KDF_TIME_COST,
        memory_cost=KDF_MEMORY_COST,
        parallelism=KDF_PARALLELISM,
        hash_len=KEY_LEN,
        type=Type.ID,
    )


def encrypt_bundle(plaintext: bytes, secret: str) -> tuple[bytes, bytes]:
    """
    Encrypt plaintext with AES-256-GCM.
    Returns (encrypted_bundle, salt) where encrypted_bundle is:
    [1 byte version=0x01][16 bytes salt][12 bytes iv][N bytes ciphertext][16 bytes GCM tag]
    """
    salt = get_random_bytes(SALT_LEN)
    iv = get_random_bytes(IV_LEN)
    key = derive_key(secret, salt)

    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)

    bundle = bytes([VERSION_BYTE]) + salt + iv + ciphertext + tag
    return bundle, salt


def main():
    parser = argparse.ArgumentParser(description="Encrypt and bundle persona files.")
    parser.add_argument(
        "--source",
        type=str,
        default=r"C:\Users\GUANZHENGHENG\persona",
        help="Path to the persona source directory",
    )
    parser.add_argument(
        "--key",
        type=str,
        default=None,
        help="Encryption secret key (will prompt if not provided)",
    )
    args = parser.parse_args()

    source_dir = Path(args.source).resolve()
    if not source_dir.is_dir():
        print(f"Error: Source directory not found: {source_dir}")
        sys.exit(1)

    # Get the secret key
    secret = args.key
    if not secret:
        import getpass
        secret = getpass.getpass("Enter encryption secret key: ")
        if not secret:
            print("Error: Secret key cannot be empty.")
            sys.exit(1)

    # Collect files
    print(f"Scanning {source_dir} ...")
    files = collect_files(source_dir)
    if not files:
        print("Error: No files found to bundle.")
        sys.exit(1)
    print(f"  Found {len(files)} files.")

    # Build JSON bundle
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    bundle_data = {
        "files": files,
        "version": now,
        "file_count": len(files),
    }
    bundle_json = json.dumps(bundle_data, ensure_ascii=False, indent=2)

    # Compress
    compressed = gzip.compress(bundle_json.encode("utf-8"))
    print(f"  Compressed: {len(bundle_json)} -> {len(compressed)} bytes")

    # Encrypt
    print("  Deriving key with Argon2id (this may take a moment) ...")
    encrypted_bundle, salt = encrypt_bundle(compressed, secret)
    print(f"  Encrypted bundle size: {len(encrypted_bundle)} bytes")

    # Write output files
    output_dir = Path(__file__).resolve().parent / "docs"
    output_dir.mkdir(parents=True, exist_ok=True)

    bundle_path = output_dir / "bundle.enc"
    bundle_path.write_bytes(encrypted_bundle)
    print(f"  Written: {bundle_path}")

    # Write manifest
    manifest = {
        "version": now,
        "file_count": len(files),
        "bundle_size": len(encrypted_bundle),
        "encryption": {
            "algorithm": "AES-256-GCM",
            "kdf": "argon2id",
            "kdf_params": {
                "time_cost": KDF_TIME_COST,
                "memory_cost": KDF_MEMORY_COST,
                "parallelism": KDF_PARALLELISM,
            },
            "version": 1,
        },
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"  Written: {manifest_path}")
    print("Done.")


if __name__ == "__main__":
    main()
