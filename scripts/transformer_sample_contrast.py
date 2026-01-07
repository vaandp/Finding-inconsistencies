import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

# 1. Load a pretrained Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Load the CSV file
csv_path = "Compix@Grasp/Finding_Inconsistency/sample_contrast_bottom.csv"
df = pd.read_csv(csv_path)

# 3. Prepare the data - handle NaN values
df['CompMix_answer_label'] = df['CompMix_answer_label'].fillna('')
df['GRASP_SPARQL_answer'] = df['GRASP_SPARQL_answer'].fillna('')

# 4. Calculate consistency scores for each row
consistency_scores = []

for idx, row in df.iterrows():
    compmix_answer = str(row['CompMix_answer_label'])
    grasp_answer = str(row['GRASP_SPARQL_answer'])
    
    # If both answers are empty, set score to NaN
    if not compmix_answer and not grasp_answer:
        consistency_scores.append(np.nan)
        continue
    
    # If one is empty and the other is not, set score to 0
    if not compmix_answer or not grasp_answer:
        consistency_scores.append(0.0)
        continue
    
    # Calculate embeddings for both answers
    embeddings = model.encode([compmix_answer, grasp_answer])
    
    # Calculate cosine similarity between the two embeddings
    similarity = cos_sim(embeddings[0], embeddings[1])
    
    # Extract the scalar value from the tensor
    score = float(similarity.item())
    consistency_scores.append(score)

# 5. Add the Consistency_score column to the dataframe
df['Consistency_score'] = consistency_scores

# 6. Save the updated CSV
df.to_csv(csv_path, index=False)
print(f"Consistency scores calculated and saved to {csv_path}")
print(f"Total rows processed: {len(df)}")
print(f"Average consistency score: {df['Consistency_score'].mean():.4f}")