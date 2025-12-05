
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

## Files and Directories

### CSV Files
- **top1000.csv**： 1,000 questions with the **highest** Question Context Scores  
- **bottom1000.csv**： 1,000 questions with the **lowest** Question Context Scores

### GRASP Outputs
- **top1000/**： GRASP output for each question in `top1000.csv`  
- **bottom1000/**： GRASP output for each question in `bottom1000.csv`

---

## Script
`run.py`: Script to generate GRASP SPARQL output.

