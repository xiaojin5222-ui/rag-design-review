"""只读离线合成检查。Python 3.9+；标准库；不评估 Agent 输出。"""
import copy
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent


def main():
    checks = []

    def add(name, passed, detail):
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    try:
        source = ROOT / "input" / "retriever.py"
        spec = importlib.util.spec_from_file_location("synthetic_retriever", source)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        data_path = ROOT / "input" / "policies.json"
        before = data_path.read_bytes()
        documents = json.loads(before.decode("utf-8"))["documents"]
        original = copy.deepcopy(documents)
        expectations = json.loads((ROOT / "expected.json").read_text(encoding="utf-8"))
        by_id = {item["id"]: item for item in documents}
        for case in expectations["cases"]:
            actual = module.retrieve(documents, case["topic"], case["day"], case["role"])
            expected = by_id[case["id"]] if case["id"] is not None else None
            add(case["name"], actual == expected,
                {"expected_id": case["id"], "actual_id": actual["id"] if actual else None,
                 "complete_record_matches": actual == expected})
        add("empty_documents", module.retrieve([], "studio-pass", "2032-03-18", "visitor") is None,
            "Empty input returns no supporting record.")
        for name, day, role in [
            ("invalid_calendar_date", "2032-02-30", "visitor"),
            ("noncanonical_date", "2032-3-1", "visitor"),
            ("unknown_role_rejected", "2032-03-18", "administrator"),
        ]:
            rejected = False
            try:
                module.retrieve(documents, "studio-pass", day, role)
            except ValueError:
                rejected = True
            add(name, rejected, "Invalid input must fail explicitly.")
        private_only = [item for item in documents if item["audience"] != "public"]
        add("all_records_forbidden", module.retrieve(private_only, "studio-pass", "2032-03-18", "visitor") is None,
            "A visitor receives no private record when no public alternative exists.")
        tie_a = dict(by_id["pass-spring"], id="same-day-a")
        tie_b = dict(by_id["pass-spring"], id="same-day-b")
        tie_result = module.retrieve([tie_b, tie_a], "studio-pass", "2032-03-18", "visitor")
        add("tie_is_deterministic", tie_result == tie_b,
            {"expected_id": "same-day-b", "actual_id": tie_result["id"]})
        detached = module.retrieve(documents, "studio-pass", "2032-03-18", "visitor")
        detached["text"] = "changed only in the returned copy"
        add("source_and_input_unchanged", documents == original and data_path.read_bytes() == before,
            "Calls and caller mutation of the returned record preserve input records and fixture bytes.")
    except Exception as error:
        add("check_execution", False, {"error_type": type(error).__name__})
    print(json.dumps({"skill": "rag-design-review", "checks": checks,
                      "kind": "offline_fixture_check"}, ensure_ascii=False))
    return 0 if checks and all(item["passed"] for item in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
