#!/usr/bin/env python3.12
import json
import math
from statistics import median

import matplotlib.pyplot as plt

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

def analyze_dataset(data):
    stats = {
        'num_questions': len(data),
        'question_lengths': [],
        'num_question_entities': [],
        'answer_lengths': [],
        'num_answers': [],
        'all_entities': set(),
        'domains': set()
    }
    
    for item in data:
        # lenght of the question
        question = item.get('question', '')
        stats['question_lengths'].append(count_words(question))
        
        # Number of entity in the question
        entities = item.get('entities', [])
        stats['num_question_entities'].append(len(entities))
        
        # Collect ID of the entities in the question
        for entity in entities:
            stats['all_entities'].add(entity['id'])
        
        # Length of the answer
        answer_text = item.get('answer_text', '')
        stats['answer_lengths'].append(count_words(answer_text))
        
        # Number of answer
        answers = item.get('answers', [])
        stats['num_answers'].append(len(answers))
        
        # Collect ID of the entities from the answer
        for answer in answers:
            stats['all_entities'].add(answer['id'])
        
        # Collect the domains
        domain = item.get('domain', '')
        stats['domains'].add(domain)
    
    return stats

def merge_stats(train_stats, dev_stats, test_stats):
    merged = {
        'question_lengths': train_stats['question_lengths'] + dev_stats['question_lengths'] + test_stats['question_lengths'],
        'num_question_entities': train_stats['num_question_entities'] + dev_stats['num_question_entities'] + test_stats['num_question_entities'],
        'answer_lengths': train_stats['answer_lengths'] + dev_stats['answer_lengths'] + test_stats['answer_lengths'],
        'num_answers': train_stats['num_answers'] + dev_stats['num_answers'] + test_stats['num_answers'],
        'all_entities': train_stats['all_entities'].union(dev_stats['all_entities']).union(test_stats['all_entities']),
        'all_domains': train_stats['domains'].union(dev_stats['domains']).union(test_stats['domains']),
        'num_questions_train': train_stats['num_questions'],
        'num_questions_dev': dev_stats['num_questions'],
        'num_questions_test': test_stats['num_questions']
    }
    return merged

def calculate_statistics(merged_stats):
    results = {}
    
    # Domains
    domains_str = ", ".join(sorted(merged_stats['all_domains']))
    results['Domains'] = domains_str
    
    # Total number of question
    total_questions = merged_stats['num_questions_train'] + merged_stats['num_questions_dev'] + merged_stats['num_questions_test']
    results['Questions'] = f"{total_questions:,} (train: {merged_stats['num_questions_train']:,}, dev: {merged_stats['num_questions_dev']:,}, test: {merged_stats['num_questions_test']:,})"
    
    # Average length of a question
    q_lengths = merged_stats['question_lengths']
    results['Avg. question length'] = f"{sum(q_lengths)/len(q_lengths):.2f} words (min={min(q_lengths)}, median={int(median(q_lengths))}, max={max(q_lengths)})"
    
    # Average number of entities in a question
    q_entities = merged_stats['num_question_entities']
    results['Avg. no. of question entities'] = f"{sum(q_entities)/len(q_entities):.2f} (min={min(q_entities)}, median={int(median(q_entities))}, max={max(q_entities)})"
    
    # Average length of an answer
    a_lengths = merged_stats['answer_lengths']
    results['Avg. answer length (text)'] = f"{sum(a_lengths)/len(a_lengths):.2f} words (min={min(a_lengths)}, median={int(median(a_lengths))}, max={max(a_lengths)})"
    
    # Average number of answer per question
    n_answers = merged_stats['num_answers']
    results['Avg. no. of answers'] = f"{sum(n_answers)/len(n_answers):.2f} (min={min(n_answers)}, median={int(median(n_answers))}, max={max(n_answers)})"
    
    # Total number of entities
    results['Entities covered'] = f"{len(merged_stats['all_entities']):,}"
    
    return results

def plot_distributions(merged_stats):
    metrics = [
        ("Lenght of the questions", merged_stats['question_lengths'], "Words"),
        ("Number of entities per question", merged_stats['num_question_entities'], "Number of entities"),
        ("Length of the answer", merged_stats['answer_lengths'], "Words"),
        ("Number of answer", merged_stats['num_answers'], "Number of items"),
    ]
    
    cols = 2
    rows = math.ceil(len(metrics) / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(6 * cols, 4 * rows))
    axes = axes.flatten()
    
    for ax, (title, values, xlabel) in zip(axes, metrics):
        bins = min(50, max(10, len(set(values))))
        ax.hist(values, bins=bins, color="#4C72B0", edgecolor="black", alpha=0.8)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Number of questions")
        ax.grid(alpha=0.2, linestyle="--")
    
    # Masquer les axes inutilisés si le nombre de graphiques est impair
    for ax in axes[len(metrics):]:
        ax.axis('off')
    
    fig.suptitle("CompMix statistics", fontsize=16)
    fig.tight_layout()
    plt.show()

def main(train_path, dev_path, test_path):
    print("=== Analysis of CompMix ===\n")
    
    print("Loading JSON file...")
    train_data, dev_data, test_data = load_json_files(train_path, dev_path, test_path)
    
    print("Analysis of the dataset...")
    train_stats = analyze_dataset(train_data)
    dev_stats = analyze_dataset(dev_data)
    test_stats = analyze_dataset(test_data)
    
    merged_stats = merge_stats(train_stats, dev_stats, test_stats)
    
    results = calculate_statistics(merged_stats)
    
    print("\n=== Results ===\n")
    for key, value in results.items():
        print(f"{key:30s} {value}")
    
    print("\nPrinting the graph...")
    plot_distributions(merged_stats)


if __name__ == "__main__":
    train_path = "train_set.json"
    dev_path = "dev_set.json"
    test_path = "test_set.json"
    
    main(train_path, dev_path, test_path)