# Getting Started Guide

This guide helps you set up the environment to run all the packaging quality analysis notebooks.

## Quick Setup

### 1. Install Dependencies
```bash
# Create and activate a virtual environment (recommended)
python -m venv capstone_env
source capstone_env/bin/activate  # On Mac/Linux
# capstone_env\Scripts\activate   # On Windows

# Install all required packages
pip install -r requirements.txt
```

### 2. Start Analysis
```bash
# Launch Jupyter Notebook
jupyter notebook

# Navigate to the ML folder to start with the notebooks
```

## Notebook Execution Order

For best results, run the notebooks in this sequence:

### Main ML Pipeline:
1. **1. Data cleaning & Integration.ipynb** - Prepares the data
2. **2. Recommendation_Model.ipynb** - Builds packaging recommendations
3. **3. Risk_model.ipynb** - Creates risk prediction model  
4. **4. Cost Model.ipynb** - Develops cost optimization model
5. **5. Model Monitoring.ipynb** - Sets up ongoing model maintenance

### Analysis Notebooks:
- **analysis/recommendation_model/results_analysis.ipynb** - Analyzes recommendation performance
- **analysis/risk_model/result_analysis.ipynb** - Evaluates risk model results
- **analysis/risk_model/strata_analysis.ipynb** - Deep-dive into risk segments

## Troubleshooting

### Common Issues:
- **Import errors**: Make sure you've activated your virtual environment and installed requirements.txt
- **File not found**: Check that you're running notebooks from the correct directory
- **Memory issues**: Close unused notebooks and restart kernel if needed

### Getting Help:
- Check the README.md files in each folder for detailed explanations
- Each notebook contains business-friendly explanations before technical steps
- Look for markdown cells that explain what each section does in plain language

## Project Structure

```
capstone/
├── requirements.txt          # This file - install dependencies
├── SETUP.md                 # This guide
├── ML/                      # Main analysis notebooks
│   ├── README.md           # Detailed guide to ML notebooks  
│   └── analysis/           # Results analysis notebooks
├── data/                   # Data files and preprocessing
└── EDA/                    # Exploratory data analysis
```
