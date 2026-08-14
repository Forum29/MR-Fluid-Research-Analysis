from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
# ============================================================
# 1. PROJECT PATHS
# ============================================================
PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "MR_Fluid_Three_Paper_Research_Dataset_v2.csv"
RESULTS_DIR = PROJECT_DIR / "results"
FIGURES_DIR = RESULTS_DIR / "figures"
RESULTS_DIR.mkdir(exist_ok=True)
FIGURES_DIR.mkdir(exist_ok=True)
# ============================================================
# 2. LOAD DATASET
# ============================================================
print("=" * 70)
print("MR FLUID THREE-PAPER RESEARCH ANALYSIS")
print("=" * 70)
print("\nLoading dataset...")
if not DATA_FILE.exists():
    print("\nERROR: Dataset file was not found.")
    print("Expected location:")
    print(DATA_FILE)
    raise FileNotFoundError(DATA_FILE)
df = pd.read_csv(DATA_FILE)
print("\nDataset loaded successfully.")
print("Number of records:", len(df))
# ============================================================
# 3. CLEAN COLUMN NAMES
# ============================================================
df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
    .str.replace("-", "_", regex=False)
)
print("\n" + "=" * 70)
print("DATASET COLUMNS")
print("=" * 70)
for column in df.columns:
    print("-", column)
# ============================================================
# 4. BASIC DATASET INFORMATION
# ============================================================
print("\n" + "=" * 70)
print("DATASET PREVIEW")
print("=" * 70)
print(df.head(15).to_string(index=False))
# ============================================================
# 5. PAPER-WISE RECORD COUNT
# ============================================================
if "paper" in df.columns:
    print("\n" + "=" * 70)
    print("RECORDS BY PAPER")
    print("=" * 70)
    print(
        df["paper"]
        .value_counts(dropna=False)
        .to_string()
    )
