# GitHub Contribution Finder (ghfind)

A fast, lightweight developer tool allowing users to input their project idea and a target GitHub repository, relying on Gemini API to intelligently discover relevant GitHub Issues or Pull Requests utilizing GitHub CLI (gh) commands.

## 1. Architecture Overview
This application follows a minimal 3-tier structure, focused completely on local execution:
1. **Frontend Layer**: Streamlit web UI (`app.py`) and Terminal CLI (`main.py`) acting as dual entry points.
2. **AI Logic Layer**: `backend.py` hosts the Gemini API integration using structured JSON output from `google-genai` to smartly translate natural language into context-specific `gh` shell commands.
3. **Command Execution Engine**: An encapsulated function securely interpreting commands, checking against predefined allowed terms (restricting shell-injection risks mapping to `subprocess.run` without `shell=True`), then converting `gh` CLI JSON payloads to parsed Python entities.

## 2. Folder Structure
```
c:\Users\Admin\Desktop\Projects\ghfind\
 │
 ├── requirements.txt         # Required Python packages
 ├── backend.py               # Core Gemini Logic, Execution Engine & Fallback Logic
 ├── main.py                  # Terminal-based Interface
 ├── app.py                   # Streamlit Web Frontend Interface
 ├── setup.bat                # Windows setup & installation batch script
 └── README.md                # This comprehensive documentation file
```

## 3. Dependency List
*   **google-genai**: Official SDK for calling and parsing Gemini requests securely.
*   **pydantic**: Used to construct strictly structured outputs mapped natively into the `google-genai` integration logic. 
*   **streamlit**: Chosen to deliver a rapid, minimal, high-aesthetic web interface ensuring "extremely fast load time" without heavy state management logic.

**(Additionally relying on built-in modules: `subprocess`, `json`, `shlex`, `argparse`, `sys`, `os`)**

## 4. Backend Implementation Code
*File Reference: `backend.py`*
A single lightweight Python module is responsible for initializing the `genai.Client()`, managing the prompt instructions natively, and processing the results. A custom `BaseModel` from `pydantic` dictates output structure.
It defines `generate_gh_commands()`, mapping model outputs gracefully. It sets the temperature to `0.2` to assure command accuracy while retaining inference determinism.

## 5. Gemini Prompt Template
This AI System employs the following structured instruction to generate precise bash parameters:
```text
You are an expert GitHub CLI (gh) command generator.
The user wants to find contribution opportunities in an open source GitHub repository based on their idea.

Given the repository "{repo}" and the user's idea: "{idea}"

Generate the best `gh` commands to search for relevant issues, and a fallback to search for relevant pull requests.
Constraints for the commands:
1. Must be read-only search commands (`gh issue list` or `gh pr list`).
2. Must use `--repo {repo}`
3. Must use `--limit 5`
4. Must use `--state open`
5. Must include appropriate `--search "..."` or `--label "..."` based on the idea.
6. MUST include `--json number,title,url` at the end of the command to ensure the output can be parsed by our execution engine.

Only generate the two commands in the structured JSON output. Do NOT add markdown blocks or code formatting around JSON, return strictly JSON.
```

## 6. Command Execution Layer
*File Reference: `backend.py - execute_gh_command()`*
The command execution restricts string arrays strictly to those initiated via `"gh issue list", "gh pr list", "gh search issues"` enforcing absolute restrictions via `shlex.split(..., posix=True)`. All outputs rely on deterministic stdout byte streams retrieved asynchronously locally allowing maximum speeds without unnecessary intermediary text file generation.
It implements the strict Fallback Logic (Issues > PRs > Message).

## 7. CLI Interface Code
*File Reference: `main.py`*
A lightweight standard python script built with `argparse`. It directly invokes the orchestration engine (`search_contributions`), presenting the user with clean console printing containing ID numbers, Titles, and native console-clickable URL formats.

## 8. Frontend Implementation
*File Reference: `app.py`*
Built with **Streamlit** (per your previous system requirements preferring Python frameworks). It utilizes native spinners during API requests avoiding screen locks, and employs minimal error management handling and success formatting rendering native clickable hyperlinks without raw HTML injection.

## 9. Setup Instructions (Windows)
1. You **must** have the GitHub CLI installed globally. First run:
   > `gh auth login`
2. Configure your API Key as an Environment Variable in CMD or PowerShell:
   > `set GEMINI_API_KEY="AIzaSyYourAPIKeyHere..."`
3. Execute the Setup Script from the project directory:
   > `setup.bat`
4. **Deploy the Streamlit UI**:
   > `streamlit run app.py`
5. **Run Terminal Tool**:
   > `python main.py facebook/react "Update documentation on Hooks"`

## 10. Example Run Demonstration

### CLI Example:
```console
> python main.py cli/cli "help with parsing bugs"
Searching for opportunities in 'cli/cli' matching idea: 'help with parsing bugs'...

Asking Gemini to generate intelligent GitHub CLI commands...

Found 1 relevant Issues:

#8512 - argument parsing issue causing bad command crash
https://github.com/cli/cli/issues/8512
```

### Fallback Example:
```console
> python main.py some/repo "really specific obscure thing"
Searching for opportunities in 'some/repo' matching idea: 'really specific obscure thing'...

Asking Gemini to generate intelligent GitHub CLI commands...

No relevant issues or pull requests found.
```
