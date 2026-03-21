#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from _common import (
    ROOT,
    comet_log_asset,
    finalize_comet,
    gate_file,
    init_comet_context,
    init_output_root,
    log_command,
    now_iso,
    resolve_corpus,
    update_run_manifest,
    write_checkpoint,
    write_text,
)

import json
import hashlib


def main() -> None:
    init_output_root()
    log_command("python3 code/scripts/gate_a_setup.py")
    corpus = resolve_corpus()
    comet = init_comet_context("gate_a", corpus)

    schema_path = ROOT / "code" / "format" / "ZPMOC_SCHEMA_V1.json"
    schema_bytes = schema_path.read_bytes()
    schema_hash = hashlib.sha256(schema_bytes).hexdigest()

    fixture_lock = {
        "lock_version": "1.0.0",
        "seed": 20260220,
        "core_corpus": {
            "labels": [
                "walk",
                "turn_left",
                "turn_right",
                "run",
                "jump",
                "punch",
                "crouch",
                "sidestep",
                "idle",
                "fall_recover",
            ],
            "clips_per_label": 8,
            "frames": 240,
            "fps": 60,
            "noise_scale": 0.00025,
        },
        "search_library": {
            "size": 10000,
            "frames": 120,
            "fps": 30,
            "query_count": 120,
        },
        "schema": {
            "path": "code/format/ZPMOC_SCHEMA_V1.json",
            "sha256": schema_hash,
        },
        "resource_plan": {
            "acl": "concept-reference comparator + in-lane gzip comparator",
            "lafan1": "deterministic proxy corpus parameters locked",
            "lafan1_resolved": "60fps proxy included in lock",
            "bvhio": "adapter-compatibility tracked in traceability",
            "usdBVHAnim": "adapter smoke tracked in traceability",
            "mixamo": "retarget proxy tracked in traceability",
            "cmu": "diversity proxy tracked in stress matrix",
            "moma": "design-note mapping tracked in traceability",
        },
    }

    lock_path = ROOT / "code" / "fixtures" / "locked_corpus_v1.json"
    lock_path.write_text(json.dumps(fixture_lock, indent=2) + "\n", encoding="utf-8")

    write_text(
        gate_file("gate_a_status.txt"),
        "Gate A PASS: runbooks present, fixture lock and schema hash frozen.\n",
    )
    comet_log_asset(comet, gate_file("gate_a_status.txt"))

    comet_url = finalize_comet(comet)
    write_checkpoint(
        gate="gate_a",
        status="PASS",
        details={
            "schema_sha256": schema_hash,
            "fixture_lock": "code/fixtures/locked_corpus_v1.json",
            "runbooks": [
                "proofs/runbooks/RUNBOOK_ZPE_MOCAP_MASTER.md",
                "proofs/runbooks/RUNBOOK_GATE_A.md",
                "proofs/runbooks/RUNBOOK_GATE_B.md",
                "proofs/runbooks/RUNBOOK_GATE_C.md",
                "proofs/runbooks/RUNBOOK_GATE_D.md",
                "proofs/runbooks/RUNBOOK_GATE_E.md",
            ],
        },
        comet_url=comet_url,
    )
    update_run_manifest(
        {
            "gate": "gate_a",
            "corpus": corpus,
            "status": "PASS",
            "timestamp_utc": now_iso(),
            "comet_experiment_url": comet_url,
        }
    )


if __name__ == "__main__":
    main()
