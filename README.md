# Yahoo Finance Stock Data Visualizer 

This repository demonstrates how to programmatically fetch historical stock data on the FAANG stocks using the Yahoo Finance API, process the data using Pandas, and generate plots using Matplotlib. 

It contains two primary implementations: an interactive **Jupyter Notebook** for exploration and a **Python Script** integrated with **GitHub Actions** for automated reporting.

## Repository Contents

| File/Folder | Description |
| :--- | :--- |
| `assignment/problems.ipynb` | **Interactive:** A step-by-step Jupyter Notebook explaining the logic, data fetching, and plotting process. |
| `assignment/faang.py` | **Automated:** A standalone script optimized for command-line execution and CI/CD pipelines. |
| `.github/workflows/faang.yml` | Contains the YAML configuration to run the Python script automatically via GitHub Actions. |
| `requirements.txt` | List of Python dependencies required to run the project. |

## Features

* **Data Extraction:** Fetches real-time and historical market data using `yfinance`.
* **Data Visualization:** Generates trend lines and closing price charts using `matplotlib`.
* **CI/CD Integration:** Demonstrates how to run data science scripts in the cloud using GitHub Actions runners.
* **Artifact Management:** The GitHub Action is configured to save the generated plots as downloadable artifacts.

## 🛠️ Installation & Local Usage

To run this project on your local machine, follow these steps:

### 1. Clone the repository
```bash
git clone [https://github.com/callagg2/computer_infrastructure.git](https://github.com/callagg2/computer_infrastructure.git)
cd your-repo-name

### 2. Set up a virtual environment (Optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

### 3. Install dependencies
```bash
pip install -r requirements.txt

### 4. Run the code
```bash
To use the script
python faang.py

To use the notebook
jupyter notebook aproblems.ipynb


## GitHub Actions Automation

This repository includes a GitHub Actions workflow that automatically runs the python script.

* ** Trigger: The action triggers on [e.g., specific time via cron, or on push to main].
* ** Process: It sets up a Python environment, installs dependencies, executes the script, and saves the resulting graph.
* ** Output: You can view the generated plots in the Actions tab under the "Artifacts" section of the latest build.
