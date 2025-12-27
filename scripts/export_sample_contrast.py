from __future__ import annotations

import csv
import re
from pathlib import Path


BASE = Path(__file__).resolve().parent.parent
SOURCE_CSV = BASE / "Compix@Grasp/top1000.csv"
GRASP_DIR = BASE / "Compix@Grasp/grasp_query_result"
OUT_CSV = BASE / "Compix@Grasp/Finding_Inconsistency/sample_contrast.csv"

#lines of the form "Label (wd:Qxxxx)" only
ENTITY_LINE_PATTERN = re.compile(r".+\(wd:[^)]+\)")


def extract_grasp_answer(qid: str) -> str | None:
    #return the grasp answer if it is of the form 'XXX (wd:Qxxxx)'
    txt_path = GRASP_DIR / f"{qid}.txt"
    if not txt_path.exists():
        return None

    content = txt_path.read_text(encoding="utf-8").strip()
    if not content:
        return None

    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if ENTITY_LINE_PATTERN.fullmatch(line):
            return line
        break

    return None


def main() -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    with SOURCE_CSV.open(encoding="utf-8-sig", newline="") as infile, OUT_CSV.open(
        "w", encoding="utf-8", newline=""
    ) as outfile:
        reader = csv.DictReader(infile)
        fieldnames = [
            "Question_id",
            "Question",
            "CompMix_answer_label",
            "GRASP_SPARQL_answer",
        ]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        missing = 0
        written = 0

        for row in reader:
            qid = (row.get("question_id") or "").strip()
            question = (row.get("question") or "").strip()
            answer_label = (row.get("answer_label") or "").strip()

            if not (qid and question and answer_label):
                missing += 1
                continue

            grasp_answer = extract_grasp_answer(qid)

            writer.writerow(
                {
                    "Question_id": qid,
                    "Question": question,
                    "CompMix_answer_label": answer_label,
                    "GRASP_SPARQL_answer": grasp_answer or "",
                }
            )
            written += 1

    print(f"Written lines : {written}")
    if missing:
        print(f"Ignored lines (missing field) : {missing}")


if __name__ == "__main__":
    main()


