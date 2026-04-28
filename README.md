# Liv Insights

Liv Insights is a Streamlit decision-support app that helps users turn uploaded CSV or Excel datasets into simple insights, quality checks, charts, recommendations, and exportable summaries.

The app does not require an OpenAI API key or any paid external service. All insights are generated locally from the uploaded dataset using pandas, NumPy, Plotly, and Streamlit.

## Features

- Upload CSV or XLSX files
- Preview uploaded data
- Keep uploaded data available across sections with Streamlit session state
- Detect column types automatically:
  - Numeric
  - Categorical
  - Date/time
  - Boolean
- Run data health checks:
  - Missing values
  - Duplicate rows
  - Invalid or inconsistent values where detectable
  - IQR outliers
- Generate a Data Quality Score from 0 to 100
- Show numeric and category summaries
- Generate charts with Plotly:
  - Histogram
  - Bar chart
  - Scatter plot
  - Line chart
  - Correlation heatmap
- Run correlation analysis and Top Drivers analysis
- Ask natural-language questions about the uploaded dataset with Ask Liv Insights
- Run simple linear regression from questions such as "Predict target using predictor"
- Explain the dataset in plain English without an external API
- Generate recommended next actions
- Generate suggested questions
- Support analysis modes:
  - General Analytics
  - Business Analytics
  - Customer Insights
  - Financial Data
  - Marketing Analysis
- Export:
  - Cleaned dataset as CSV
  - Insights summary as Markdown

## How To Run Locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the app:

```bash
streamlit run app.py
```

3. Upload a `.csv` or `.xlsx` file in the sidebar.

## Deployment Note

This project is ready for Streamlit Community Cloud.

For deployment:

1. Push `app.py`, `requirements.txt`, and `README.md` to a GitHub repository.
2. In Streamlit Community Cloud, create a new app from that repository.
3. Set the main file path to:

```text
app.py
```

The app uses only uploaded CSV/XLSX files and does not depend on local file paths, local secrets, or paid APIs.
