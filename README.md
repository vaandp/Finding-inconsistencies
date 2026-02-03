# Finding-inconsistencies

├── data/

│ ├── raw/

│ │ ├── compmix_train.json

│ │ ├── compmix_dev.json

│ │ └── compmix_test.json

│ └── selected/

│ ├── 400_questions.json

│ └── 400_questions.csv

│

├── scripts/

│ ├── categorize_inconsistencies.py      #categorize inconsistencies based on the result

│ ├── compute_basic_stats.py          #statistics of CompMix

│ ├── export_sample_contrast.py        #retrieve the question, golden answer, answer by SPARQL in a csv file

│ ├── extract_questions_csv.py          #extract question with highest context score (400) in a csv file

│ ├── llm_result_stat.py              #statistics from computing the llm retrieving property

│ ├── plot_domain_distribution.py            #plot the domain distribution of CompMix

│ ├── run_wikidata_queries.py                  #re-run the SPARQL query of GRASP

│ ├── select_top_context_questions.py            #compute context score and plot some statistics

│ ├── sparql_results_from_grasp.py            #extract answer from json file of GRASP

│ ├── sparql_to_rq.py                        #extract SPARQL query from json file of GRASP

│ ├── stats_grasp_result.py                #statistics of re-executed query of GRASP

│ ├── transformer_sample_contrast.py          #sentence transformer on the golden answer and answer given by SPARQL

│ └── wikidata_llm_inconsistencies.py          #retrieve all property and compare with ollama

│

├── Compix@Grasp/

│ ├── bottom1000/           #json file from graps of the lowest context score question

│ ├── Finding_Inconsistency/          #main csv file containing the inconsistencies

│ │ ├── sample_contrast_bottom.csv

│ │ └── sample_contrast.csv

│ ├── generated_query/        #query taken from grasp with top1000 dataset

│ ├── generated_query_bottom/      #query taken from grasp with bottom1000 dataset

│ ├── grasp_query_result/          #result from graps json

│ │ ├── compmix_train.json

│ │ ├── compmix_dev.json

│ │ └── compmix_test.json

│ ├── grasp_query_result_bottom/     #same but bottom1000 instead of top1000 dataset

│ ├── top1000/             #json file from graps of the highest context score question

│ ├── wikidata_query_result/      #result from re-run query from graps

│ ├── wikidata_query_result_bottom/    #same but bottom1000 instead of top1000 dataset

│ ├── bottom1000.csv              #questions and answers from bottom1000 

│ └── top1000.csv              #same for top1000 dataset

│

│

└── readme.md

