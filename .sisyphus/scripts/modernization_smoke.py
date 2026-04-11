from __future__ import annotations

import argparse
import ast
import json
import os
import py_compile
import subprocess
import sys
import traceback
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[2]
SISYPHUS_DIR = REPO_ROOT / ".sisyphus"
LEDGER_PATH = SISYPHUS_DIR / "task-1-modernization-ledger.json"
EVIDENCE_DIR = SISYPHUS_DIR / "evidence"
SUMMARY_JSON_PATH = EVIDENCE_DIR / "task-2-smoke-summary.json"
SUMMARY_MD_PATH = EVIDENCE_DIR / "task-2-smoke-summary.md"

CHECK_IMPORT_SMOKE = "import-smoke"
CHECK_ENTRYPOINT_SMOKE = "entrypoint-smoke"
CHECK_DUPLICATE_AUTHORITY = "duplicate-authority"
CHECK_RESOLVER_SMOKE = "resolver-smoke"
CHECK_ALL = "all"

CHECK_OUTPUTS = {
    CHECK_IMPORT_SMOKE: EVIDENCE_DIR / "task-2-import-smoke.json",
    CHECK_ENTRYPOINT_SMOKE: EVIDENCE_DIR / "task-2-entrypoint-smoke.json",
    CHECK_DUPLICATE_AUTHORITY: EVIDENCE_DIR / "task-2-duplicate-authority.json",
    CHECK_RESOLVER_SMOKE: EVIDENCE_DIR / "task-2-resolver-smoke.json",
}


@dataclass(frozen=True)
class ImportAttempt:
    module: str
    path: Path
    authority: str
    pythonpath: str | None = None


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_ledger() -> dict[str, Any]:
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def ensure_evidence_dir() -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


