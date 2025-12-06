# CompMix@Grasp Dataset

This dataset contains the 2,000 Text2SPARQL experiment for Question-Answer Pairs from [CompMix](https://qa.mpi-inf.mpg.de/compmix/) using [GRASP](https://grasp.cs.uni-freiburg.de/).  


The questions are ranked by their contextual richness using a weighted Question Context Score.


```
Question Context Score = w1 * (# of entities) + w2 * (question length in tokens)
```

Because entity count carries more contextual information than raw question length, we use:

- **w1 = 0.7** (weight for number of entities)  
- **w2 = 0.3** (weight for question length)

---


Questions are sorted by this score into two subsets:
- **Top 1,000**: highest contextual richness  
- **Bottom 1,000**: lowest contextual richness

---

## Dataset Components

### Question Lists
- **top1000.csv** — questions with the highest context scores  
- **bottom1000.csv** — questions with the lowest context scores  

### GRASP Outputs
- **top1000/** — original GRASP output for each high-context question  
- **bottom1000/** — original GRASP output for each low-context question  

### Processed Queries and Results
- **generated_query/** — cleaned GRASP-generated SPARQL queries, standardized for execution on the Wikidata Query Service  
- **grasp_query_result/** — results from executing GRASP queries on GRASP’s internal precomputed Wikidata index  
- **wikidata_query_result/** — results from executing the same queries on the public WDQS endpoint  

### Inconsistency Analysis
- **Finding_Inconsistency/** — a sample summary table illustrating inconsistency between CompMix gold answers and GRASP SPARQL result

---

## Generation Pipeline

The GRASP SPARQL queries were produced using the script **`run.py`**, configured with the following model setup:
```
Qwen/Qwen3-4B-Instruct-2507 --reasoning-parser qwen3 --tool-call-parser hermes --enable-auto-tool-choice --max-model-len 225136
```

