from __future__ import annotations

import csv
import re
from pathlib import Path
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from datetime import datetime


BASE = Path(__file__).resolve().parent.parent
SOURCE_CSV = BASE / "Compix@Grasp/top1000.csv"
GRASP_DIR = BASE / "Compix@Grasp/wikidata_query_result"
OUT_CSV = BASE / "Compix@Grasp/Finding_Inconsistency/sample_contrast.csv"

# 1. Load a pretrained Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def is_valid_iso_date(date_str: str) -> bool:
    try:
        # Le format correspond à : Année-Mois-Jour T Heure:Minute:Seconde Z
        datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        return True
    except ValueError:
        return False

def compare_date(qid, real_answer):
    txt_path = GRASP_DIR / f"{qid}.csv"
    if not txt_path.exists():
        return (None,None)
    items = []
    with txt_path.open(encoding="utf-8") as f:
        reader = csv.reader(f)
        items = [row[0] for row in reader if row]
    if not items:
        return (None,None)

    items=items[1:]
    if not items:
        return (None, None)

    similarity_score=[]

    for i in range (len(items)):
        # Calculate embeddings for both answers 
        try:
            date=datetime.strptime(items[i], "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            if type(real_answer) != datetime:
                real_answer=datetime.strptime(real_answer, "%Y-%m-%dT%H:%M:%SZ")
            if items[i] == str(real_answer.year):
                similarity_score.append(1)
            else:
                similarity_score.append(0)
            continue
        if type(real_answer) != datetime:
            real_answer=datetime.strptime(real_answer, "%Y-%m-%dT%H:%M:%SZ")
        if date.year == real_answer.year and date.month == real_answer.month and date.day == real_answer.day:
            if date.hour == real_answer.hour and date.minute == real_answer.minute and date.second == real_answer.second:
                similarity_score.append(1)
            else:
                similarity_score.append( 0.8)
        elif date.year == real_answer.year and date.month == real_answer.month:
            similarity_score.append(  0.6)
        elif date.year == real_answer.year:
            similarity_score.append(  0.5)
        else:
            similarity_score.append(  0)

    max_value = max(similarity_score)
    index_max = similarity_score.index(max_value)
    
    return (items[index_max], max_value)

def extract_grasp_answer(qid, real_answer):
    txt_path = GRASP_DIR / f"{qid}.csv"
    if not txt_path.exists():
        return (None,None)

    # --- MODIFICATION ICI ---
    # On lit le fichier ligne par ligne comme un CSV à une colonne
    # pour récupérer TOUS les éléments dans une liste (items)
    items = []
    with txt_path.open(encoding="utf-8") as f:
        reader = csv.reader(f)
        # On prend la 1ère colonne de chaque ligne non vide
        items = [row[0] for row in reader if row]

    if not items:
        return (None,None)

    #take off the name of the column
    items=items[1:]

    if not items:
        return (None, None)

    similarity_score=[]

    for i in range (len(items)):
        # Calculate embeddings for both answers
        embeddings = model.encode([items[i], real_answer])
        #print ("HERE IS THE CODE")
        #print (items[i]+""+real_answer)
        
        # Calculate cosine similarity between the two embeddings
        similarity = cos_sim(embeddings[0], embeddings[1])

        # Extract the scalar value from the tensor
        score = float(similarity.item())
        similarity_score.append(score)
    
    max_value = max(similarity_score)
    index_max = similarity_score.index(max_value)
    
    return (items[index_max], max_value)


def main() -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    with SOURCE_CSV.open(encoding="utf-8-sig", newline="") as infile, OUT_CSV.open(
        "w", encoding="utf-8", newline=""
    ) as outfile:
        reader = csv.DictReader(infile)
        fieldnames = [
            "Question_id",
            "Question",
            "Question_entity",
            "CompMix_answer_label",
            "CompMix_answer_id",
            "GRASP_SPARQL_answer",
            "Consistency_score"
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
            question_entity=(row.get("entity_id1") or "").strip()
            answer_label = (row.get("answer_label") or "").strip()
            answer_id = (row.get("answer_id") or "").strip()
            print(qid, answer_id)
            if not (qid and question and answer_label):
                missing += 1
                continue
            if qid == "7229" or qid == "416" or qid=="6191":
                missing += 1
                continue

            if is_valid_iso_date(answer_id):
                grasp_answer, consistency_score = compare_date(qid, answer_id)
            else:
                grasp_answer, consistency_score = extract_grasp_answer(qid, answer_label)

            writer.writerow(
                {
                    "Question_id": qid,
                    "Question": question,
                    "Question_entity":question_entity,
                    "CompMix_answer_label": answer_label,
                    "CompMix_answer_id": answer_id,
                    "GRASP_SPARQL_answer": grasp_answer or "",
                    "Consistency_score":consistency_score or "",
                }
            )
            written += 1

if __name__ == "__main__":
    main()


