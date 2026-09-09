"""Adapter for unchanged historical synthetic ordering fixtures.

The nine frozen fixtures test the original sorting kernel and intentionally do
not supply production provenance (some ratios are arbitrary sorting keys).
Public build_ranking validation is exercised separately on real frozen inputs.
"""
import runpy
from pathlib import Path
SOURCE = Path(__file__).resolve().parents[2] / "src/ai/fabric_ai_optimizer/fabric_ai_benchmark.py"
build_ranking = runpy.run_path(str(SOURCE))["_rank_validated_frames"]