# ============================================================
# 6. MEASURED VARIABLES
# ============================================================
if "measured_variable" in df.columns:
    print("\n" + "=" * 70)
    print("MEASURED VARIABLES IN THE THREE PAPERS")
    print("=" * 70)
    variables = (
        df["measured_variable"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
    )
    for variable in sorted(variables):
        print("-", variable)
# ============================================================
# 7. CONDITION VARIABLES
# ============================================================
if "condition_1" in df.columns:
    print("\n" + "=" * 70)
    print("CONDITION 1 VARIABLES")
    print("=" * 70)
    print(
        df["condition_1"]
        .dropna()
        .astype(str)
        .value_counts()
        .to_string()
    )
if "condition_2" in df.columns:
    print("\n" + "=" * 70)
    print("CONDITION 2 VARIABLES")
    print("=" * 70)
    print(
        df["condition_2"]
        .dropna()
        .astype(str)
        .value_counts()
        .to_string()
    )
# ============================================================
# 8. MEASURED VARIABLE SUMMARY
# ============================================================
if (
    "measured_variable" in df.columns
    and "measured_value" in df.columns
):
    df["measured_value"] = pd.to_numeric(
        df["measured_value"],
        errors="coerce"
    )
    print("\n" + "=" * 70)
    print("MEASURED VARIABLE SUMMARY")
    print("=" * 70)
    summary = (
        df.groupby("measured_variable")["measured_value"]
        .agg(
            count="count",
            minimum="min",
            maximum="max",
            mean="mean"
        )
        .round(4)
    )
    print(summary.to_string())
# ============================================================
# 9. IDENTIFY YIELD-STRESS DATA
# ============================================================
yield_mask = pd.Series(False, index=df.index)
if "measured_variable" in df.columns:
    yield_mask = (
        df["measured_variable"]
        .astype(str)
        .str.lower()
        .str.contains(
            "yield|yield_stress",
            na=False
        )
    )
yield_df = df[yield_mask].copy()
# ============================================================
# 10. DISPLAY YIELD-STRESS DATA
# ============================================================
print("\n" + "=" * 70)
print("YIELD-STRESS DATA")
print("=" * 70)
if len(yield_df) == 0:
    print(
        "\nNo measured variable containing "
        "'yield' was automatically identified."
    )
else:
    print(
        yield_df.to_string(index=False)
    )
    print(
        "\nNumber of yield-stress records:",
        len(yield_df)
    )
# ============================================================
# 11. IDENTIFY MAGNETIC-FIELD CONDITION
# ============================================================
magnetic_mask_1 = pd.Series(False, index=df.index)
magnetic_mask_2 = pd.Series(False, index=df.index)
if "condition_1" in df.columns:
    magnetic_mask_1 = (
        df["condition_1"]
        .astype(str)
        .str.lower()
        .str.contains(
            "magnetic|field|magnet",
            na=False
        )
    )
if "condition_2" in df.columns:
    magnetic_mask_2 = (
        df["condition_2"]
        .astype(str)
        .str.lower()
        .str.contains(
            "magnetic|field|magnet",
            na=False
        )
    )
# ============================================================
# 12. DISPLAY MAGNETIC-FIELD CONDITIONS
# ============================================================
print("\n" + "=" * 70)
print("POSSIBLE MAGNETIC-FIELD CONDITIONS")
print("=" * 70)
if magnetic_mask_1.any():
    print("\nCondition 1:")
    print(
        df.loc[
            magnetic_mask_1,
            [
                "condition_1",
                "condition_1_value",
                "condition_1_unit"
            ]
        ]
        .drop_duplicates()
        .to_string(index=False)
    )
if magnetic_mask_2.any():
    print("\nCondition 2:")
    print(
        df.loc[
            magnetic_mask_2,
            [
                "condition_2",
                "condition_2_value",
                "condition_2_unit"
            ]
        ]
        .drop_duplicates()
        .to_string(index=False)
    )
if not magnetic_mask_1.any() and not magnetic_mask_2.any():
    print(
        "\nNo magnetic-field condition was automatically identified."
    )
# ============================================================
# 13. CREATE MAGNETIC-FIELD VS YIELD-STRESS DATA
# ============================================================
analysis_df = pd.DataFrame()
# ---- Magnetic field in condition 1 ----
if magnetic_mask_1.any() and len(yield_df) > 0:
    temp = df[
        magnetic_mask_1 & yield_mask
    ].copy()
    if len(temp) > 0:
        analysis_df["magnetic_field"] = pd.to_numeric(
            temp["condition_1_value"],
            errors="coerce"
        )
        analysis_df["yield_stress"] = pd.to_numeric(
            temp["measured_value"],
            errors="coerce"
        )
        if "paper" in temp.columns:
            analysis_df["paper"] = temp["paper"].values
# ---- Magnetic field in condition 2 ----
if magnetic_mask_2.any() and len(yield_df) > 0:
    temp = df[
        magnetic_mask_2 & yield_mask
    ].copy()
    if len(temp) > 0:
        second_df = pd.DataFrame()
        second_df["magnetic_field"] = pd.to_numeric(
            temp["condition_2_value"],
            errors="coerce"
        )
        second_df["yield_stress"] = pd.to_numeric(
            temp["measured_value"],
            errors="coerce"
        )
        if "paper" in temp.columns:
            second_df["paper"] = temp["paper"].values
        analysis_df = pd.concat(
            [
                analysis_df,
                second_df
            ],
            ignore_index=True
        )
# ============================================================
# 14. CLEAN ANALYSIS DATA
# ============================================================
if len(analysis_df) > 0:
    analysis_df = analysis_df.dropna(
        subset=[
            "magnetic_field",
            "yield_stress"
        ]
    )
# ============================================================
# 15. MAGNETIC FIELD VS YIELD STRESS GRAPH
# ============================================================
print("\n" + "=" * 70)
print("MAGNETIC FIELD VS YIELD STRESS ANALYSIS")
print("=" * 70)
if len(analysis_df) == 0:
    print(
        "\nThe available dataset does not contain "
        "enough automatically identifiable information "
        "to create the magnetic-field vs yield-stress graph."
    )
    print(
        "\nThis is NOT a Python error."
    )
    print(
        "The dataset structure is general and the "
        "experimental variable names need to be inspected."
    )
else:
    print(
        "\nAnalysis records:",
        len(analysis_df)
    )
    print(
        analysis_df.to_string(index=False)
    )
    plt.figure(figsize=(8, 5))
    if "paper" in analysis_df.columns:
        for paper in analysis_df["paper"].unique():

            subset = analysis_df[
                analysis_df["paper"] == paper
            ]
            plt.scatter(
                subset["magnetic_field"],
                subset["yield_stress"],
                s=60,
                label=str(paper)
            )
        plt.legend()
    else:
        plt.scatter(
            analysis_df["magnetic_field"],
            analysis_df["yield_stress"],
            s=60
        )
    plt.xlabel("Magnetic Field")
    plt.ylabel("Yield Stress")
    plt.title(
        "Magnetic Field vs Yield Stress in MR Fluids"
    )
    plt.grid(True)
    plt.tight_layout()
    output_file = (
        FIGURES_DIR /
        "magnetic_field_vs_yield_stress.png"
    )
    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )
    print(
        "\nGraph saved to:"
    )
    print(output_file)
    plt.show()
# ============================================================
# 16. COMPLETION
# ============================================================
print("\n" + "=" * 70)
print("DATASET INSPECTION COMPLETED")
print("=" * 70)
print(
    "\nYour three-paper MR-fluid dataset was loaded successfully."
)
print(
    "\nThe program has inspected:"
)
print("- Papers")
print("- Measured variables")
print("- Experimental conditions")
print("- Yield-stress records")
print("- Magnetic-field conditions")
print(
    "\nNo changes were made to your original CSV."
)