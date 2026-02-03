## Project structure

```text
Finding-inconsistencies/
│
├── data/
│   ├── raw/
│   │   ├── compmix_train.json
│   │   ├── compmix_dev.json
│   │   └── compmix_test.json
│   │
│   └── selected/
│       ├── 400_questions.json
│       └── 400_questions.csv
│
├── scripts/
│   ├── categorize_inconsistencies.py        # Categorize inconsistencies based on results
│   ├── compute_basic_stats.py               # Basic statistics on CompMix
│   ├── export_sample_contrast.py            # Export question, golden answer and SPARQL answer to CSV
│   ├── extract_questions_csv.py             # Extract top 400 questions (highest context score) to CSV
│   ├── llm_result_stat.py                   # Statistics on LLM retrieval results
│   ├── plot_domain_distribution.py          # Plot domain distribution of CompMix
│   ├── run_wikidata_queries.py               # Re-run GRASP SPARQL queries on Wikidata
│   ├── select_top_context_questions.py      # Compute context score and plot statistics
│   ├── sparql_results_from_grasp.py         # Extract answers from GRASP JSON files
│   ├── sparql_to_rq.py                      # Extract SPARQL queries from GRASP JSON files
│   ├── stats_grasp_result.py                # Statistics on re-executed GRASP queries
│   ├── transformer_sample_contrast.py       # SentenceTransformer comparison (gold vs SPARQL answer)
│   └── wikidata_llm_inconsistencies.py      # Compare Wikidata properties with LLM (Ollama)
│
├── CompMix@Grasp/
│   ├── top1000/                             # GRASP outputs for highest context-score questions
│   ├── bottom1000/                          # GRASP outputs for lowest context-score questions
│   │
│   ├── Finding_Inconsistency/               # Main inconsistency CSV files
│   │   ├── sample_contrast.csv
│   │   └── sample_contrast_bottom.csv
│   │
│   ├── generated_query/                     # GRASP-generated queries (top1000)
│   ├── generated_query_bottom/              # GRASP-generated queries (bottom1000)
│   │
│   ├── grasp_query_result/
│   │   ├── compmix_train.json
│   │   ├── compmix_dev.json
│   │   └── compmix_test.json
│   │
│   ├── grasp_query_result_bottom/            # Same as above for bottom1000
│   ├── wikidata_query_result/                # Results from re-run Wikidata queries
│   ├── wikidata_query_result_bottom/         # Same for bottom1000
│   │
│   ├── top1000.csv                           # Questions and answers (top1000)
│   └── bottom1000.csv                        # Questions and answers (bottom1000)
│
└── README.md
