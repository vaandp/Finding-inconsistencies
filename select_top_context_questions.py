import argparse
import json
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

def load_json_files(train_path, dev_path, test_path):
    with open(train_path, 'r', encoding='utf-8') as f:
        train_data = json.load(f)
    with open(dev_path, 'r', encoding='utf-8') as f:
        dev_data = json.load(f)
    with open(test_path, 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    return train_data, dev_data, test_data

def count_words(text):
    return len(text.split())

def calculate_question_context_score(question, entities):
    num_entities = len(entities)
    question_length = count_words(question)
    
    score = 0.5 * num_entities + 0.5 * question_length
    
    return score

def analyze_dataset(data, dataset_name="Dataset"):
    """Compute the score for each question"""
    results = []
    
    for item in data:
        question = item.get('question', '')
        entities = item.get('entities', [])
        domain = item.get('domain', 'unknown')
        question_id = item.get('question_id', '')
        
        num_entities = len(entities)
        question_length = count_words(question)
        score = calculate_question_context_score(question, entities)
        
        results.append({
            'question_id': question_id,
            'question': question,
            'domain': domain,
            'num_entities': num_entities,
            'question_length': question_length,
            'context_score': score,
            'raw_item': item
        })
    
    return results

def print_statistics(results, dataset_name="Dataset"):
    scores = [r['context_score'] for r in results]
    
    print(f"\n=== Question Context Score Statistics - {dataset_name} ===")
    print(f"{'Metric':<25} {'Value':<15}")
    print("-" * 40)
    print(f"{'Total questions':<25} {len(scores)}")
    print(f"{'Mean score':<25} {np.mean(scores):.2f}")
    print(f"{'Median score':<25} {np.median(scores):.2f}")
    print(f"{'Min score':<25} {np.min(scores):.2f}")
    print(f"{'Max score':<25} {np.max(scores):.2f}")

def print_domain_statistics(results):
    domain_scores = defaultdict(list)
    
    for r in results:
        domain_scores[r['domain']].append(r['context_score'])
    
    print(f"\n=== Question Context Score by Domain ===")
    print(f"{'Domain':<15} {'Count':<10} {'Mean':<10} {'Median':<10} {'Std':<10}")
    print("-" * 55)
    
    for domain in sorted(domain_scores.keys()):
        scores = domain_scores[domain]
        print(f"{domain.capitalize():<15} {len(scores):<10} {np.mean(scores):<10.2f} {np.median(scores):<10.2f} {np.std(scores):<10.2f}")

def plot_score_distribution(results, title="Question Context Score Distribution"):
    """Create a histogram of the score distribution"""
    scores = [r['context_score'] for r in results]
    
    plt.figure(figsize=(10, 6))
    plt.hist(scores, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    plt.xlabel('Question Context Score', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    
    # Add line for the median and the mean
    mean_score = np.mean(scores)
    median_score = np.median(scores)
    plt.axvline(mean_score, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_score:.2f}')
    plt.axvline(median_score, color='green', linestyle='--', linewidth=2, label=f'Median: {median_score:.2f}')
    
    plt.legend()
    plt.tight_layout()
    
    plt.show()
    plt.close()

def plot_score_by_domain(results):
    """Create a boxplot score per domain"""
    domain_scores = defaultdict(list)
    
    for r in results:
        domain_scores[r['domain']].append(r['context_score'])
    
    domains = sorted(domain_scores.keys())
    scores_by_domain = [domain_scores[d] for d in domains]
    domain_labels = [d.capitalize() for d in domains]
    
    plt.figure(figsize=(12, 6))
    bp = plt.boxplot(scores_by_domain, labels=domain_labels, patch_artist=True)
    
    # Color the boxplot
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
    
    plt.xlabel('Domain', fontsize=12)
    plt.ylabel('Question Context Score', fontsize=12)
    plt.title('Question Context Score Distribution by Domain', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    plt.show()
    plt.close()

def plot_components_scatter(results):
    """Create a scatter plot showing the relationship between the number of entities and the question length."""
    num_entities = [r['num_entities'] for r in results]
    question_lengths = [r['question_length'] for r in results]
    scores = [r['context_score'] for r in results]
    
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(num_entities, question_lengths, c=scores, 
                         cmap='viridis', alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
    
    plt.xlabel('Number of Question Entities', fontsize=12)
    plt.ylabel('Question Length (words)', fontsize=12)
    plt.title('Question Context Score Components', fontsize=14, fontweight='bold')
    plt.colorbar(scatter, label='Context Score')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    plt.show()
    plt.close()


def show_top_bottom_examples(results, n=5):
    """Shows questions with the highest and lowest scores"""
    sorted_results = sorted(results, key=lambda x: x['context_score'], reverse=True)
    
    print(f"\n=== Top {n} Questions with Highest Context Scores ===")
    for i, r in enumerate(sorted_results[:n], 1):
        print(f"\n{i}. Score: {r['context_score']:.2f} (Entities: {r['num_entities']}, Length: {r['question_length']})")
        print(f"   Domain: {r['domain']}")
        print(f"   Question: {r['question']}")

    print(f"\n=== Top {n} Questions with Lowest Context Scores ===")
    for i, r in enumerate(sorted_results[-n:], 1):
        print(f"\n{i}. Score: {r['context_score']:.2f} (Entities: {r['num_entities']}, Length: {r['question_length']})")
        print(f"   Domain: {r['domain']}")
        print(f"   Question: {r['question']}")


def select_top_questions(results, top_k=400):
    """Returns the top_k questions with the best context score"""
    if not results:
        return []

    top_k = max(0, top_k)
    sorted_results = sorted(results, key=lambda x: x['context_score'], reverse=True)
    limited_results = sorted_results[:top_k]
    selected_questions = [r.get('raw_item') for r in limited_results if r.get('raw_item') is not None]

    if len(selected_questions) < len(limited_results):
        print("Some elements no longer contained the raw data and were ignored.")

    return selected_questions


def save_selected_questions(questions, output_path):
    """Saves the selected questions to a JSON file"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open('w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    print(f"\n✓ {len(questions)} questions saved in {output_path}")

def main(train_path, dev_path, test_path, output_path="400_questions.json",
         top_k=400):
    print("=== Question Context Score Analysis ===\n")
    print("Formula: Score = 0.5 × (# entities) + 0.5 × (# words)\n")
    
    print("Chargement des fichiers JSON...")
    train_data, dev_data, test_data = load_json_files(train_path, dev_path, test_path)
    
    print("Calcul des scores...")
    train_results = analyze_dataset(train_data, "Train")
    dev_results = analyze_dataset(dev_data, "Dev")
    test_results = analyze_dataset(test_data, "Test")
    all_results = train_results + dev_results + test_results
    
    print_statistics(train_results, "Train Set")
    print_statistics(dev_results, "Dev Set")
    print_statistics(test_results, "Test Set")
    print_statistics(all_results, "All Data")
    
    print_domain_statistics(all_results)
    
    show_top_bottom_examples(all_results, n=3)
    
    # Select and save the questions in CompMix format
    selected_questions = select_top_questions(all_results, top_k=top_k)
    print(f"\nSelection of the {len(selected_questions)} best questions (among {len(all_results)})")
    save_selected_questions(selected_questions, output_path)
    
    # Create the plot
    print("\nPlotting...")
    plot_score_distribution(
        all_results,
        "Question Context Score Distribution - All Data",
    )
    
    plot_score_by_domain(
        all_results
    )
    
    plot_components_scatter(
        all_results
    )
    
    print("\nEnd of analysis")

def parse_arguments():
    """Constructs and returns command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Analyzes context scores and extracts the best questions."
    )
    parser.add_argument("--train-path", default="train_set.json", dest="train_path",
                        help="Path to the train json")
    parser.add_argument("--dev-path", default="dev_set.json", dest="dev_path",
                        help="Path to the dev json")
    parser.add_argument("--test-path", default="test_set.json", dest="test_path",
                        help="Path to the test json")
    parser.add_argument("--output-path", default="400_questions.json", dest="output_path",
                        help="Path to the file json to save the 400 questions")
    parser.add_argument("--top-k", type=int, default=400,
                        help="Number of question to select")
    parser.add_argument("--show-plots", action="store_true",
                        help="print the graph")
    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    main(
        train_path=args.train_path,
        dev_path=args.dev_path,
        test_path=args.test_path,
        output_path=args.output_path,
        top_k=args.top_k,
    )