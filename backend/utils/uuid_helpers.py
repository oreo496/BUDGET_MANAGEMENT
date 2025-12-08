"""
Utility functions for UUID handling with binary storage.
"""
import uuid


def uuid_to_binary(uuid_string):
    """Convert UUID string to binary format."""
    return uuid.UUID(uuid_string).bytes


def binary_to_uuid(binary_data):
    """Convert binary data to UUID string."""
    return str(uuid.UUID(bytes=binary_data))


def generate_uuid_binary():
    """Generate a new UUID and return as binary."""
    return uuid.uuid4().bytes

