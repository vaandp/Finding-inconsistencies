import json
import matplotlib.pyplot as plt
from collections import Counter

def load_json_files(train_path, dev_path, test_path):
    with open(train_path, 'r', encoding='utf-8') as f:
        train_data = json.load(f)
    with open(dev_path, 'r', encoding='utf-8') as f:
        dev_data = json.load(f)
    with open(test_path, 'r', encoding='utf-8') as f:
        test_data = json.load(f)
    
    return train_data, dev_data, test_data

def extract_domains(data):
    domains = []
    for item in data:
        domain = item.get('domain', 'Unknown')
        domains.append(domain)
    return domains

def plot_domain_distribution(domain_counts, title="Domain Distribution", save_path=None):
    """Create pie chart of the distribution of each domain"""
    labels = []
    sizes = []
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
    
    domain_name_map = {
        'books': 'Books',
        'movies': 'Movies',
        'music': 'Music',
        'tvseries': 'TV Series',
        'soccer': 'Soccer'
    }
    
    for domain, count in sorted(domain_counts.items()):
        display_name = domain_name_map.get(domain, domain.capitalize())
        labels.append(f"{display_name}\n({count})")
        sizes.append(count)
    
    # Create pie chart
    fig, ax = plt.subplots(figsize=(10, 8))
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels, 
        colors=colors[:len(labels)],
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 11}
    )
    
    # Appearance
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(12)
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    ax.axis('equal')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"File saved in: {save_path}")
    
    plt.show()

def print_domain_statistics(domain_counts, dataset_name="Dataset"):
    total = sum(domain_counts.values())
    
    print(f"\n=== Domains Distribution - {dataset_name} ===")
    print(f"{'Domain':<15} {'Count':<10} {'Percentage':<12}")
    print("-" * 40)
    
    for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total) * 100
        print(f"{domain.capitalize():<15} {count:<10} {percentage:>6.2f}%")
    
    print("-" * 40)
    print(f"{'Total':<15} {total:<10} {100.0:>6.2f}%")

def main(train_path, dev_path, test_path):
    print("=== Analysis of the distribution of each domains ===\n")
    
    print("Loading JSON file...")
    train_data, dev_data, test_data = load_json_files(train_path, dev_path, test_path)
    
    train_domains = extract_domains(train_data)
    dev_domains = extract_domains(dev_data)
    test_domains = extract_domains(test_data)
    all_domains = train_domains + dev_domains + test_domains
    
    train_counts = Counter(train_domains)
    dev_counts = Counter(dev_domains)
    test_counts = Counter(test_domains)
    all_counts = Counter(all_domains)
    
    #print statistics
    print_domain_statistics(train_counts, "Train Set")
    print_domain_statistics(dev_counts, "Dev Set")
    print_domain_statistics(test_counts, "Test Set")
    print_domain_statistics(all_counts, "All Data")
    
    print("\nCreation of the chart...")
    
    # Pie chart
    plot_domain_distribution(
        all_counts, 
        title="Domain Distribution - CompMix Benchmark (All Data)"
    )
    
    create_subplots(train_counts, dev_counts, test_counts)

def create_subplots(train_counts, dev_counts, test_counts):
    """Create a pie chart for train/dev/test"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
    
    domain_name_map = {
        'books': 'Books',
        'movies': 'Movies',
        'music': 'Music',
        'tvseries': 'TV Series',
        'soccer': 'Soccer'
    }
    
    datasets = [
        (train_counts, "Train Set", axes[0]),
        (dev_counts, "Dev Set", axes[1]),
        (test_counts, "Test Set", axes[2])
    ]
    
    for counts, title, ax in datasets:
        labels = [domain_name_map.get(d, d.capitalize()) for d in sorted(counts.keys())]
        sizes = [counts[d] for d in sorted(counts.keys())]
        
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors[:len(labels)],
            autopct='%1.1f%%',
            startangle=90
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.axis('equal')
    
    plt.suptitle("Domain Distribution by Dataset Split", fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    train_path = "train_set.json"
    dev_path = "dev_set.json"
    test_path = "test_set.json"
    
    main(train_path, dev_path, test_path)