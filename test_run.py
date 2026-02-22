import os
from backend import generate_gh_commands, execute_gh_command, search_contributions

def run_test():
    repo = "google-gemini/gemini-cli"
    idea = "implementing visualize feature where user can tell gemini to use visualize tool so gemini can show visualization easily"
    
    print(f"Testing with repo: {repo}")
    print(f"Testing with idea: {idea}")
    
    print("\n--- Testing generate_gh_commands ---")
    try:
        commands = generate_gh_commands(repo, idea)
        print("Generated Commands Object:")
        print(commands.model_dump_json(indent=2))
        
        print("\n--- Testing execute_gh_command (Primary) ---")
        primary_result = execute_gh_command(commands.primary_command)
        print(f"Primary Result count: {len(primary_result)}")
        if primary_result:
            print("First item metadata:", primary_result[0])
        else:
            print("\n--- Testing execute_gh_command (Fallback) ---")
            fallback_result = execute_gh_command(commands.fallback_command)
            print(f"Fallback Result count: {len(fallback_result)}")
            if fallback_result:
                print("First item metadata:", fallback_result[0])
            
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    if not os.environ.get("GEMINI_API_KEY"):
        print("WARNING: GEMINI_API_KEY is not set. The API call will fail.")
        
    run_test()
