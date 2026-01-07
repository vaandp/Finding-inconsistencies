from __future__ import annotations

import csv
import re
from pathlib import Path


BASE = Path(__file__).resolve().parent.parent
SOURCE_CSV = BASE / "Compix@Grasp/top1000.csv"
GRASP_DIR = BASE / "Compix@Grasp/grasp_query_result"
OUT_CSV = BASE / "Compix@Grasp/Finding_Inconsistency/sample_contrast.csv"

#lines of the form "Label (wd:Qxxxx)" or "Label (xsd:xxxx)" only
ENTITY_LINE_PATTERN1 = re.compile(r"(.+?)\s*\(wd:([^)]+)\)")
ENTITY_LINE_PATTERN2 = re.compile(r"(.+?)\s*\(xsd:([^)]+)\)")
ENTITY_LINE_PATTERN3 = re.compile(r"(.+?)\s*\(lang:([^)]+)\)")


def extract_grasp_answer(qid):
    #return tuple (answer, answer_id) if it is of the form 'XXX (wd:Qxxxx)' or 'XXX (xsd:xxxx)'
    txt_path = GRASP_DIR / f"{qid}.txt"
    if not txt_path.exists():
        return (None, None)

    content = txt_path.read_text(encoding="utf-8").strip()
    if not content:
        return (None, None)

    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        
        # Try to match pattern with wd: prefix
        match = ENTITY_LINE_PATTERN1.fullmatch(line)
        if match:
            answer = match.group(1).strip()
            answer_id = match.group(2).strip()
            return (answer, answer_id)
        
        # Try to match pattern with xsd: prefix
        match = ENTITY_LINE_PATTERN2.fullmatch(line)
        if match:
            answer = match.group(1).strip()
            answer_id = match.group(2).strip()
            return (answer, answer_id)
        
        # Try to match pattern with lang: prefix
        match = ENTITY_LINE_PATTERN3.fullmatch(line)
        if match:
            answer = match.group(1).strip()
            answer_id = match.group(2).strip()
            return (answer, answer_id)

        # If no pattern matches, return the line as answer with no ID
        break

    return (None, None)


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
            "CompMix_answer_id",
            "GRASP_SPARQL_answer",
            "GRASP_SPARQL_answer_id",
            "ID_match"
        ]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        missing = 0
        written = 0
        id_matches = 0
        id_mismatches = 0
        both_empty = 0
        one_empty = 0

        for row in reader:
            qid = (row.get("question_id") or "").strip()
            question = (row.get("question") or "").strip()
            answer_label = (row.get("answer_label") or "").strip()
            answer_id = (row.get("answer_id") or "").strip()

            if not (qid and question and answer_label):
                missing += 1
                continue

            grasp_answer, grasp_answer_id = extract_grasp_answer(qid)

            # Compare the IDs
            compmix_id = answer_id.strip() if answer_id else ""
            grasp_id = (grasp_answer_id or "").strip() if grasp_answer_id else ""
            
            # Determine match status
            if not compmix_id and not grasp_id:
                id_match = "Both_empty"
                both_empty += 1
            elif not compmix_id or not grasp_id:
                id_match = "False"
                one_empty += 1
                id_mismatches += 1
            elif compmix_id == grasp_id:
                id_match = "True"
                id_matches += 1
            else:
                id_match = "False"
                id_mismatches += 1

            writer.writerow(
                {
                    "Question_id": qid,
                    "Question": question,
                    "CompMix_answer_label": answer_label,
                    "CompMix_answer_id": answer_id,
                    "GRASP_SPARQL_answer": grasp_answer or "",
                    "GRASP_SPARQL_answer_id": grasp_answer_id or "",
                    "ID_match": id_match,
                }
            )
            written += 1

    print(f"\n{'='*60}")
    print(f"Statistics of ID matching")
    print(f"{'='*60}")
    if missing:
        print(f"Lines ignored (missing field) : {missing}")
    print(f"\nID matching :")
    print(f"  - IDs identical : {id_matches} ({id_matches/written*100:.2f}%)")
    print(f"  - IDs different : {id_mismatches} ({id_mismatches/written*100:.2f}%)")
    print(f"  - Both empty : {both_empty} ({both_empty/written*100:.2f}%)")
    print(f"  - One empty : {one_empty} ({one_empty/written*100:.2f}%)")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()


