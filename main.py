import argparse
import sys
from backend import search_contributions

def main():
    parser = argparse.ArgumentParser(description="Find GitHub contribution opportunities using Gemini AI.")
    parser.add_argument("repo", help="Target GitHub repository (e.g. facebook/react)")
    parser.add_argument("idea", help="Contribution idea described in natural language")

    args = parser.parse_args()

    print(f"Searching for opportunities in '{args.repo}' matching idea: '{args.idea}'...\n")
    print("Asking Gemini to generate intelligent GitHub CLI commands...\n")
    
    result = search_contributions(args.repo, args.idea)

    if "error" in result:
        print(f"Error: {result['error']}")
        sys.exit(1)

    data = result["data"]
    results_type = result["type"]

    if results_type == "none" or not data:
        print("No relevant issues or pull requests found.")
        return

    titles = {"issues": "Issues", "pull requests": "Pull Requests"}
    display_type = titles.get(results_type, "Items")

    print(f"Found {len(data)} relevant {display_type}:\n")

    for item in data:
        print(f"#{item.get('number')} - {item.get('title')}")
        print(f"{item.get('url')}\n")

if __name__ == "__main__":
    main()
