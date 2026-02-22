@echo off
echo Setting up virtual environment...
python -m venv venv
call venv\Scripts\activate.bat
echo Installing dependencies...
pip install -r requirements.txt
echo Setup complete.
echo.
echo Please ensure that your 'GEMINI_API_KEY' environment variable is set.
echo.
echo Run CLI: python main.py ^<repo^> "^<idea^>"
echo Run Web UI: streamlit run app.py
