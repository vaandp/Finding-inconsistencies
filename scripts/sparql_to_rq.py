from __future__ import annotations

import csv
import json
import re
from pathlib import Path

#load the file 
BASE = Path(__file__).resolve().parent.parent
CSV_PATH = BASE / "Compix@Grasp/top1000.csv"
JSON_DIR = BASE / "Compix@Grasp/top1000"
OUT_DIR = BASE / "Compix@Grasp/top1000_rq"


def extract_select_block(sparql: str) -> str | None:
    """Retourne uniquement le bloc SELECT … } s'il existe."""
    match = re.search(r"(SELECT[\s\S]*?})", sparql, flags=re.IGNORECASE)
    return match.group(1).strip() if match else None


def main():
    missing_json= []
    missing_sparql= []
    decode_errors= []
    trimmed = 0
    written = 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with CSV_PATH.open(newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        total_rows = 0
        found_sparql = 0
        for row in reader:
            #get the question id
            total_rows += 1
            qid = (row.get("question_id") or "").strip()
            if not qid:
                continue

            #get the json file
            json_path = JSON_DIR / f"{qid}.json"
            if not json_path.exists():
                missing_json.append(qid)
                continue

            #load the json file
            try:
                data = json.loads(json_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                decode_errors.append(qid)
                continue

            #check if the data is a dictionary
            if not isinstance(data, dict):
                decode_errors.append(qid)
                continue

            #get the output
            output = data.get("output") if isinstance(data, dict) else {}
            if not isinstance(output, dict):
                missing_sparql.append(qid)
                continue

            #get the sparql
            sparql = output.get("sparql")
            if not sparql:
                missing_sparql.append(qid)
                continue

            #write uniquement le bloc SELECT ... } si présent
            select_block = extract_select_block(sparql)
            if select_block:
                sparql = select_block
                trimmed += 1

            out_path = OUT_DIR / f"{qid}.rq"
            out_path.write_text(
                sparql if sparql.endswith("\n") else sparql + "\n",
                encoding="utf-8",
            )
            #increment the number of written files and found sparql
            written += 1
            found_sparql += 1

    print(f"Total line read in csv file : {total_rows}")
    print(f"Number of file .rq generated : {written} (SPARQL found : {found_sparql})")
    if missing_json:
        print(
            f"JSON not found ({len(missing_json)}): "
            f"{', '.join(missing_json[:10])}"
            f"{' ...' if len(missing_json) > 10 else ''}"
        )
    if decode_errors:
        print(
            f"Invalid JSON ({len(decode_errors)}): "
            f"{', '.join(decode_errors[:10])}"
            f"{' ...' if len(decode_errors) > 10 else ''}"
        )
    if missing_sparql:
        print(
            f"SPARQL not found ({len(missing_sparql)}): "
            f"{', '.join(missing_sparql[:10])}"
            f"{' ...' if len(missing_sparql) > 10 else ''}"
        )


if __name__ == "__main__":
    main()

