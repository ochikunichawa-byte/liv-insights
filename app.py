import html
import warnings

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Liv Insights",
    layout="wide",
)


THEME_COLOR = "#1f7a8c"
ACCENT_COLOR = "#f2a541"
INK_COLOR = "#16324f"
SOFT_BG = "#f5f8fb"
NAV_ITEMS = [
    ("Upload Data", "📁"),
    ("Data Health", "🩺"),
    ("Insights", "💡"),
    ("Explain My Data", "📝"),
    ("Visualizations", "📊"),
    ("Recommended Actions", "✅"),
    ("Suggested Questions", "❓"),
]
ANALYSIS_MODES = [
    "General Analytics",
    "Business Analytics",
    "Customer Insights",
    "Financial Data",
    "Marketing Analysis",
]


def apply_theme():
    """Add simple branding and a clean visual theme."""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: {SOFT_BG};
        }}
        section[data-testid="stSidebar"] {{
            background: #ffffff;
            border-right: 1px solid #dfe7ef;
        }}
        .top-banner {{
            background: linear-gradient(135deg, {INK_COLOR}, {THEME_COLOR});
            border-radius: 8px;
            padding: 24px 28px;
            margin-bottom: 22px;
            color: white;
            box-shadow: 0 8px 22px rgba(22, 50, 79, 0.16);
        }}
        .brand-row {{
            display: flex;
            gap: 14px;
            align-items: center;
        }}
        .logo-mark {{
            width: 46px;
            height: 46px;
            border-radius: 8px;
            display: grid;
            place-items: center;
            background: {ACCENT_COLOR};
            color: {INK_COLOR};
            font-weight: 800;
            font-size: 19px;
        }}
        .top-banner h1 {{
            margin: 0;
            font-size: 34px;
            letter-spacing: 0;
        }}
        .top-banner p {{
            margin: 4px 0 0 0;
            color: #eaf4f7;
            font-size: 16px;
        }}
        .insight-card {{
            background: #ffffff;
            border: 1px solid #dfe7ef;
            border-left: 5px solid {THEME_COLOR};
            border-radius: 8px;
            padding: 15px 16px;
            margin: 10px 0;
            box-shadow: 0 4px 12px rgba(22, 50, 79, 0.06);
        }}
        .insight-card strong {{
            color: {INK_COLOR};
        }}
        .small-muted {{
            color: #222222;
            font-size: 15px;
            line-height: 1.45;
        }}
        div[data-testid="stMetric"] {{
            background: #ffffff;
            border: 1px solid #dfe7ef;
            border-radius: 8px;
            padding: 12px 14px;
            box-shadow: 0 4px 12px rgba(22, 50, 79, 0.06);
        }}
        div[data-testid="stMetric"] label,
        div[data-testid="stMetricLabel"],
        div[data-testid="stMetricLabel"] p {{
            color: #222222;
            font-weight: 700;
            font-size: 15px;
        }}
        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] div {{
            color: #111111;
            font-weight: 800;
            font-size: 30px;
            line-height: 1.15;
        }}
        div[data-testid="stMetricDelta"] {{
            color: #222222;
        }}
        section[data-testid="stSidebar"] div[data-testid="stButton"] > button {{
            width: 100%;
            justify-content: flex-start;
            border-radius: 8px;
            border: 1px solid #dfe7ef;
            background: #ffffff;
            color: {INK_COLOR};
            min-height: 42px;
            font-weight: 600;
        }}
        .nav-active {{
            background: {THEME_COLOR};
            color: #ffffff;
            border-radius: 8px;
            padding: 11px 14px;
            margin: 8px 0;
            font-weight: 800;
            box-shadow: 0 5px 14px rgba(31, 122, 140, 0.25);
        }}
        .health-good {{
            background: #eaf7ef;
            color: #17633a;
            border: 1px solid #b9e4c9;
            border-radius: 8px;
            padding: 14px 16px;
            font-weight: 700;
        }}
        .health-warning {{
            background: #fff6df;
            color: #7a4f00;
            border: 1px solid #f2d48a;
            border-radius: 8px;
            padding: 14px 16px;
            font-weight: 700;
        }}
        .chart-choice {{
            color: {INK_COLOR};
            font-weight: 700;
            margin-top: 8px;
        }}
        div[data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        button[data-baseweb="tab"] {{
            color: #111111;
            background: #ffffff;
            border: 1px solid #cbd8e3;
            border-radius: 8px;
            padding: 8px 14px;
            font-weight: 800;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            color: #ffffff;
            background: {THEME_COLOR};
            border-color: {THEME_COLOR};
        }}
        div[data-testid="stSegmentedControl"] label,
        div[data-testid="stSegmentedControl"] p,
        div[data-testid="stSegmentedControl"] span {{
            color: #111111;
            font-weight: 800;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_banner():
    """Render the branded top banner."""
    st.markdown(
        """
        <div class="top-banner">
            <div class="brand-row">
                <div class="logo-mark">LI</div>
                <div>
                    <h1>Liv Insights</h1>
                    <p>Turn your data into simple insights</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def insight_card(title, body):
    """Render a friendly plain-English insight card."""
    safe_title = html.escape(str(title))
    safe_body = html.escape(str(body))
    st.markdown(
        f"""
        <div class="insight-card">
            <strong>{safe_title}</strong>
            <div class="small-muted">{safe_body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def read_uploaded_file(uploaded_file):
    """Read a CSV or Excel file into a pandas DataFrame."""
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):
        return pd.read_csv(uploaded_file)

    if file_name.endswith(".xlsx"):
        return pd.read_excel(uploaded_file, engine="openpyxl")

    raise ValueError("Please upload a CSV or XLSX file.")


def try_parse_datetime(series):
    """Return a datetime version of a column when enough values can be parsed."""
    if pd.api.types.is_datetime64_any_dtype(series):
        return series

    if pd.api.types.is_numeric_dtype(series) or pd.api.types.is_bool_dtype(series):
        return None

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        parsed = pd.to_datetime(series, errors="coerce")
    non_empty = series.dropna()

    if len(non_empty) == 0:
        return None

    parse_rate = parsed.notna().sum() / len(non_empty)
    return parsed if parse_rate >= 0.8 else None


def detect_column_types(df):
    """Classify each column as numeric, categorical, date/time, boolean, or unknown."""
    detected = {
        "Numeric": [],
        "Categorical": [],
        "Date/Time": [],
        "Boolean": [],
        "Unknown": [],
    }
    date_versions = {}

    for column in df.columns:
        series = df[column]

        if pd.api.types.is_bool_dtype(series):
            detected["Boolean"].append(column)
            continue

        datetime_series = try_parse_datetime(series)
        if datetime_series is not None:
            detected["Date/Time"].append(column)
            date_versions[column] = datetime_series
            continue

        numeric_series = pd.to_numeric(series, errors="coerce")
        non_empty = series.dropna()
        numeric_rate = numeric_series.notna().sum() / len(non_empty) if len(non_empty) else 0

        if pd.api.types.is_numeric_dtype(series) or numeric_rate >= 0.9:
            detected["Numeric"].append(column)
        elif series.nunique(dropna=True) > 0:
            detected["Categorical"].append(column)
        else:
            detected["Unknown"].append(column)

    return detected, date_versions


def numeric_dataframe(df, numeric_columns):
    """Return numeric columns converted to numbers."""
    if not numeric_columns:
        return pd.DataFrame(index=df.index)
    return df[numeric_columns].apply(pd.to_numeric, errors="coerce")


def find_invalid_type_values(df, detected_types, date_versions):
    """Find values that do not fit the detected column type."""
    issues = []

    for column, invalid_count in invalid_type_counts(df, detected_types, date_versions).items():
        if invalid_count > 0:
            if column in detected_types["Numeric"]:
                issues.append(f"{invalid_count} value(s) in {column} do not look like numbers")
            else:
                issues.append(f"{invalid_count} value(s) in {column} do not look like dates")

    return issues


def invalid_type_counts(df, detected_types, date_versions):
    """Count values that do not match detected numeric or date/time types."""
    counts = {}

    for column in detected_types["Numeric"]:
        invalid_count = pd.to_numeric(df[column], errors="coerce").isna().sum() - df[column].isna().sum()
        counts[column] = int(max(invalid_count, 0))

    for column in detected_types["Date/Time"]:
        parsed = date_versions.get(column, pd.to_datetime(df[column], errors="coerce"))
        invalid_count = parsed.isna().sum() - df[column].isna().sum()
        counts[column] = int(max(invalid_count, 0))

    return counts


def build_health_issues(df, detected_types, date_versions):
    """Create plain-English data quality messages."""
    issues = {
        "Missing values": [],
        "Duplicate rows": [],
        "Data type issues": [],
    }

    for column in df.columns:
        missing_count = int(df[column].isna().sum())
        if missing_count > 0:
            issues["Missing values"].append(f"{missing_count} missing value(s) in {column}")

    duplicate_count = int(df.duplicated().sum())
    if duplicate_count > 0:
        issues["Duplicate rows"].append(f"{duplicate_count} duplicate row(s) found")

    issues["Data type issues"].extend(find_invalid_type_values(df, detected_types, date_versions))
    return issues


def has_health_issues(health_issues):
    """Return True when any health issue group has messages."""
    return any(messages for messages in health_issues.values())


def data_quality_score(df, detected_types, date_versions):
    """Score dataset quality from 0 to 100 using simple, explainable penalties."""
    total_cells = max(df.shape[0] * df.shape[1], 1)
    missing_values = int(df.isna().sum().sum())
    duplicate_rows = int(df.duplicated().sum())
    invalid_values = sum(invalid_type_counts(df, detected_types, date_versions).values())
    unknown_columns = len(detected_types["Unknown"])

    missing_rate = missing_values / total_cells
    duplicate_rate = duplicate_rows / max(df.shape[0], 1)
    invalid_rate = invalid_values / total_cells
    unknown_column_rate = unknown_columns / max(df.shape[1], 1)

    missing_impact = min(round(missing_rate * 35), 35)
    duplicate_impact = min(round(duplicate_rate * 25), 25)
    type_impact = min(round(invalid_rate * 25), 25)
    usability_impact = min(round(unknown_column_rate * 15), 15)
    score = max(0, 100 - missing_impact - duplicate_impact - type_impact - usability_impact)

    if score >= 90:
        explanation = "This means the file is mostly clean and ready for analysis."
    elif score >= 75:
        explanation = "This means the file is usable, but a few checks are worth reviewing first."
    elif score >= 60:
        explanation = "This means the file can be analyzed, but quality issues may affect confidence."
    else:
        explanation = "This means the file needs cleanup before you rely on the results."

    return {
        "score": int(score),
        "explanation": explanation,
        "missing_impact": int(missing_impact),
        "duplicate_impact": int(duplicate_impact),
        "type_impact": int(type_impact),
        "usability_impact": int(usability_impact),
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "invalid_values": int(invalid_values),
    }


def detect_outliers_iqr(df, numeric_columns):
    """Detect numeric outliers with the interquartile range method."""
    rows = []
    numeric_df = numeric_dataframe(df, numeric_columns)

    for column in numeric_df.columns:
        values = numeric_df[column].dropna()
        if len(values) < 4:
            continue

        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        if iqr == 0:
            continue

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outlier_count = int(((values < lower_bound) | (values > upper_bound)).sum())

        rows.append(
            {
                "Column": column,
                "Outliers": outlier_count,
                "Lower Bound": round(lower_bound, 2),
                "Upper Bound": round(upper_bound, 2),
                "Percent of Values": round((outlier_count / len(values)) * 100, 2),
            }
        )

    return pd.DataFrame(rows)


def numeric_summary(df, numeric_columns):
    """Create summary statistics for numeric columns."""
    numeric_df = numeric_dataframe(df, numeric_columns)
    if numeric_df.empty:
        return pd.DataFrame()
    return numeric_df.agg(["mean", "min", "max", "std"]).round(2).T


def categorical_summary(df, categorical_columns):
    """Create top-value summaries for categorical columns."""
    rows = []

    for column in categorical_columns:
        top_values = df[column].value_counts(dropna=True).head(5)
        for value, count in top_values.items():
            rows.append(
                {
                    "Column": column,
                    "Value": str(value),
                    "Count": int(count),
                }
            )

    return pd.DataFrame(rows)


def correlation_matrix(df, numeric_columns):
    """Calculate correlations for numeric columns."""
    numeric_df = numeric_dataframe(df, numeric_columns)
    if numeric_df.shape[1] < 2:
        return pd.DataFrame()
    return numeric_df.corr().round(3)


def strongest_correlations(corr):
    """Return the strongest positive and negative correlation pairs."""
    if corr.empty:
        return None, None

    pairs = []
    columns = list(corr.columns)

    for index, left_column in enumerate(columns):
        for right_column in columns[index + 1 :]:
            value = corr.loc[left_column, right_column]
            if pd.notna(value):
                pairs.append((left_column, right_column, value))

    if not pairs:
        return None, None

    positive_pairs = [pair for pair in pairs if pair[2] > 0]
    negative_pairs = [pair for pair in pairs if pair[2] < 0]
    strongest_positive = max(positive_pairs, key=lambda pair: pair[2]) if positive_pairs else None
    strongest_negative = min(negative_pairs, key=lambda pair: pair[2]) if negative_pairs else None

    return strongest_positive, strongest_negative


def target_drivers(corr, target_column):
    """Find numeric columns most related to a selected target column."""
    if corr.empty or target_column not in corr.columns:
        return pd.DataFrame()

    drivers = corr[target_column].drop(labels=[target_column], errors="ignore").dropna()
    if drivers.empty:
        return pd.DataFrame()

    result = drivers.abs().sort_values(ascending=False).reset_index()
    result.columns = ["Column", "Relationship Strength"]
    result["Correlation"] = result["Column"].map(drivers).round(3)
    result["Direction"] = np.where(result["Correlation"] >= 0, "Positive", "Negative")
    return result.head(5)


def driver_groups(corr, target_column):
    """Split target drivers into positive and negative relationships."""
    drivers = target_drivers(corr, target_column)
    if drivers.empty:
        return pd.DataFrame(), pd.DataFrame()

    positive = drivers[drivers["Correlation"] > 0].sort_values("Correlation", ascending=False)
    negative = drivers[drivers["Correlation"] < 0].sort_values("Correlation", ascending=True)
    return positive, negative


def mode_context(mode):
    """Return wording that adapts insights to the selected analysis mode."""
    contexts = {
        "Business Analytics": {
            "lens": "business performance, operations, trends, efficiency, and decision-making",
            "recommendation": "Use these patterns to prioritize operational improvements and clearer decisions.",
        },
        "Customer Insights": {
            "lens": "customers, retention, segmentation, satisfaction, churn, and behavior",
            "recommendation": "Use these patterns to compare customer groups and spot retention opportunities.",
        },
        "Financial Data": {
            "lens": "costs, revenue, spending, margins, financial risk, and performance",
            "recommendation": "Use these patterns to review financial risk, cost drivers, and revenue opportunities.",
        },
        "Marketing Analysis": {
            "lens": "campaigns, engagement, conversion, channels, and audience behavior",
            "recommendation": "Use these patterns to compare campaign performance and audience engagement.",
        },
        "General Analytics": {
            "lens": "patterns, trends, groups, quality, and relationships",
            "recommendation": "Use these patterns to decide what to explore next.",
        },
    }
    return contexts.get(mode, contexts["General Analytics"])


def quality_score_card_text(quality):
    """Create a short plain-English quality score explanation."""
    return (
        f"Your dataset quality score is {quality['score']}/100. "
        f"{quality['explanation']}"
    )


def cleaned_dataset(df):
    """Create a light cleanup export without changing values."""
    return df.dropna(how="all").dropna(axis=1, how="all").drop_duplicates()


def summarize_outliers(outliers):
    """Create a compact outlier summary for display and export."""
    if outliers.empty:
        return "No numeric columns had enough variation for IQR outlier checks."
    if outliers["Outliers"].sum() == 0:
        return "No IQR outliers were detected."

    biggest = outliers.sort_values("Outliers", ascending=False).iloc[0]
    return (
        f"{biggest['Column']} has the most IQR outliers with "
        f"{int(biggest['Outliers']):,} flagged value(s)."
    )


def describe_trend(df, date_column, numeric_column, date_versions):
    """Estimate whether a numeric value is increasing or decreasing over time."""
    chart_df = pd.DataFrame(
        {
            "date": date_versions.get(date_column, pd.to_datetime(df[date_column], errors="coerce")),
            "value": pd.to_numeric(df[numeric_column], errors="coerce"),
        }
    ).dropna()

    if len(chart_df) < 3:
        return None

    chart_df = chart_df.sort_values("date")
    x_values = np.arange(len(chart_df))
    slope = np.polyfit(x_values, chart_df["value"], 1)[0]

    if abs(slope) < 0.01:
        return f"{numeric_column} appears mostly stable over time."

    direction = "increasing" if slope > 0 else "decreasing"
    return f"{numeric_column} appears to be {direction} over time."


def generate_insights(df, detected_types, date_versions, outliers, corr, quality=None, mode="General Analytics"):
    """Generate simple English insights that work for many datasets."""
    cards = []
    numeric_columns = detected_types["Numeric"]
    categorical_columns = detected_types["Categorical"]
    date_columns = detected_types["Date/Time"]
    context = mode_context(mode)

    cards.append(
        (
            "Dataset overview",
            f"This file has {df.shape[0]:,} rows and {df.shape[1]:,} columns. "
            f"I detected {len(numeric_columns)} numeric, {len(categorical_columns)} categorical, "
            f"{len(date_columns)} date/time, and {len(detected_types['Boolean'])} boolean column(s). "
            f"In {mode.lower()} mode, I am framing the analysis around {context['lens']}.",
        )
    )

    if quality:
        cards.append(("Data Quality Score", quality_score_card_text(quality)))

    missing_total = int(df.isna().sum().sum())
    duplicate_count = int(df.duplicated().sum())
    if missing_total == 0 and duplicate_count == 0:
        cards.append(("Data quality", "No missing values or duplicate rows were found."))
    else:
        cards.append(
            (
                "Data quality",
                f"I found {missing_total:,} missing value(s) and {duplicate_count:,} duplicate row(s). "
                "Review these before making important decisions from the data.",
            )
        )

    if date_columns:
        first_date_column = date_columns[0]
        date_series = date_versions[first_date_column].dropna()
        if not date_series.empty:
            cards.append(
                (
                    "Time coverage",
                    f"{first_date_column} runs from {date_series.min().date()} to {date_series.max().date()}.",
                )
            )

    if not outliers.empty and outliers["Outliers"].sum() > 0:
        biggest = outliers.sort_values("Outliers", ascending=False).iloc[0]
        cards.append(
            (
                "Outliers",
                f"{biggest['Column']} has the most IQR outliers with {int(biggest['Outliers']):,} flagged value(s). "
                "Outliers can be real signals, data entry issues, or unusual cases worth reviewing.",
            )
        )
    elif numeric_columns:
        cards.append(("Outliers", "No IQR outliers were detected in the numeric columns that had enough data."))

    positive, negative = strongest_correlations(corr)
    if positive:
        cards.append(
            (
                "Strongest positive correlation",
                f"{positive[0]} and {positive[1]} move together most strongly with a correlation of {positive[2]:.2f}.",
            )
        )
    if negative:
        cards.append(
            (
                "Strongest negative correlation",
                f"{negative[0]} and {negative[1]} move in opposite directions most strongly with a correlation of {negative[2]:.2f}.",
            )
        )

    if date_columns and numeric_columns:
        trend = describe_trend(df, date_columns[0], numeric_columns[0], date_versions)
        if trend:
            cards.append(("Trend", trend))

    for column in categorical_columns[:2]:
        top_values = df[column].value_counts(dropna=True)
        if not top_values.empty:
            cards.append(
                (
                    "Dominant category",
                    f"The most common value in {column} is {top_values.index[0]} "
                    f"with {top_values.iloc[0]:,} row(s).",
                )
            )

    return cards


def explain_my_data(df, detected_types, date_versions, outliers, corr, quality, mode):
    """Generate an AI-style dataset explanation without using an API."""
    numeric_columns = detected_types["Numeric"]
    categorical_columns = detected_types["Categorical"]
    date_columns = detected_types["Date/Time"]
    context = mode_context(mode)
    cards = []

    cards.append(
        (
            "What this dataset contains",
            f"This dataset contains {df.shape[0]:,} records across {df.shape[1]:,} fields. "
            f"It includes {len(numeric_columns)} numeric field(s), {len(categorical_columns)} category field(s), "
            f"and {len(date_columns)} date/time field(s). I am reading it through a {mode.lower()} lens focused on {context['lens']}.",
        )
    )

    if numeric_columns:
        summary_bits = []
        for column in numeric_columns[:3]:
            values = pd.to_numeric(df[column], errors="coerce").dropna()
            if not values.empty:
                summary_bits.append(f"{column} averages {values.mean():,.2f} and ranges from {values.min():,.2f} to {values.max():,.2f}")
        cards.append(("Key numeric patterns", ". ".join(summary_bits) + "." if summary_bits else "Numeric columns were found, but they do not have enough usable values to summarize."))

    if categorical_columns:
        category_bits = []
        for column in categorical_columns[:3]:
            counts = df[column].value_counts(dropna=True)
            if not counts.empty:
                category_bits.append(f"{column} is led by {counts.index[0]} with {counts.iloc[0]:,} row(s)")
        cards.append(("Key category patterns", ". ".join(category_bits) + "." if category_bits else "Category columns were found, but they do not have enough usable values to summarize."))

    if date_columns:
        date_column = date_columns[0]
        date_series = date_versions[date_column].dropna()
        if not date_series.empty:
            cards.append(("Date/time coverage", f"{date_column} covers {date_series.min().date()} through {date_series.max().date()}."))

    warnings_text = []
    if quality["missing_values"] > 0:
        warnings_text.append(f"{quality['missing_values']:,} missing value(s)")
    if quality["duplicate_rows"] > 0:
        warnings_text.append(f"{quality['duplicate_rows']:,} duplicate row(s)")
    if quality["invalid_values"] > 0:
        warnings_text.append(f"{quality['invalid_values']:,} possible data type issue(s)")
    if not outliers.empty and outliers["Outliers"].sum() > 0:
        warnings_text.append(summarize_outliers(outliers))
    cards.append(("Possible risks or warnings", ", ".join(warnings_text) + "." if warnings_text else "No major quality warnings stood out from the automated checks."))

    recommendations = recommended_actions(df, detected_types, date_versions, outliers, corr, quality, mode)[:3]
    cards.append(("Practical recommendations", " ".join(f"{index + 1}. {item}" for index, item in enumerate(recommendations))))

    return cards


def generate_questions(detected_types, mode="General Analytics"):
    """Suggest analysis questions based on detected columns."""
    questions = []
    numeric_columns = detected_types["Numeric"]
    categorical_columns = detected_types["Categorical"]
    date_columns = detected_types["Date/Time"]
    context = mode_context(mode)

    if date_columns and numeric_columns:
        questions.append(f"How does {numeric_columns[0]} change over time?")

    if numeric_columns:
        questions.append(f"Are there extreme values in {numeric_columns[0]}?")

    if categorical_columns:
        questions.append(f"Which {categorical_columns[0]} appears most frequently?")

    if len(numeric_columns) >= 2:
        questions.append(f"Is there a relationship between {numeric_columns[0]} and {numeric_columns[1]}?")

    if categorical_columns and numeric_columns:
        questions.append(f"How does {numeric_columns[0]} compare across {categorical_columns[0]}?")

    if mode == "Customer Insights" and categorical_columns:
        questions.append(f"Which {categorical_columns[0]} segment may need closer attention for retention or satisfaction?")
    elif mode == "Financial Data" and numeric_columns:
        questions.append(f"Which numeric metric could represent the biggest financial risk or opportunity?")
    elif mode == "Marketing Analysis" and categorical_columns:
        questions.append(f"Which {categorical_columns[0]} group shows the strongest engagement or conversion signal?")
    elif mode == "Business Analytics" and numeric_columns:
        questions.append(f"Which metric should leaders monitor to improve performance or efficiency?")
    else:
        questions.append(f"Which finding would be most useful for decisions about {context['lens']}?")

    return questions


def recommended_actions(df, detected_types, date_versions, outliers, corr, quality, mode):
    """Generate practical next actions from the dataset profile."""
    actions = []
    numeric_columns = detected_types["Numeric"]
    categorical_columns = detected_types["Categorical"]
    date_columns = detected_types["Date/Time"]
    context = mode_context(mode)

    if quality["missing_values"] > 0:
        actions.append("Review columns with missing values before making decisions.")
    if quality["duplicate_rows"] > 0:
        actions.append("Check duplicate rows and decide whether they represent repeated events or accidental copies.")
    if quality["invalid_values"] > 0:
        actions.append("Fix values that do not match their detected data type so summaries and charts are more reliable.")

    if not outliers.empty and outliers["Outliers"].sum() > 0:
        biggest = outliers.sort_values("Outliers", ascending=False).iloc[0]
        actions.append(f"Investigate extreme values in {biggest['Column']} to see whether they are errors or meaningful exceptions.")

    positive, negative = strongest_correlations(corr)
    if positive:
        actions.append(f"Explore why {positive[0]} and {positive[1]} move together before using that relationship in decisions.")
    elif negative:
        actions.append(f"Explore why {negative[0]} and {negative[1]} move in opposite directions before using that relationship in decisions.")

    if categorical_columns and numeric_columns:
        actions.append(f"Segment results by {categorical_columns[0]} to compare groups and find where {numeric_columns[0]} changes most.")

    if date_columns and numeric_columns:
        actions.append(f"Track {numeric_columns[0]} over {date_columns[0]} to see whether the pattern is stable or changing.")

    if mode == "Customer Insights" and categorical_columns:
        actions.append(f"Use {categorical_columns[0]} to compare customer segments for retention, satisfaction, or churn signals.")
    elif mode == "Financial Data" and numeric_columns:
        actions.append(f"Review {numeric_columns[0]} for cost, revenue, spending, margin, or risk implications.")
    elif mode == "Marketing Analysis" and categorical_columns:
        actions.append(f"Compare {categorical_columns[0]} groups to understand campaign, conversion, or audience behavior differences.")
    elif mode == "Business Analytics":
        actions.append(f"Use these findings to prioritize performance, operations, efficiency, and decision-making questions.")

    actions.append(context["recommendation"])

    unique_actions = []
    for action in actions:
        if action not in unique_actions:
            unique_actions.append(action)

    return unique_actions[:5]


def top_driver_summary(corr, target_column):
    """Create plain-English driver text for one target column."""
    if corr.empty or not target_column:
        return "At least two numeric columns are needed to summarize Top Drivers."

    positive, negative = driver_groups(corr, target_column)
    lines = []

    if not positive.empty:
        row = positive.iloc[0]
        lines.append(
            f"{row['Column']} has the strongest positive relationship with {target_column} "
            f"(correlation {row['Correlation']:.2f}). This may suggest that higher values in one also tend to appear with higher values in the other."
        )

    if not negative.empty:
        row = negative.iloc[0]
        lines.append(
            f"{row['Column']} has the strongest negative relationship with {target_column} "
            f"(correlation {row['Correlation']:.2f}). This may suggest that higher values in one tend to appear with lower values in the other."
        )

    if not lines:
        lines.append(f"No strong positive or negative driver relationships stood out for {target_column}.")

    lines.append("Caution: correlation does not prove causation. Treat these as useful clues, not final answers.")
    return " ".join(lines)


def insights_markdown(df, detected_types, date_versions, outliers, corr, quality, mode, target_column):
    """Build a downloadable Markdown insights summary."""
    cards = generate_insights(df, detected_types, date_versions, outliers, corr, quality, mode)
    explanation_cards = explain_my_data(df, detected_types, date_versions, outliers, corr, quality, mode)
    questions = generate_questions(detected_types, mode)
    actions = recommended_actions(df, detected_types, date_versions, outliers, corr, quality, mode)

    lines = [
        "# Liv Insights Summary",
        "",
        f"Analysis Mode: {mode}",
        "",
        "## Dataset Overview",
        f"- Rows: {df.shape[0]:,}",
        f"- Columns: {df.shape[1]:,}",
        f"- Numeric columns: {len(detected_types['Numeric'])}",
        f"- Categorical columns: {len(detected_types['Categorical'])}",
        f"- Date/time columns: {len(detected_types['Date/Time'])}",
        "",
        "## Data Quality Score",
        f"- Score: {quality['score']}/100",
        f"- Explanation: {quality['explanation']}",
        f"- Missing values impact: -{quality['missing_impact']} points",
        f"- Duplicate rows impact: -{quality['duplicate_impact']} points",
        f"- Data type issues impact: -{quality['type_impact']} points",
        "",
        "## Key Insights",
    ]

    for title, body in cards:
        lines.append(f"- {title}: {body}")

    lines.extend(["", "## Explain My Data"])
    for title, body in explanation_cards:
        lines.append(f"- {title}: {body}")

    lines.extend(["", "## Outliers Summary", f"- {summarize_outliers(outliers)}"])
    lines.extend(["", "## Correlation and Top Drivers", f"- {top_driver_summary(corr, target_column)}"])
    lines.extend(["", "## Recommended Next Actions"])
    lines.extend([f"- {action}" for action in actions])
    lines.extend(["", "## Suggested Questions"])
    lines.extend([f"- {question}" for question in questions])

    return "\n".join(lines)


def clean_figure(fig):
    """Apply a consistent Plotly style."""
    fig.update_layout(
        template="plotly_white",
        title_font_color=INK_COLOR,
        title_font_size=20,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#111111", size=13),
        legend=dict(
            font=dict(color="#111111", size=13),
            bgcolor="rgba(255,255,255,0.92)",
            bordercolor="#dfe7ef",
            borderwidth=1,
        ),
        margin=dict(l=30, r=30, t=70, b=40),
        colorway=[THEME_COLOR, ACCENT_COLOR, "#6c8ead", "#6ab187", "#c8553d"],
    )
    fig.update_xaxes(
        showgrid=False,
        title_font=dict(color="#111111", size=14),
        tickfont=dict(color="#111111", size=12),
        linecolor="#9fb0bf",
        zerolinecolor="#9fb0bf",
    )
    fig.update_yaxes(
        gridcolor="#dfe7ef",
        title_font=dict(color="#111111", size=14),
        tickfont=dict(color="#111111", size=12),
        linecolor="#9fb0bf",
        zerolinecolor="#9fb0bf",
    )
    return fig


def show_column_type_summary(detected_types):
    """Display detected column types in compact columns."""
    st.subheader("Detected Column Types")
    type_columns = st.columns(4)

    for index, column_type in enumerate(["Numeric", "Categorical", "Date/Time", "Boolean"]):
        with type_columns[index]:
            st.metric(column_type, len(detected_types[column_type]))
            if detected_types[column_type]:
                st.caption(", ".join(detected_types[column_type]))


def show_upload_section(df, detected_types):
    """Render upload preview and column type information."""
    st.header("Upload Data")
    st.write("Preview your uploaded dataset and confirm the detected column types.")

    preview_rows = st.slider("Rows to preview", min_value=5, max_value=10, value=5)
    st.dataframe(df.head(preview_rows), use_container_width=True)

    metric_columns = st.columns(3)
    metric_columns[0].metric("Rows", f"{df.shape[0]:,}")
    metric_columns[1].metric("Columns", f"{df.shape[1]:,}")
    metric_columns[2].metric("Missing Values", f"{int(df.isna().sum().sum()):,}")

    show_column_type_summary(detected_types)


def show_data_health_section(df, detected_types, date_versions, outliers):
    """Render missing values, duplicates, invalid types, and outlier checks."""
    st.header("Data Health Check")
    st.write("We checked for missing values, duplicates, data types, outliers, and overall usability.")
    health_issues = build_health_issues(df, detected_types, date_versions)
    quality = data_quality_score(df, detected_types, date_versions)

    st.subheader("Data Quality Score")
    score_col, detail_col = st.columns([1, 2])
    score_col.metric("Overall Score", f"{quality['score']}/100")
    with detail_col:
        insight_card("Quality summary", quality_score_card_text(quality))
        st.write(
            f"Missing values impact: -{quality['missing_impact']} points | "
            f"Duplicate rows impact: -{quality['duplicate_impact']} points | "
            f"Data type issues impact: -{quality['type_impact']} points"
        )

    if has_health_issues(health_issues):
        st.markdown(
            '<div class="health-warning">⚠️ Data issues detected</div>',
            unsafe_allow_html=True,
        )
        for issue_type, messages in health_issues.items():
            if messages:
                st.subheader(issue_type)
                for message in messages:
                    st.warning(message)
    else:
        st.markdown(
            '<div class="health-good">✅ Your data looks healthy. No major issues detected.</div>',
            unsafe_allow_html=True,
        )

    st.subheader("Outlier Detection")
    st.write("Numeric outliers are detected using the IQR method.")
    if outliers.empty:
        st.info("No numeric columns had enough variation for IQR outlier checks.")
    elif outliers["Outliers"].sum() == 0:
        st.success("No IQR outliers found.")
        st.dataframe(outliers, use_container_width=True)
    else:
        st.dataframe(outliers.sort_values("Outliers", ascending=False), use_container_width=True)

    st.subheader("Summary")
    summary_view = st.segmented_control(
        "Choose summary type",
        ["Numeric Summary", "Category Summary"],
        default="Numeric Summary",
        label_visibility="collapsed",
        width="stretch",
    )

    if summary_view == "Numeric Summary":
        summary = numeric_summary(df, detected_types["Numeric"])
        if summary.empty:
            st.info("No numeric columns found.")
        else:
            st.dataframe(summary, use_container_width=True)
    else:
        summary = categorical_summary(df, detected_types["Categorical"])
        if summary.empty:
            st.info("No categorical columns found.")
        else:
            st.dataframe(summary, use_container_width=True)


def show_insights_section(df, detected_types, date_versions, outliers, corr, quality, mode):
    """Render plain-English insight cards."""
    st.header("Insights")
    st.write("Review the most important patterns, warnings, and decision clues found in your dataset.")
    cards = generate_insights(df, detected_types, date_versions, outliers, corr, quality, mode)

    for title, body in cards:
        insight_card(title, body)

    if detected_types["Numeric"]:
        target_column = st.selectbox(
            "Choose a numeric target for exported Top Drivers summary",
            detected_types["Numeric"],
            key="insights_export_target",
        )
    else:
        target_column = None

    show_export_buttons(df, detected_types, date_versions, outliers, corr, quality, mode, target_column)


def show_explain_section(df, detected_types, date_versions, outliers, corr, quality, mode):
    """Render an AI-style explanation created locally from the data profile."""
    st.header("Explain My Data")
    st.write("A friendly business-analyst style explanation generated from your data, with no external API required.")

    for title, body in explain_my_data(df, detected_types, date_versions, outliers, corr, quality, mode):
        insight_card(title, body)


def show_recommended_actions_section(df, detected_types, date_versions, outliers, corr, quality, mode):
    """Render practical next actions."""
    st.header("Recommended Next Actions")
    st.write("Use these next steps to turn the analysis into practical decisions.")

    for action in recommended_actions(df, detected_types, date_versions, outliers, corr, quality, mode):
        insight_card("Recommended action", action)


def show_export_buttons(df, detected_types, date_versions, outliers, corr, quality, mode, target_column):
    """Render download buttons for cleaned data and insights."""
    st.subheader("Exports")
    st.write("Download a lightly cleaned dataset or a written insights summary for sharing.")

    cleaned_csv = cleaned_dataset(df).to_csv(index=False).encode("utf-8")
    summary_text = insights_markdown(df, detected_types, date_versions, outliers, corr, quality, mode, target_column)

    export_col_a, export_col_b = st.columns(2)
    export_col_a.download_button(
        "Download cleaned dataset as CSV",
        data=cleaned_csv,
        file_name="liv_insights_cleaned_dataset.csv",
        mime="text/csv",
    )
    export_col_b.download_button(
        "Download insights summary as Markdown",
        data=summary_text,
        file_name="liv_insights_summary.md",
        mime="text/markdown",
    )


def show_correlation_section(df, numeric_columns, corr):
    """Render correlation heatmap and top driver explanation."""
    st.subheader("Correlation Analysis")
    st.write("Compare numeric fields to see which values tend to move together or apart.")

    if corr.empty:
        st.info("At least two numeric columns are needed for correlation analysis.")
        return

    heatmap = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        title="Correlation Heatmap",
    )
    st.plotly_chart(clean_figure(heatmap), use_container_width=True)

    positive, negative = strongest_correlations(corr)
    col_a, col_b = st.columns(2)

    with col_a:
        if positive:
            insight_card(
                "Positive relationship",
                f"{positive[0]} and {positive[1]} have the strongest positive correlation ({positive[2]:.2f}).",
            )
        else:
            st.info("No positive correlations found.")

    with col_b:
        if negative:
            insight_card(
                "Negative relationship",
                f"{negative[0]} and {negative[1]} have the strongest negative correlation ({negative[2]:.2f}).",
            )
        else:
            st.info("No negative correlations found.")

    target_column = st.selectbox("Choose a target column for Top Drivers", numeric_columns)
    positive_drivers, negative_drivers = driver_groups(corr, target_column)
    drivers = target_drivers(corr, target_column)

    st.subheader("Top Drivers")
    if drivers.empty:
        st.info("No driver relationships were found for this target.")
    else:
        insight_card("What this may mean", top_driver_summary(corr, target_column))

        driver_cols = st.columns(2)
        with driver_cols[0]:
            st.write("Strongest positive relationships")
            if positive_drivers.empty:
                st.info("No positive driver relationships found.")
            else:
                st.dataframe(positive_drivers, use_container_width=True)

        with driver_cols[1]:
            st.write("Strongest negative relationships")
            if negative_drivers.empty:
                st.info("No negative driver relationships found.")
            else:
                st.dataframe(negative_drivers, use_container_width=True)

        st.caption("Correlation does not prove causation. Use these relationships as clues for deeper analysis.")


def show_visualizations(df, selected_columns, detected_types, date_versions, corr):
    """Show chart options that match the selected columns."""
    st.header("Visualizations")
    st.write("Choose the columns and chart type that best match the question you want to answer.")

    selected_numeric = [col for col in selected_columns if col in detected_types["Numeric"]]
    selected_categorical = [col for col in selected_columns if col in detected_types["Categorical"]]
    selected_dates = [col for col in selected_columns if col in detected_types["Date/Time"]]

    st.markdown('<div class="chart-choice">Choose a visualization</div>', unsafe_allow_html=True)
    chart_type = st.segmented_control(
        "Choose a visualization",
        ["Histogram", "Bar Chart", "Scatter Plot", "Line Chart", "Heatmap"],
        default="Histogram",
        label_visibility="collapsed",
        width="stretch",
    )
    chart_type = chart_type or "Histogram"

    if chart_type == "Histogram":
        if selected_numeric:
            column = st.selectbox("Numeric column", selected_numeric, key="histogram_column")
            chart_df = pd.DataFrame({column: pd.to_numeric(df[column], errors="coerce")}).dropna()
            fig = px.histogram(chart_df, x=column, nbins=30, title=f"Distribution of {column}")
            st.plotly_chart(clean_figure(fig), use_container_width=True)
        else:
            st.info("Select at least one numeric column to create a histogram.")

    elif chart_type == "Bar Chart":
        if selected_categorical:
            column = st.selectbox("Categorical column", selected_categorical, key="bar_column")
            counts = df[column].value_counts(dropna=False).head(20).reset_index()
            counts.columns = [column, "Count"]
            fig = px.bar(counts, x=column, y="Count", title=f"Top values in {column}")
            st.plotly_chart(clean_figure(fig), use_container_width=True)
        else:
            st.info("Select at least one categorical column to create a bar chart.")

    elif chart_type == "Scatter Plot":
        if len(selected_numeric) >= 2:
            x_column = st.selectbox("X-axis", selected_numeric, key="scatter_x")
            y_options = [col for col in selected_numeric if col != x_column]
            y_column = st.selectbox("Y-axis", y_options, key="scatter_y")
            chart_df = df[[x_column, y_column]].apply(pd.to_numeric, errors="coerce").dropna()
            fig = px.scatter(chart_df, x=x_column, y=y_column, title=f"{y_column} vs {x_column}")
            st.plotly_chart(clean_figure(fig), use_container_width=True)
        else:
            st.info("Select at least two numeric columns to create a scatter plot.")

    elif chart_type == "Line Chart":
        if selected_dates and selected_numeric:
            date_column = st.selectbox("Date/time column", selected_dates, key="line_date")
            value_column = st.selectbox("Value column", selected_numeric, key="line_value")
            chart_df = pd.DataFrame(
                {
                    date_column: date_versions.get(date_column, pd.to_datetime(df[date_column], errors="coerce")),
                    value_column: pd.to_numeric(df[value_column], errors="coerce"),
                }
            ).dropna()
            chart_df = chart_df.sort_values(date_column)
            fig = px.line(chart_df, x=date_column, y=value_column, title=f"{value_column} over time")
            st.plotly_chart(clean_figure(fig), use_container_width=True)
        else:
            st.info("Select a date/time column and a numeric column to create a line chart.")

    elif chart_type == "Heatmap":
        show_correlation_section(df, detected_types["Numeric"], corr)


def show_questions_section(detected_types, mode):
    """Render suggested questions."""
    st.header("Suggested Questions")
    st.write("Use these prompts to guide your next round of analysis.")
    questions = generate_questions(detected_types, mode)

    if not questions:
        st.info("No suggested questions could be generated from the detected column types.")
        return

    for question in questions:
        insight_card("Try asking", question)


def sidebar_navigation():
    """Render app branding and section navigation in the sidebar."""
    st.sidebar.markdown("## LI Liv Insights")
    st.sidebar.caption("Simple analytics for everyday datasets")
    st.sidebar.markdown("### Navigation")

    if "active_section" not in st.session_state:
        st.session_state.active_section = "Upload Data"

    for label, icon in NAV_ITEMS:
        if st.session_state.active_section == label:
            st.sidebar.markdown(
                f'<div class="nav-active">{icon} {label}</div>',
                unsafe_allow_html=True,
            )
        elif st.sidebar.button(f"{icon} {label}", key=f"nav_{label}"):
            st.session_state.active_section = label
            st.rerun()

    return st.session_state.active_section


def initialize_session_state():
    """Create session keys used to keep uploaded data available across sections."""
    if "data" not in st.session_state:
        st.session_state.data = None
    if "file_name" not in st.session_state:
        st.session_state.file_name = None
    if "analysis_mode" not in st.session_state:
        st.session_state.analysis_mode = "General Analytics"


def show_upload_prompt():
    """Show the upload message only when no dataset is stored."""
    st.header("Upload Data")
    st.info("Upload a dataset from the sidebar to begin.")


def main():
    initialize_session_state()
    apply_theme()
    show_banner()
    section = sidebar_navigation()
    mode = st.sidebar.selectbox(
        "Analysis Mode",
        ANALYSIS_MODES,
        index=ANALYSIS_MODES.index(st.session_state.analysis_mode),
        help="Changes the wording of questions, recommendations, and insights.",
    )
    st.session_state.analysis_mode = mode

    uploaded_file = st.sidebar.file_uploader("Upload a CSV or XLSX file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            uploaded_df = read_uploaded_file(uploaded_file)
        except Exception as error:
            st.error(f"Could not read this file: {error}")
            if st.session_state.data is None:
                return
        else:
            if uploaded_df.empty:
                st.warning("The uploaded file does not contain any rows.")
                if st.session_state.data is None:
                    return
            else:
                st.session_state.data = uploaded_df
                st.session_state.file_name = uploaded_file.name

    df = st.session_state.get("data")

    if df is None:
        show_upload_prompt()
        return

    if st.session_state.get("file_name"):
        st.sidebar.success(f"Using {st.session_state.file_name}")

    detected_types, date_versions = detect_column_types(df)
    numeric_columns = detected_types["Numeric"]
    outliers = detect_outliers_iqr(df, numeric_columns)
    corr = correlation_matrix(df, numeric_columns)
    quality = data_quality_score(df, detected_types, date_versions)

    if section == "Upload Data":
        show_upload_section(df, detected_types)
    elif section == "Data Health":
        show_data_health_section(df, detected_types, date_versions, outliers)
    elif section == "Insights":
        show_insights_section(df, detected_types, date_versions, outliers, corr, quality, mode)
    elif section == "Explain My Data":
        show_explain_section(df, detected_types, date_versions, outliers, corr, quality, mode)
    elif section == "Visualizations":
        st.header("Select Columns")
        selected_columns = st.multiselect(
            "Choose columns for deeper analysis",
            options=list(df.columns),
            default=list(df.columns[: min(4, len(df.columns))]),
        )

        if selected_columns:
            show_visualizations(df, selected_columns, detected_types, date_versions, corr)
        else:
            st.info("Select one or more columns to generate visualizations.")
    elif section == "Recommended Actions":
        show_recommended_actions_section(df, detected_types, date_versions, outliers, corr, quality, mode)
    elif section == "Suggested Questions":
        show_questions_section(detected_types, mode)


if __name__ == "__main__":
    main()
