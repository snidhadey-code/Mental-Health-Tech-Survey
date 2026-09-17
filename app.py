# ============================================================
# MENTAL HEALTH IN TECH - INTERACTIVE STREAMLIT DASHBOARD
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------

st.set_page_config(
    page_title="Mental Health in Tech Survey",
    page_icon="🧠",
    layout="wide"
)

# ------------------------------------------------------------
# TITLE
# ------------------------------------------------------------

st.title("🧠 Mental Health in Tech Survey Dashboard")

st.markdown(
    """
    This interactive dashboard explores mental health patterns among
    technology-sector employees. It examines treatment, family history,
    work interference, employer benefits, remote work, company size,
    gender and access to mental-health care.
    """
)

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("survey.csv")


try:
    df = load_data()

except FileNotFoundError:
    st.error(
        "survey.csv was not found. Make sure survey.csv and app.py "
        "are inside the same folder."
    )
    st.stop()


# ------------------------------------------------------------
# BASIC DATA CLEANING
# ------------------------------------------------------------

# Remove accidental spaces from column names
df.columns = df.columns.str.strip()

# Age cleaning
if "Age" in df.columns:
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

    # Keep realistic working-age responses
    df.loc[(df["Age"] < 18) | (df["Age"] > 80), "Age"] = pd.NA


# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

st.sidebar.header("🔎 Dashboard Filters")

filtered_df = df.copy()


# Gender filter
if "Gender" in df.columns:

    gender_options = sorted(
        df["Gender"].dropna().astype(str).unique().tolist()
    )

    selected_gender = st.sidebar.multiselect(
        "Select Gender",
        gender_options
    )

    if selected_gender:
        filtered_df = filtered_df[
            filtered_df["Gender"].astype(str).isin(selected_gender)
        ]


# Treatment filter
if "treatment" in df.columns:

    treatment_options = sorted(
        df["treatment"].dropna().astype(str).unique().tolist()
    )

    selected_treatment = st.sidebar.multiselect(
        "Select Treatment Status",
        treatment_options
    )

    if selected_treatment:
        filtered_df = filtered_df[
            filtered_df["treatment"].astype(str).isin(selected_treatment)
        ]


# Remote work filter
if "remote_work" in df.columns:

    remote_options = sorted(
        df["remote_work"].dropna().astype(str).unique().tolist()
    )

    selected_remote = st.sidebar.multiselect(
        "Select Remote Work Status",
        remote_options
    )

    if selected_remote:
        filtered_df = filtered_df[
            filtered_df["remote_work"].astype(str).isin(selected_remote)
        ]


st.sidebar.markdown("---")

st.sidebar.info(
    "Use the filters above to interactively explore the survey."
)


# ------------------------------------------------------------
# KPI SECTION
# ------------------------------------------------------------

st.subheader("📌 Survey Overview")

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "Total Respondents",
        f"{len(filtered_df):,}"
    )

with k2:

    if "treatment" in filtered_df.columns and len(filtered_df) > 0:

        treatment_rate = (
            filtered_df["treatment"]
            .astype(str)
            .str.lower()
            .eq("yes")
            .mean()
            * 100
        )

        st.metric(
            "Sought Treatment",
            f"{treatment_rate:.1f}%"
        )

    else:
        st.metric("Sought Treatment", "N/A")


with k3:

    if "Age" in filtered_df.columns:

        avg_age = filtered_df["Age"].mean()

        if pd.notna(avg_age):
            st.metric(
                "Average Age",
                f"{avg_age:.1f}"
            )
        else:
            st.metric("Average Age", "N/A")

    else:
        st.metric("Average Age", "N/A")


with k4:

    if "remote_work" in filtered_df.columns and len(filtered_df) > 0:

        remote_rate = (
            filtered_df["remote_work"]
            .astype(str)
            .str.lower()
            .eq("yes")
            .mean()
            * 100
        )

        st.metric(
            "Remote Workers",
            f"{remote_rate:.1f}%"
        )

    else:
        st.metric("Remote Workers", "N/A")


st.markdown("---")


# ------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------

def value_count_chart(data, column, title, xlabel):

    if column not in data.columns:
        st.warning(f"Column '{column}' is unavailable.")
        return

    counts = data[column].dropna().value_counts()

    if counts.empty:
        st.warning("No data available for the selected filters.")
        return

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        counts.index.astype(str),
        counts.values
    )

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Number of Respondents")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


