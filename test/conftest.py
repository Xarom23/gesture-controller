"""Pytest configuration file for test suite."""
import sys
from pathlib import Path

# Add parent directory to sys.path to allow importing modules
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))
