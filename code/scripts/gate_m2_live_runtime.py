#!/usr/bin/env python3
from __future__ import annotations

from _common import (
    comet_log_asset,
    comet_log_metrics,
    finalize_comet,
    gate_file,
    init_comet_context,
    init_output_root,
    load_env_file,
    log_command,
    now_iso,
    preferred_python,
    read_json,
    resolve_corpus,
    run_command,
    update_run_manifest,
    write_checkpoint,
)
from zpe_mocap.utils import write_json


def main() -> None:
    init_output_root()
    log_command("python3 code/scripts/gate_m2_live_runtime.py")
    corpus = resolve_corpus()
    comet = init_comet_context("gate_m2", corpus)
    env_report = load_env_file()

    evidence = []
    evidence.append(
        run_command(
            ["zsh", "-lc", "set -a; [ -f .env ] && source .env; set +a; echo BOOTSTRAP_OK"],
            timeout_sec=30,
        )
    )

    which_blender = run_command(["which", "blender"], timeout_sec=10)
    evidence.append(which_blender)

    blender_live_ok = False
    blender_note = ""
    if which_blender["exit_code"] == 0 and which_blender["stdout_tail"].strip():
        blender_ver = run_command(["blender", "--background", "--version"], timeout_sec=60)
        evidence.append(blender_ver)
        blender_live_ok = blender_ver["exit_code"] == 0
        blender_note = "blender headless runtime executed" if blender_live_ok else "blender binary found but runtime failed"
    else:
        blender_note = "blender binary not found"

    usd_live_ok = False
    usd_runtime_interpreter = ""
    usd_probe_cmd = (
        "from pxr import Usd,Sdf;"
        "l=Sdf.Layer.CreateAnonymous();"
        "s=Usd.Stage.Open(l.identifier);"
        "print('usd_runtime_ok' if s else 'usd_runtime_fail')"
    )
    for candidate in ("python3", "python3.11", preferred_python()):
        pxr_probe = run_command([candidate, "-c", usd_probe_cmd], timeout_sec=60)
        evidence.append(pxr_probe)
        if pxr_probe.get("exit_code") == 0 and "usd_runtime_ok" in pxr_probe.get("stdout_tail", ""):
            usd_live_ok = True
            usd_runtime_interpreter = candidate
            break

    live_status = "PASS" if (blender_live_ok or usd_live_ok) else "FAIL"
    impracticality = None
    if live_status != "PASS":
        impracticality = {
            "resource": "Blender/USD live runtime",
            "code": "IMP-ACCESS",
            "failure_signature": "blender runtime and/or pxr runtime unavailable in lane environment",
            "fallback": "retain deterministic adapter simulation evidence only",
            "claim_impact": "MOC-C007 max-wave live-runtime closure remains explicit FAIL until live runtime is proven",
        }

    roundtrip_path = gate_file("mocap_blender_roundtrip.json")
    roundtrip_payload = read_json(roundtrip_path) if roundtrip_path.exists() else {}
    roundtrip_payload["live_runtime_attempt"] = {
        "status": live_status,
        "blender_live_ok": blender_live_ok,
        "usd_live_ok": usd_live_ok,
        "usd_runtime_interpreter": usd_runtime_interpreter,
        "note": blender_note,
    }
    write_json(roundtrip_path, roundtrip_payload)

    write_json(
        gate_file("usd_live_runtime_check.json"),
        {
            "status": "PASS" if usd_live_ok else "FAIL",
            "usd_runtime_interpreter": usd_runtime_interpreter,
            "env_report": {
                "exists": env_report.get("exists"),
                "loaded_keys": env_report.get("loaded_keys", []),
                "parse_errors": env_report.get("parse_errors", []),
            },
            "evidence": evidence,
        },
    )

    comet_log_metrics(
        comet,
        {
            "live_runtime_status": 1 if live_status == "PASS" else 0,
            "blender_live_ok": 1 if blender_live_ok else 0,
            "usd_live_ok": 1 if usd_live_ok else 0,
            "corpus_type": 0 if corpus == "synthetic" else 1,
        },
    )
    comet_log_asset(comet, roundtrip_path)
    comet_log_asset(comet, gate_file("usd_live_runtime_check.json"))

    comet_url = finalize_comet(comet)
    write_checkpoint(
        gate="gate_m2",
        status="PASS" if live_status == "PASS" else "FAIL",
        details={
            "live_status": live_status,
            "impracticality": impracticality,
        },
        comet_url=comet_url,
    )
    update_run_manifest(
        {
            "gate": "gate_m2",
            "corpus": corpus,
            "status": "PASS" if live_status == "PASS" else "FAIL",
            "timestamp_utc": now_iso(),
            "comet_experiment_url": comet_url,
        }
    )


if __name__ == "__main__":
    main()
