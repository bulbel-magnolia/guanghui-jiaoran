"""Compute Round 1 feedback from validation data and versioned rules."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

AI_ROOT = Path(__file__).resolve().parents[1]
if str(AI_ROOT) not in sys.path:
    sys.path.insert(0, str(AI_ROOT))

from fabric_ai.metabolic import compute_feedback_update, validate_closed_loop


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-dir", required=True, type=Path)
    parser.add_argument("--rules", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    evidence = args.evidence_dir.resolve()
    frame = compute_feedback_update(evidence, args.rules)
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output, index=False)
    if output.parent == evidence and output.name == "post_feedback_evidence.csv":
        validate_closed_loop(evidence)
    print(f"Computed {len(frame)} feedback evidence rows at {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())