"""Makes the `app` package importable when running `pytest 01-fastapi-deployment/`."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
