import subprocess

# Run FastAPI
subprocess.Popen(["uvicorn", "main:app", "--reload"])

# Run Streamlit
subprocess.Popen(["streamlit", "run", "app.py"])
