from __future__ import annotations

import csv
import io
import re
import time
from pathlib import Path

import requests


BASE = Path(__file__).resolve().parent.parent
RQ_DIR = BASE / "Compix@Grasp/generated_query"
OUT_DIR = BASE / "Compix@Grasp/wikidata_query_result"

ENDPOINT_URL = "https://query.wikidata.org/sparql"
HEADERS = {
    "Accept": "text/csv",
    "User-Agent": "Finding-inconsistencies-student-project/1.0 (mailto:vadiep.20@gmail.com)",
}


retrive_id = re.compile(r"https?://www\.wikidata\.org/entity/([A-Za-z0-9]+)")
qid = re.compile(r"^Q[0-9]+$")


def _strip_entity_uris(csv_text):
    #replace the entity uri with the id
    return retrive_id.sub(r"\1", csv_text)


def _fetch_labels(qids: list[str]) -> dict[str, str]:
    #keep the labels of the qids
    if not qids:
        return {}

    labels = {}
    chunk_size = 50  # limit of the api

    for i in range(0, len(qids), chunk_size):
        chunk = qids[i : i + chunk_size]
        ids_param = "|".join(chunk)

        try:
            resp = requests.get(
                "https://www.wikidata.org/w/api.php",
                params={
                    "action": "wbgetentities",
                    "format": "json",
                    "ids": ids_param,
                    "props": "labels",
                    "languages": "en",
                },
                headers=HEADERS,
                timeout=30,
            )
            # if the api refuse (403/429), skip this block to not block the execution
            if resp.status_code != 200:
                print(f"    -> Impossible to retrieve the labels for {ids_param} (HTTP {resp.status_code})")
                continue
            data = resp.json()
        except Exception as e:  # noqa: BLE001
            print(f"    -> Erreur lors de la récupération des labels pour {ids_param}: {e}")
            continue

        entities = data.get("entities", {})
        for qid, entity in entities.items():
            #label_fr = entity.get("labels", {}).get("fr", {}).get("value")
            label_en = entity.get("labels", {}).get("en", {}).get("value")
            #if label_fr:
             #   labels[qid] = label_fr
            #elif label_en:
            #    labels[qid] = label_en
            labels[qid] = label_en

    return labels


def _replace_qids_with_labels(csv_text: str) -> str:
    #replace the qids with the labels in the csv
    reader = csv.reader(csv_text.splitlines())
    rows = list(reader)

    #collect the qids in the csv
    qids= set()
    for row in rows:
        for cell in row:
            if qid.match(cell):
                qids.add(cell)

    label_map = _fetch_labels(sorted(qids))

    #replace the qids with the labels in the csv
    output = io.StringIO()
    writer = csv.writer(output)
    for row in rows:
        new_row = [label_map.get(cell, cell) for cell in row]
        writer.writerow(new_row)

    return output.getvalue()


def run_query(rq_path: Path, out_path: Path, sleep_seconds: float = 1.0) -> None:
    #execute the query on the wikidata sparql service and save the result in a csv file
    query = rq_path.read_text(encoding="utf-8")

    response = requests.get(
        ENDPOINT_URL,
        params={"query": query},
        headers=HEADERS,
        timeout=60,
    )

    #error handling
    if response.status_code != 200:
        raise RuntimeError(
            f"HTTP error {response.status_code} for {rq_path.name}: {response.text[:500]}"
        )

    #replace uri with the id only
    cleaned_csv = _strip_entity_uris(response.text)
    #replace the qids with the labels in the csv
    labeled_csv = _replace_qids_with_labels(cleaned_csv)

    out_path.write_text(labeled_csv, encoding="utf-8")

    #small pause between the queries 
    if sleep_seconds > 0:
        time.sleep(sleep_seconds)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rq_files = sorted(RQ_DIR.glob("*.rq"))
    if not rq_files:
        print(f"No .rq file found in {RQ_DIR}")
        return

    total = len(rq_files)
    success = 0
    failed = []

    print(f"Number of queries found : {total}")

    for i, rq_path in enumerate(rq_files, start=1):
        qid = rq_path.stem
        out_path = OUT_DIR / f"{qid}.csv"

        #skip this specific problematic query_id
        if qid == "3907":
            print(f"[{i}/{total}] {qid}: explicitly skipped.")
            continue

        if qid == "6462":
            print(f"[{i}/{total}] {qid}: explicitly skipped.")
            continue

        if qid == "3430":
            print(f"[{i}/{total}] {qid}: explicitly skipped.")
            continue

        if qid == "4079":
            print(f"[{i}/{total}] {qid}: explicitly skipped.")
            continue

        if qid == "6227":
            print(f"[{i}/{total}] {qid}: explicitly skipped.")
            continue

        if qid == "7652":
            print(f"[{i}/{total}] {qid}: explicitly skipped.")
            continue

        if qid == "8648":
            print(f"[{i}/{total}] {qid}: explicitly skipped.")
            continue
        
        if qid == "8753":
            print(f"[{i}/{total}] {qid}: explicitly skipped.")
            continue
        
        #do not execute again if the file already exists (easier to restart partially)
        '''if out_path.exists():
            print(f"[{i}/{total}] {qid}: already exists, skipping.")
            continue'''

        print(f"[{i}/{total}] {qid}: execution in progress...")
        try:
            run_query(rq_path, out_path)
            success += 1
        except Exception as e:  # noqa: BLE001
            print(f"  -> Failure for {qid}: {e}")
            failed.append(qid)

    print(f"\nSuccessful queries : {success}/{total}")
    if failed:
        print(f"Failures for {len(failed)} queries : {', '.join(failed[:20])}"
              f"{' ...' if len(failed) > 20 else ''}")


if __name__ == "__main__":
    main()


