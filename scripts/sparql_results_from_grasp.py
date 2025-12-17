from __future__ import annotations

import csv
import json
from pathlib import Path


BASE = Path(__file__).resolve().parent.parent
CSV_PATH = BASE / "Compix@Grasp/top1000.csv"
JSON_DIR = BASE / "Compix@Grasp/top1000"
OUT_DIR = BASE / "Compix@Grasp/grasp_query_result"


def extract_answer(text):
    lines = text.strip().split('\n')

    last_line = lines[-1]
    
    part = last_line.split('|')
    
    if len(part) > 1:
        return part[1].strip()
    return None

def main():
    missing_json = []
    missing_output = []
    missing_result = []
    decode_errors= []
    written = 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with CSV_PATH.open(newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        total_rows = 0
        for row in reader:
            total_rows += 1
            qid = (row.get("question_id") or "").strip()
            if not qid:
                continue

            json_path = JSON_DIR / f"{qid}.json"
            if not json_path.exists():
                missing_json.append(qid)
                continue

            try:
                data = json.loads(json_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                decode_errors.append(qid)
                continue

            if not isinstance(data, dict):
                decode_errors.append(qid)
                continue

            output = data.get("output")
            if not isinstance(output, dict):
                missing_output.append(qid)
                continue

            result = output.get("result")
            if not isinstance(result, str) or not result.strip():
                missing_result.append(qid)
                continue
            
            select_block = extract_answer(result)
            if select_block:
                result = select_block

            out_path = OUT_DIR / f"{qid}.txt"
            out_path.write_text(
                result if result.endswith("\n") else result + "\n",
                encoding="utf-8",
            )
            written += 1

    print(f"Total line read in csv file : {total_rows}")
    print(f"Number of file .txt generated : {written}")
    if missing_json:
        print(
            f"JSON not found ({len(missing_json)}) : "
            f"{', '.join(missing_json[:10])}"
            f"{' ...' if len(missing_json) > 10 else ''}"
        )
    if decode_errors:
        print(
            f"Invalid JSON ({len(decode_errors)}) : "
            f"{', '.join(decode_errors[:10])}"
            f"{' ...' if len(decode_errors) > 10 else ''}"
        )
    if missing_output:
        print(
            f"Key 'output' not found ({len(missing_output)}) : "
            f"{', '.join(missing_output[:10])}"
            f"{' ...' if len(missing_output) > 10 else ''}"
        )
    if missing_result:
        print(
            f"Key 'result' not found or empty ({len(missing_result)}) : "
            f"{', '.join(missing_result[:10])}"
            f"{' ...' if len(missing_result) > 10 else ''}"
        )


if __name__ == "__main__":
    main()
