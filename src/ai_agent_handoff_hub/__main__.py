"""Entry point for `python -m ai_agent_handoff_hub`."""
from __future__ import annotations

import sys

from .cli import main

if __name__ == "__main__":
      sys.exit(main())
