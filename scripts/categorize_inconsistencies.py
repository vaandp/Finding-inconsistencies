from __future__ import annotations

from pathlib import Path

import pandas as pd


def main() -> None:
    base = Path(__file__).resolve().parent.parent
    csv_path = base / "Compix@Grasp/Finding_Inconsistency/sample_contrast.csv"

    df = pd.read_csv(csv_path)

    def classify(row) -> str:
        #id_match = str(row.get("ID_match", "")).strip().lower()
        grasp_answer_raw = row.get("GRASP_SPARQL_answer", "")
        score = row.get("Consistency_score", None)

        # Normalize the GRASP answer (handle NaN)
        grasp_answer = "" if pd.isna(grasp_answer_raw) else str(grasp_answer_raw).strip()

        # If the IDs correspond, no category to fill
        """if id_match == "true":
            return """""

        # If GRASP has nothing returned (or both IDs are empty)
        #if not grasp_answer or id_match == "both_empty":
        if not grasp_answer:
            return "Incomplete schema"

        # If the similarity score is low
        try:
            if pd.notna(score) and float(score) < 0.6:
                return "inconsistent"
        except (TypeError, ValueError):
            pass

        # By default, no category
        return ""

    df["Inconsistency_category"] = df.apply(classify, axis=1)

    df.to_csv(csv_path, index=False)

    # Summary
    counts = df["Inconsistency_category"].value_counts(dropna=False).to_dict()
    print(f"Updated {csv_path}")
    print("Category distribution :", counts)


if __name__ == "__main__":
    main()

