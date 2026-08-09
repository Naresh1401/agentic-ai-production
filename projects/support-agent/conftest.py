"""Makes the `app` package importable under `pytest projects/support-agent/`."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