def comparison_chart(
    data,
    row_column,
    target_column,
    title,
    xlabel
):

    if (
        row_column not in data.columns
        or target_column not in data.columns
    ):
        st.warning("Required columns are unavailable.")
        return

    temp = data[
        [row_column, target_column]
    ].dropna()

    if temp.empty:
        st.warning("No data available for the selected filters.")
        return

    comparison = pd.crosstab(
        temp[row_column],
        temp[target_column]
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    comparison.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Number of Respondents")

    ax.legend(
        title="Treatment"
    )

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


# ============================================================
# CHART 1
# Mental Health Treatment Distribution
# ============================================================

st.header("Chart 1 — Mental Health Treatment Distribution")

value_count_chart(
    filtered_df,
    "treatment",
    "Mental Health Treatment Among Respondents",
    "Sought Treatment"
)

st.markdown(
    """
    **Insight:** This visualization shows the overall distribution of
    respondents who have and have not sought treatment for a mental
    health condition.
    """
)

st.markdown("---")


# ============================================================
# CHART 2
# Treatment by Family History
# ============================================================

st.header("Chart 2 — Treatment by Family History")

comparison_chart(
    filtered_df,
    "family_history",
    "treatment",
    "Mental Health Treatment by Family History",
    "Family History of Mental Illness"
)

st.markdown(
    """
    **Insight:** This comparison helps examine whether respondents with
    a family history of mental illness show different treatment patterns.
    """
)

st.markdown("---")


# ============================================================
# CHART 3
# Work Interference
# ============================================================

st.header("Chart 3 — Mental Health and Work Interference")

value_count_chart(
    filtered_df,
    "work_interfere",
    "Impact of Mental Health on Work",
    "Frequency of Work Interference"
)

st.markdown(
    """
    **Insight:** The chart illustrates how frequently mental-health
    conditions interfere with respondents' work.
    """
)

st.markdown("---")


# ============================================================
# CHART 4
# Benefits vs Treatment
# ============================================================

st.header("Chart 4 — Mental Health Benefits vs Treatment")

comparison_chart(
    filtered_df,
    "benefits",
    "treatment",
    "Mental Health Treatment by Company Benefits",
    "Mental Health Benefits Provided by Employer"
)

st.markdown(
    """
    **Insight:** This chart compares treatment behaviour with the
    availability of employer-provided mental-health benefits.
    """
)

st.markdown("---")


# ============================================================
# CHART 5
# Remote Work vs Treatment
# ============================================================

st.header("Chart 5 — Remote Work vs Mental Health Treatment")

comparison_chart(
    filtered_df,
    "remote_work",
    "treatment",
    "Mental Health Treatment by Remote Work Status",
    "Remote Work"
)

st.markdown(
    """
    **Insight:** This analysis examines whether treatment patterns vary
    between remote and non-remote employees.
    """
)

st.markdown("---")


# ============================================================
# CHART 6
# Company Size vs Treatment
# ============================================================

st.header("Chart 6 — Company Size vs Mental Health Treatment")

comparison_chart(
    filtered_df,
    "no_employees",
    "treatment",
    "Mental Health Treatment by Company Size",
    "Number of Employees"
)

st.markdown(
    """
    **Insight:** This visualization compares treatment behaviour across
    organizations of different sizes.
    """
)

st.markdown("---")


# ============================================================
# CHART 7
# Gender vs Treatment
# ============================================================

st.header("Chart 7 — Mental Health Treatment by Gender")

comparison_chart(
    filtered_df,
    "Gender",
    "treatment",
    "Mental Health Treatment by Gender",
    "Gender"
)

st.markdown(
    """
    **Insight:** Treatment-seeking patterns can be compared across the
    gender categories represented in the survey.
    """
)

st.markdown("---")


# ============================================================
# CHART 8
# Family History vs Treatment
# ============================================================

st.header("Chart 8 — Family History vs Mental Health Treatment")

comparison_chart(
    filtered_df,
    "family_history",
    "treatment",
    "Mental Health Treatment by Family History",
    "Family History"
)

st.markdown(
    """
    **Insight:** Family history may be associated with greater awareness
    of mental-health conditions and differences in treatment-seeking
    behaviour.
    """
)

st.markdown("---")


# ============================================================
# CHART 9
# Work Interference vs Treatment
# ============================================================

st.header("Chart 9 — Treatment vs Work Interference")

comparison_chart(
    filtered_df,
    "work_interfere",
    "treatment",
    "Mental Health Treatment by Work Interference",
    "Work Interference"
)

st.markdown(
    """
    **Insight:** This comparison explores whether people experiencing
    different levels of work interference also show different treatment
    patterns.
    """
)

st.markdown("---")


# ============================================================
# CHART 10
# Benefits vs Treatment
# ============================================================

st.header("Chart 10 — Mental Health Treatment vs Benefits")

comparison_chart(
    filtered_df,
    "benefits",
    "treatment",
    "Mental Health Treatment vs Employer Benefits",
    "Employer Mental Health Benefits"
)

st.markdown(
    """
    **Insight:** Employer benefits may influence awareness and access to
    professional mental-health support.
    """
)

st.markdown("---")


# ============================================================
# CHART 11
# Care Options vs Treatment
# ============================================================

st.header("Chart 11 — Treatment vs Care Options")

comparison_chart(
    filtered_df,
    "care_options",
    "treatment",
    "Mental Health Treatment by Awareness of Care Options",
    "Awareness of Mental Health Care Options"
)

st.markdown(
    """
    **Insight:** Awareness of available care options can play an important
    role in whether employees seek mental-health treatment.
    """
)

st.markdown("---")


# ============================================================
# CHART 12
# Work Interference vs Treatment
# ============================================================

st.header("Chart 12 — Mental Health Treatment vs Work Interference")

comparison_chart(
    filtered_df,
    "work_interfere",
    "treatment",
    "Mental Health Treatment vs Work Interference",
    "Work Interference"
)

st.markdown(
    """
    **Insight:** Respondents whose mental health interferes with work can
    be compared according to whether they have sought treatment.
    """
)

st.markdown("---")


# ============================================================
# CHART 13
# Employer Benefits Distribution
# ============================================================

st.header("Chart 13 — Benefits Provided by Employers")

value_count_chart(
    filtered_df,
    "benefits",
    "Mental Health Benefits Provided by Employers",
    "Mental Health Benefits"
)

st.markdown(
    """
    **Insight:** The chart shows respondents' awareness of whether their
    employers provide mental-health benefits.
    """
)

st.markdown("---")


# ============================================================
# CHART 14
# Correlation Heatmap
# ============================================================

st.header("Chart 14 — Correlation Heatmap")

numeric_df = filtered_df.select_dtypes(
    include="number"
)

if numeric_df.shape[1] >= 2:

    corr = numeric_df.corr()

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        ax=ax
    )

    ax.set_title(
        "Correlation Heatmap of Numerical Variables"
    )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)

    st.markdown(
        """
        **Insight:** The heatmap shows relationships among the numerical
        variables. Values closer to +1 or -1 indicate stronger linear
        relationships, while values closer to zero indicate weaker
        linear relationships.
        """
    )

