from __future__ import annotations

import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
GRASP_DIR = BASE / "Compix@Grasp/grasp_query_result"

# different patterns
PATTERN_WITH_PARENTHESES = re.compile(r".+\([^:)]+:[^)]+\)")
PATTERN_NO_ROWS = re.compile(r"Got no rows and \d+ columns?", re.IGNORECASE)
PATTERN_ERROR = re.compile(r"Error executing SPARQL query over wikidata:", re.IGNORECASE)
PATTERN_SPARQL_EXECUTION_FAILED = re.compile(r"SPARQL execution failed", re.IGNORECASE)


def analyze_file(file_path: Path) -> str:
    """analyze a file and return its type"""
    try:
        content = file_path.read_text(encoding="utf-8").strip()
        if not content:
            return "empty"
        
        # check the specific patterns first
        if PATTERN_SPARQL_EXECUTION_FAILED.search(content):
            return "sparql_execution_failed"
        
        if PATTERN_ERROR.search(content):
            return "error"
        
        if PATTERN_NO_ROWS.fullmatch(content):
            return "no_rows"
        
        # check if the content contains a pattern with parentheses
        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            if PATTERN_WITH_PARENTHESES.fullmatch(line):
                return "with_parentheses"
            # if we find a line with parentheses but not in the exact format, we still count it
            if "(" in line and ":" in line and ")" in line:
                return "with_parentheses"
        
        # if no match, it is another format
        return "other"
    
    except Exception as e:
        return f"error_reading: {str(e)}"


def main():
    if not GRASP_DIR.exists():
        print(f"The directory {GRASP_DIR} does not exist.")
        return
    
    stats = {
        "with_parentheses": [],
        "no_rows": [],
        "error": [],
        "sparql_execution_failed": [],
        "other": [],
        "empty": [],
        "error_reading": [],
    }
    
    total_files = 0
    
    # loop through all .txt files
    for txt_file in sorted(GRASP_DIR.glob("*.txt")):
        total_files += 1
        file_type = analyze_file(txt_file)
        
        if file_type.startswith("error_reading"):
            stats["error_reading"].append(txt_file.name)
        else:
            stats[file_type].append(txt_file.name)
    
    # print the statistics
    print("=" * 60)
    print("STATISTICS OF GRASP RESULTS")
    print("=" * 60)
    print(f"\nTotal files analyzed : {total_files}\n")
    
    print(f"Format with parentheses (.... (..:...)) : {len(stats['with_parentheses'])}")
    if stats['with_parentheses']:
        print(f"  Percentage : {len(stats['with_parentheses']) / total_files * 100:.2f}%")
        print(f"  Examples : {', '.join(stats['with_parentheses'][:5])}")
        if len(stats['with_parentheses']) > 5:
            print(f"  ... and {len(stats['with_parentheses']) - 5} others")
    
    print(f"\nFormat 'Got no rows and .. columns' : {len(stats['no_rows'])}")
    if stats['no_rows']:
        print(f"  Percentage : {len(stats['no_rows']) / total_files * 100:.2f}%")
        print(f"  Examples : {', '.join(stats['no_rows'][:5])}")
        if len(stats['no_rows']) > 5:
            print(f"  ... and {len(stats['no_rows']) - 5} others")
    
    print(f"\nFormat 'Error executing SPARQL query' : {len(stats['error'])}")
    if stats['error']:
        print(f"  Percentage : {len(stats['error']) / total_files * 100:.2f}%")
        print(f"  Examples : {', '.join(stats['error'][:5])}")
        if len(stats['error']) > 5:
            print(f"  ... and {len(stats['error']) - 5} others")
    
    print(f"\nFormat 'SPARQL execution failed' : {len(stats['sparql_execution_failed'])}")
    if stats['sparql_execution_failed']:
        print(f"  Percentage : {len(stats['sparql_execution_failed']) / total_files * 100:.2f}%")
        print(f"  Examples : {', '.join(stats['sparql_execution_failed'][:5])}")
        if len(stats['sparql_execution_failed']) > 5:
            print(f"  ... and {len(stats['sparql_execution_failed']) - 5} others")
    
    print(f"\nOther formats : {len(stats['other'])}")
    if stats['other']:
        print(f"  Percentage : {len(stats['other']) / total_files * 100:.2f}%")
        print(f"  Examples : {', '.join(stats['other'])}")
        #if len(stats['other']) > 5:
         #   print(f"  ... and {len(stats['other']) - 5} others")
    
    print(f"\nEmpty files : {len(stats['empty'])}")
    if stats['empty']:
        print(f"  Percentage : {len(stats['empty']) / total_files * 100:.2f}%")
        print(f"  Examples : {', '.join(stats['empty'][:5])}")
        if len(stats['empty']) > 5:
            print(f"  ... and {len(stats['empty']) - 5} others")
    
    if stats['error_reading']:
        print(f"\nReading errors : {len(stats['error_reading'])}")
        print(f"  Files : {', '.join(stats['error_reading'][:10])}")
    
    print("\n" + "=" * 60)
    
    # check if the total number of categorized files is equal to the total number of files
    total_categorized = (
        len(stats['with_parentheses']) +
        len(stats['no_rows']) +
        len(stats['error']) +
        len(stats['sparql_execution_failed']) +
        len(stats['other']) +
        len(stats['empty']) +
        len(stats['error_reading'])
    )
    if total_categorized != total_files:
        print(f"Warning : {total_files - total_categorized} files not categorized")


if __name__ == "__main__":
    main()