def make_parent_status(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def run_import_attempt(attempt: ImportAttempt) -> dict[str, Any]:
    if not attempt.path.exists():
        return {
            "module": attempt.module,
            "authority": attempt.authority,
            "path": make_parent_status(attempt.path),
            "status": "missing_expected_future"
            if attempt.authority == "future"
            else "missing_current_module_path",
            "import_ok": False,
            "detail": "module path does not exist",
        }

    env = os.environ.copy()
    if attempt.pythonpath:
        existing_pythonpath = env.get("PYTHONPATH")
        env["PYTHONPATH"] = (
            attempt.pythonpath
            if not existing_pythonpath
            else os.pathsep.join([attempt.pythonpath, existing_pythonpath])
        )
    code = "\n".join(
        [
            "import importlib, json, sys, traceback",
            "name = sys.argv[1]",
            "payload = {'module': name}",
            "try:",
            "    importlib.import_module(name)",
            "    payload.update({'status': 'pass', 'import_ok': True})",
            "except Exception as exc:",
            "    payload.update({'status': 'fail', 'import_ok': False, 'error_type': type(exc).__name__, 'error': str(exc), 'traceback': traceback.format_exc()})",
            "print(json.dumps(payload, ensure_ascii=False))",
        ]
    )
    completed = subprocess.run(
        [sys.executable, "-c", code, attempt.module],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()

    payload: dict[str, Any] = {
        "module": attempt.module,
        "authority": attempt.authority,
        "path": make_parent_status(attempt.path),
        "pythonpath": attempt.pythonpath,
        "returncode": completed.returncode,
    }
    if not stdout:
        payload.update(
            {
                "status": "fail",
                "import_ok": False,
                "error_type": "NoOutputError",
                "error": "import probe produced no stdout",
                "stderr": stderr,
            }
        )
        return payload

    try:
        payload.update(json.loads(stdout.splitlines()[-1]))
    except json.JSONDecodeError:
        payload.update(
            {
                "status": "fail",
                "import_ok": False,
                "error_type": "JsonDecodeError",
                "error": "import probe did not emit valid JSON",
                "stdout": stdout,
                "stderr": stderr,
            }
        )
        return payload

    if stderr:
        payload["stderr"] = stderr
    return payload


def module_name_from_package_path(package_path: str) -> str:
    parts = Path(package_path).parts
    if not parts:
        return ""
    if parts[0] == "src":
        parts = parts[1:]
    return ".".join(parts)


def summarize_statuses(
    results: list[dict[str, Any]], *, fail_keys: set[str] | None = None
) -> str:
    fail_keys = fail_keys or {"fail", "missing_current_module_path"}
    statuses = {result.get("status") for result in results}
    if statuses & fail_keys:
        return "fail"
    if statuses - {"pass"}:
        return "attention"
    return "pass"


def run_import_smoke(ledger: dict[str, Any]) -> dict[str, Any]:
    root_packages = [
        entry["source"] for entry in ledger["mapping"] if entry["kind"] == "package"
    ]
    future_package_paths = ledger["canonical_boundaries"]["packages"]
    future_modules = [
        "wzry_ai",
        *[module_name_from_package_path(path) for path in future_package_paths],
    ]
    future_modules = list(dict.fromkeys(future_modules))

    attempts: list[ImportAttempt] = []
    for package_name in root_packages:
        attempts.append(
            ImportAttempt(
                module=package_name,
                path=REPO_ROOT / package_name,
                authority="root",
            )
        )

    src_root = REPO_ROOT / "src"
    for module_name in future_modules:
        relative_parts = module_name.split(".")
        module_path = src_root.joinpath(*relative_parts)
        attempts.append(
            ImportAttempt(
                module=module_name,
                path=module_path,
                authority="future",
                pythonpath=str(src_root),
            )
        )

    results = [run_import_attempt(attempt) for attempt in attempts]
    status = summarize_statuses(results)
    return {
        "check": CHECK_IMPORT_SMOKE,
        "status": status,
        "generated_at": utc_now(),
        "repo_root": str(REPO_ROOT),
        "ledger": make_parent_status(LEDGER_PATH),
        "results": results,
        "summary": {
            "root_modules": len(
                [result for result in results if result["authority"] == "root"]
            ),
            "future_modules": len(
                [result for result in results if result["authority"] == "future"]
            ),
            "root_failures": len(
                [
                    result
                    for result in results
                    if result["authority"] == "root" and result["status"] != "pass"
                ]
            ),
            "future_pending": len(
                [
                    result
                    for result in results
                    if result["authority"] == "future" and result["status"] != "pass"
                ]
            ),
        },
    }


def _has_main_guard(test: ast.AST) -> bool:
    if not isinstance(test, ast.Compare):
        return False
    if not isinstance(test.left, ast.Name) or test.left.id != "__name__":
        return False
    if len(test.ops) != 1 or not isinstance(test.ops[0], ast.Eq):
        return False
    if len(test.comparators) != 1:
        return False
    comparator = test.comparators[0]
    if isinstance(comparator, ast.Constant):
        return comparator.value == "__main__"
    if isinstance(comparator, ast.Str):
        return comparator.s == "__main__"
    return False


def inspect_entrypoint(path: Path, *, authority: str) -> dict[str, Any]:
    result: dict[str, Any] = {
        "authority": authority,
        "path": make_parent_status(path),
        "exists": path.exists(),
    }
    if not path.exists():
        result["status"] = (
            "missing_expected_future" if authority == "future" else "fail"
        )
        result["detail"] = "entrypoint file does not exist"
        return result

    result["file_size_bytes"] = path.stat().st_size
    try:
        py_compile.compile(str(path), doraise=True)
        result["compile_ok"] = True
    except py_compile.PyCompileError as exc:
        result["compile_ok"] = False
        result["status"] = "fail"
        result["error_type"] = type(exc).__name__
        result["error"] = str(exc)
        return result

    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError, UnicodeDecodeError) as exc:
        result["status"] = "fail"
        result["ast_ok"] = False
        result["error_type"] = type(exc).__name__
        result["error"] = str(exc)
        return result

    functions = [
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    result["ast_ok"] = True
    result["functions"] = functions
    result["has_main_function"] = "main" in functions
    result["has_main_guard"] = any(
        isinstance(node, ast.If) and _has_main_guard(node.test) for node in tree.body
    )
    result["status"] = "pass"
    if authority == "future" and not result["has_main_guard"]:
        result["status"] = "attention"
        result["detail"] = "future entrypoint exists but has no __main__ guard"
    return result


def run_entrypoint_smoke(ledger: dict[str, Any]) -> dict[str, Any]:
    root_entrypoints = [
        REPO_ROOT / shim for shim in ledger.get("default_root_shims", [])
    ]
    future_entrypoints = [REPO_ROOT / ledger["canonical_entrypoint"]]
    results = [inspect_entrypoint(path, authority="root") for path in root_entrypoints]
    results.extend(
        inspect_entrypoint(path, authority="future") for path in future_entrypoints
    )
    status = summarize_statuses(results)
    return {
        "check": CHECK_ENTRYPOINT_SMOKE,
        "status": status,
        "generated_at": utc_now(),
        "repo_root": str(REPO_ROOT),
        "results": results,
    }


def run_duplicate_authority_smoke(ledger: dict[str, Any]) -> dict[str, Any]:
    root_packages = [
        entry["source"] for entry in ledger["mapping"] if entry["kind"] == "package"
    ]
    canonical_root = REPO_ROOT / ledger["canonical_code_root"]
    results: list[dict[str, Any]] = []

    for package_name in root_packages:
        root_path = REPO_ROOT / package_name
        canonical_path = canonical_root / package_name
        duplicate = root_path.exists() and canonical_path.exists()
        results.append(
            {
                "package": package_name,
                "root_path": make_parent_status(root_path),
                "root_exists": root_path.exists(),
                "canonical_path": make_parent_status(canonical_path),
                "canonical_exists": canonical_path.exists(),
                "status": "fail"
                if duplicate
                else (
                    "missing_expected_future" if not canonical_root.exists() else "pass"
                ),
                "duplicate_authority": duplicate,
            }
        )

    status = summarize_statuses(results)
    duplicates = [
        result["package"] for result in results if result["duplicate_authority"]
    ]
    return {
        "check": CHECK_DUPLICATE_AUTHORITY,
        "status": status,
        "generated_at": utc_now(),
        "repo_root": str(REPO_ROOT),
        "canonical_code_root": make_parent_status(canonical_root),
        "canonical_code_root_exists": canonical_root.exists(),
        "duplicate_packages": duplicates,
        "results": results,
    }


def find_resolver_candidates(code_root: Path) -> list[Path]:
    candidates: list[Path] = []
    for owner in ("app", "utils"):
        owner_root = code_root / owner
        if not owner_root.exists():
            continue
        candidates.extend(sorted(owner_root.rglob("*resolver*.py")))
    return candidates


def run_resolver_smoke(ledger: dict[str, Any]) -> dict[str, Any]:
    canonical_code_root = REPO_ROOT / ledger["canonical_code_root"]
    src_root = REPO_ROOT / "src"
    root_candidates = find_resolver_candidates(REPO_ROOT)
    if not canonical_code_root.exists():
        results: list[dict[str, Any]] = []
        for candidate in root_candidates:
            module_name = ".".join(
                candidate.relative_to(REPO_ROOT).with_suffix("").parts
            )
            import_result = run_import_attempt(
                ImportAttempt(
                    module=module_name,
                    path=candidate,
                    authority="root",
                )
            )
            import_result["candidate_path"] = make_parent_status(candidate)
            import_result["detail"] = "root transition resolver candidate"
            results.append(import_result)

        return {
            "check": CHECK_RESOLVER_SMOKE,
            "status": "fail"
            if any(result["status"] == "fail" for result in results)
            else "attention",
            "generated_at": utc_now(),
            "repo_root": str(REPO_ROOT),
            "canonical_code_root": make_parent_status(canonical_code_root),
            "root_resolver_candidates": [
                make_parent_status(candidate) for candidate in root_candidates
            ],
            "results": results
            or [
                {
                    "status": "missing_expected_future",
                    "detail": "canonical package tree does not exist yet and no root transition resolver candidate was found",
                }
            ],
        }

    candidates = find_resolver_candidates(canonical_code_root)
    if not candidates:
        return {
            "check": CHECK_RESOLVER_SMOKE,
            "status": "attention",
            "generated_at": utc_now(),
            "repo_root": str(REPO_ROOT),
            "canonical_code_root": make_parent_status(canonical_code_root),
            "results": [
                {
                    "status": "missing_expected_future",
                    "detail": "no resolver candidate files found under src/wzry_ai/app or src/wzry_ai/utils",
                }
            ],
        }

    results: list[dict[str, Any]] = []
    for candidate in candidates:
        module_name = ".".join(candidate.relative_to(src_root).with_suffix("").parts)
        import_result = run_import_attempt(
            ImportAttempt(
                module=module_name,
                path=candidate,
                authority="future",
                pythonpath=str(src_root),
            )
        )
        import_result["candidate_path"] = make_parent_status(candidate)
        results.append(import_result)

    status = summarize_statuses(results)
    return {
        "check": CHECK_RESOLVER_SMOKE,
        "status": status,
        "generated_at": utc_now(),
        "repo_root": str(REPO_ROOT),
        "canonical_code_root": make_parent_status(canonical_code_root),
        "resolver_candidates": [
            make_parent_status(candidate) for candidate in candidates
        ],
        "results": results,
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def build_markdown_summary(summary: dict[str, Any]) -> str:
    lines = [
        "# Task 2 Smoke Summary",
        "",
        f"- Generated at: `{summary['generated_at']}`",
        f"- Overall status: `{summary['overall_status']}`",
        "",
        "## Checks",
    ]
    for check in summary["checks"]:
        lines.append(
            f"- `{check['check']}` → `{check['status']}` (`{check['evidence_path']}`)"
        )
    lines.append("")
    lines.append("## Notes")
    for note in summary["notes"]:
        lines.append(f"- {note}")
    lines.append("")
    return "\n".join(lines)


def selected_checks(name: str) -> list[str]:
    if name == CHECK_ALL:
        return [
            CHECK_IMPORT_SMOKE,
            CHECK_ENTRYPOINT_SMOKE,
            CHECK_DUPLICATE_AUTHORITY,
            CHECK_RESOLVER_SMOKE,
        ]
    return [name]


def run_selected_checks(
    selected: list[str], ledger: dict[str, Any]
) -> list[dict[str, Any]]:
    runners = {
        CHECK_IMPORT_SMOKE: run_import_smoke,
        CHECK_ENTRYPOINT_SMOKE: run_entrypoint_smoke,
        CHECK_DUPLICATE_AUTHORITY: run_duplicate_authority_smoke,
        CHECK_RESOLVER_SMOKE: run_resolver_smoke,
    }
    payloads: list[dict[str, Any]] = []
    for name in selected:
        payload = runners[name](ledger)
        write_json(CHECK_OUTPUTS[name], payload)
        payloads.append(payload)
    return payloads


def build_summary(payloads: list[dict[str, Any]]) -> dict[str, Any]:
    overall_status = summarize_statuses(
        [{"status": payload["status"]} for payload in payloads], fail_keys={"fail"}
    )
    notes = []
    if any(payload["status"] == "attention" for payload in payloads):
        notes.append(
            "Attention states are expected while future package and entrypoint paths do not exist yet."
        )
    if any(
        payload["check"] == CHECK_DUPLICATE_AUTHORITY and payload["status"] == "fail"
        for payload in payloads
    ):
        notes.append(
            "Duplicate authority means both root and src/wzry_ai implementations are present for the same package."
        )
    if not notes:
        notes.append("All selected smoke checks passed without attention findings.")
    return {
        "generated_at": utc_now(),
        "overall_status": overall_status,
        "checks": [
            {
                "check": payload["check"],
                "status": payload["status"],
                "evidence_path": make_parent_status(CHECK_OUTPUTS[payload["check"]]),
            }
            for payload in payloads
        ],
        "notes": notes,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Characterization smoke harness for modernization waves."
    )
    parser.add_argument(
        "check",
        nargs="?",
        default=CHECK_ALL,
        choices=[
            CHECK_ALL,
            CHECK_IMPORT_SMOKE,
            CHECK_ENTRYPOINT_SMOKE,
            CHECK_DUPLICATE_AUTHORITY,
            CHECK_RESOLVER_SMOKE,
        ],
        help="Smoke check to run. Defaults to all.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return exit code 2 when any selected check is not pass.",
    )
    return parser.parse_args()


def main() -> int:
    ensure_evidence_dir()
    if not LEDGER_PATH.exists():
        error_payload = {
            "generated_at": utc_now(),
            "overall_status": "fail",
            "notes": [f"Ledger missing: {make_parent_status(LEDGER_PATH)}"],
            "traceback": traceback.format_exc(),
        }
        write_json(SUMMARY_JSON_PATH, error_payload)
        SUMMARY_MD_PATH.write_text(
            build_markdown_summary({**error_payload, "checks": []}), encoding="utf-8"
        )
        return 1

    args = parse_args()
    ledger = load_ledger()
    payloads = run_selected_checks(selected_checks(args.check), ledger)
    summary = build_summary(payloads)
    write_json(SUMMARY_JSON_PATH, summary)
    SUMMARY_MD_PATH.write_text(build_markdown_summary(summary), encoding="utf-8")

    for payload in payloads:
        print(
            f"{payload['check']}: {payload['status']} -> {make_parent_status(CHECK_OUTPUTS[payload['check']])}"
        )
    print(
        f"summary: {summary['overall_status']} -> {make_parent_status(SUMMARY_JSON_PATH)}"
    )

    if args.strict and any(payload["status"] != "pass" for payload in payloads):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