else:

    st.info(
        "There are not enough numerical variables to generate "
        "a correlation heatmap."
    )


st.markdown("---")


# ============================================================
# CHART 15
# Pair Plot
# ============================================================

st.header("Chart 15 — Pair Plot")

numeric_pair_df = filtered_df.select_dtypes(
    include="number"
).dropna()

if numeric_pair_df.shape[1] >= 2 and not numeric_pair_df.empty:

    # Limit the number of numerical columns to keep the
    # Streamlit dashboard responsive.
    pair_columns = numeric_pair_df.columns[:5]

    pair_data = numeric_pair_df[
        pair_columns
    ]

    # Sampling prevents the chart from becoming too slow
    # with a very large dataset.
    if len(pair_data) > 500:
        pair_data = pair_data.sample(
            500,
            random_state=42
        )

    pair_plot = sns.pairplot(
        pair_data,
        diag_kind="hist"
    )

    pair_plot.fig.suptitle(
        "Pair Plot of Numerical Variables",
        y=1.02
    )

    st.pyplot(pair_plot.fig)

    plt.close(pair_plot.fig)

    st.markdown(
        """
        **Insight:** The pair plot helps identify distributions,
        relationships, possible trends and unusual observations among
        numerical variables.
        """
    )

else:

    st.info(
        "There are not enough numerical variables to generate "
        "a pair plot."
    )


# ============================================================
# DATA EXPLORER
# ============================================================

st.markdown("---")

st.header("📋 Data Explorer")

st.write(
    f"Showing **{len(filtered_df):,}** respondents "
    "after applying the selected filters."
)

st.dataframe(
    filtered_df,
    use_container_width=True
)


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.markdown("---")

st.header("💡 Key Business Insights")

st.markdown(
    """
    - **Treatment accessibility:** Understanding treatment-seeking
      behaviour can help organizations design better employee assistance
      and mental-health programmes.

    - **Family history:** Family history provides useful context when
      analysing awareness and treatment behaviour.

    - **Work interference:** Mental-health difficulties can affect work,
      making employee support relevant to productivity and well-being.

    - **Employer benefits:** Clearly communicating available benefits and
      care options may improve employee awareness and access to support.

    - **Work environment:** Remote work and company size provide useful
      organizational context when studying employee mental health.

    - **Care awareness:** Employees need clear information about the
      mental-health resources and care options available to them.
    """
)


# ============================================================
# CONCLUSION
# ============================================================

st.markdown("---")

st.header("🎯 Conclusion")

st.markdown(
    """
    The Mental Health in Tech Survey highlights the relationship between
    employee mental health, treatment-seeking behaviour and workplace
    conditions.

    The analysis suggests that factors such as family history, work
    interference, employer benefits, awareness of care options, company
    size and work arrangements are useful dimensions for understanding
    mental-health experiences in the technology workforce.

    Organizations can use these insights to strengthen communication,
    improve access to mental-health resources and create more supportive
    workplace policies.
    """
)

