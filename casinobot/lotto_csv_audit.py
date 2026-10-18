"""Read-only integrity audit for historical Lotto 6/49 CSV files."""
import csv
import hashlib
from datetime import datetime
from pathlib import Path

def load_draws(path):
    raw = Path(path).read_bytes()
    rows = []
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        for line, row in enumerate(csv.reader(handle), 1):
            if len(row) != 8:
                raise ValueError(f"line {line}: expected 8 fields")
            try:
                draw_id = int(row[0])
                date = datetime.strptime(row[1], "%d.%m.%Y").date()
                numbers = tuple(int(n) for n in row[2:])
            except (ValueError, OverflowError) as exc:
                raise ValueError(f"line {line}: invalid field") from exc
            if draw_id <= 0 or len(set(numbers)) != 6 or any(n < 1 or n > 49 for n in numbers):
                raise ValueError(f"line {line}: invalid 6/49 draw")
            if rows and (draw_id != rows[-1][0] + 1 or date < rows[-1][1]):
                raise ValueError(f"line {line}: invalid ID sequence or date order")
            rows.append((draw_id, date, tuple(sorted(numbers))))
    if not rows:
        raise ValueError("empty archive")
    return rows, hashlib.sha256(raw).hexdigest()

def compare_archives(first, second):
    a, hash_a = load_draws(first)
    b, hash_b = load_draws(second)
    if len(a) != len(b):
        raise ValueError("archive lengths differ")
    mismatches = []
    for left, right in zip(a, b):
        if left[0] != right[0]:
            raise ValueError("draw IDs do not align")
        if left[1:] != right[1:]:
            mismatches.append({
                "draw_id": left[0],
                "first": {"date": left[1].isoformat(), "numbers": list(left[2])},
                "second": {"date": right[1].isoformat(), "numbers": list(right[2])},
            })
    return {
        "rows": len(a), "matches": len(a) - len(mismatches),
        "sha256_first": hash_a, "sha256_second": hash_b,
        "mismatches": mismatches,
        "integrity_status": "review_required" if mismatches else "consistent",
        "note": "Consistency does not establish historical authenticity or predictability.",
    }

if __name__ == "__main__":
    import argparse
    import json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first")
    parser.add_argument("second")
    args = parser.parse_args()
    print(json.dumps(compare_archives(args.first, args.second), ensure_ascii=False, indent=2))
