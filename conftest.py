"""
Pytest bootstrap: makes `src/constraint_geometry` importable as
`constraint_geometry` without requiring an editable install, so `pytest`
run from the repository root works immediately.
"""

import os
import sys

_SRC = os.path.join(os.path.dirname(__file__), "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)
