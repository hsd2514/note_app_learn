"""Test configuration helpers."""

import sys
from pathlib import Path


# Ensure the project root is on sys.path so tests can import `main`.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

