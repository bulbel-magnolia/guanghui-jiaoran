"""Path adapter for the byte-identical frozen ranking tests."""
import runpy
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[2] / "src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py"
build_ranking = runpy.run_path(str(SOURCE))["build_ranking"]
