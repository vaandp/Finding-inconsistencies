import json
import csv

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def extract_question_and_entities(item):
    """
    Extract the question and the entity IDs from an item
    
    Returns:
        str: question followed by the entity IDs separated by spaces
    """
    question = item.get('question', '').strip()
    entities = item.get('entities', [])
    
    # Extract the entity IDs
    entity_ids = []
    for entity in entities:
        if isinstance(entity, dict) and 'id' in entity:
            entity_ids.append(entity['id'])
    
    # Build the line: question + entity IDs
    line = question
    if entity_ids:
        line += ' ' + ' '.join(entity_ids)
    
    return line

def generate_csv(input_path, output_path):
    """
        input_path: path of the input JSON file
        output_path: path of the output CSV file
    """
    print(f"Loading {input_path}...")
    data = load_json_file(input_path)
    
    print(f"Number of questions found: {len(data)}")
    
    # Write in the CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write the header
        writer.writerow(['question'])
        
        # Write each question with its entity IDs
        for item in data:
            question_line = extract_question_and_entities(item)
            writer.writerow([question_line])
    
    print(f"CSV generated successfully: {output_path}")
    print(f"Number of lines: {len(data)}")

def main():
    print("=== Extraction of questions to CSV ===\n")
    
    # Paths of the files
    input_path = "400_questions.json"  # Your file with 400 questions
    output_path = "400_questions.csv"
    
    # Generate the CSV
    generate_csv(input_path, output_path)


if __name__ == "__main__":
    main()