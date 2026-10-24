"""离线合成原文选择器；角色参数不是身份认证，不调用任何服务。"""
import copy
from datetime import date
import json
from pathlib import Path
import sys


AUDIENCES = {
    "visitor": {"public"},
    "member": {"public", "member"},
    "staff": {"public", "staff"},
}


def parse_day(value):
    if not isinstance(value, str):
        raise ValueError("date must be YYYY-MM-DD")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise ValueError("date must be YYYY-MM-DD") from error
    if parsed.isoformat() != value:
        raise ValueError("date must be YYYY-MM-DD")
    return parsed


def retrieve(documents, topic, as_of, role):
    """返回完整记录的独立副本；输入集合和数据文件均不改动。"""
    if role not in AUDIENCES:
        raise ValueError("unknown role")
    when = parse_day(as_of)
    candidates = []
    for document in documents:
        if document["topic"] != topic or document["audience"] not in AUDIENCES[role]:
            continue
        start = parse_day(document["valid_from"])
        end = parse_day(document["valid_until"]) if document["valid_until"] else None
        if end is not None and end < start:
            raise ValueError("invalid validity interval")
        if start <= when and (end is None or when <= end):
            candidates.append(document)
    if not candidates:
        return None
    selected = max(candidates, key=lambda item: (parse_day(item["published_at"]), item["id"]))
    return copy.deepcopy(selected)


def main():
    if len(sys.argv) != 5:
        raise SystemExit("usage: retriever.py DATA TOPIC YYYY-MM-DD ROLE")
    path, topic, day, role = sys.argv[1:]
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    print(json.dumps(retrieve(data["documents"], topic, day, role), ensure_ascii=False))


if __name__ == "__main__":
    main()
