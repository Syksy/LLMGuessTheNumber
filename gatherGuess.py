import re
import os
import time
import pandas as pd

# Environmental variables
from dotenv import load_dotenv
load_dotenv()

# Working directory for project taken from env vars; write in an output folder 'out'
os.chdir(os.environ.get("ROOT_DIR"))

# Summary DF
summary = pd.DataFrame({'modelname': [], 'rep': [], 'temp': [], 'answer': []})

# Repeat the query 100 times
for rep in range(100):
    # Test determinism'ish (~0) and more freedom (0.2, 1.0) for temperature
    for temp in [0.0, 0.2, 1.0]:
        # Pad replicates to 00#, 0##, etc
        repf = str(rep).rjust(3, '0')
        models = [
            "claude-3-5-haiku-20241022",
            "claude-3-5-sonnet-20240620",
            "claude-3-5-sonnet-20241022",
            "claude-3-7-sonnet-20250219",
            "claude-sonnet-4-20250514",
            "claude-opus-4-20250514",
            "gpt-4o-2024-05-13",
            "gpt-4o-2024-08-06",
            "gpt-4o-2024-11-20",
            "gpt-4.1-nano-2025-04-14",
            "gpt-4.1-mini-2025-04-14",
            "gpt-4.1-2025-04-14",
            "mistral-large-2411",
            "mistral-medium-2505",
            "mistral-small-2503",
            "meta_llama-4-maverick-instruct",
            "meta_llama-4-scout-instruct",
            "deepseek-ai_deepseek-r1",
            "deepseek-ai_deepseek-v3",
            "gemini-2.5-pro-preview-03-25",
            "gemini-2.5-pro-preview-06-05",
            "gemini-2.5-pro-preview-05-06",
            "gemini-2.0-flash-001",
            "gemini-2.0-flash-lite-001",
            "grok-3-beta",
            "grok-2-1212",
            "google-deepmind_gemma-3-4b-it",
            "google-deepmind_gemma-3-12b-it",
            "google-deepmind_gemma-3-27b-it"
        ]
        # o1 / o3 are available for temp == 1.0
        if temp == 1.0:
            models = models + ["o1-2024-12-17", "o3-2025-04-16"]
        for modelname in models:
            filename = (modelname
                        + "_temp" + str(temp)
                        + "_rep" + str(repf)
                        )
            f = open("out\\" + filename + ".out", 'r', encoding='utf-8', errors='ignore')
            file_contents = f.read()
            # Chop away some models' very vocal thought process (such as DeepSeeks) wrapped in angle brackets <think>
            file_contents = re.sub(r'<think>.*?</think>', '', file_contents, flags=re.DOTALL)
            # Extracting max two digit numbers (including 1-9) from within text strings
            answer = re.search(r"\b\d{1,2}\b", file_contents).group()
            # Add result as a row to the DF
            summary.loc[len(summary.index)] = [
                modelname,
                rep,
                temp,
                answer
            ]

# Count each answer per combination
counts = summary.groupby(["modelname", "temp", "answer"]).size().reset_index(name="count")
# Calculate total counts per combination
total_counts = summary.groupby(["modelname", "temp"]).size().reset_index(name="total")
top_counts = counts.merge(total_counts, on=['modelname', 'temp'])
# Merging to calculate percentages
answer_counts = counts.merge(total_counts, on=["modelname", "temp"])
answer_counts["percent"] = (answer_counts["count"] / answer_counts["total"] * 100).round(0)
# Format <number> (<percentage>%)
answer_counts['formatted'] = answer_counts.apply(
    lambda row: f"{row['answer']} ({row['percent']}%)", axis=1
)
#print(answer_counts.head())
# Top three answers
top_counts = answer_counts.sort_values(
    ["modelname", "temp", "count"], ascending=[True, True, False]
).groupby(["modelname", "temp"]).head(3)
top_counts['percent'] = (top_counts['count'] / top_counts['total'] * 100).round(0)
top_counts['formatted'] = top_counts.apply(
    lambda row: f"{row['answer']} ({row['percent']}%)", axis=1
)
top_counts["rank"] = (top_counts.groupby(["modelname", "temp"]).cumcount()+1)
# Pivot
top_pivoted = top_counts.pivot(index=["modelname", "temp"], columns="rank", values="formatted").reset_index().rename(columns={1: "Top answer", 2: "2nd answer", 3: "3rd answer"})

# Split into separate tables
table_temp0p0 = top_pivoted[top_pivoted["temp"] == 0.0]
table_temp0p2 = top_pivoted[top_pivoted["temp"] == 0.2]
table_temp1p0 = top_pivoted[top_pivoted["temp"] == 1.0]

# View results
print("Table for temp = 0.0")
print(table_temp0p0.to_string(index=False))
table_temp0p0.to_csv("table_temp0p0.tsv", index=False, sep="\t")

print("\nTable for temp = 0.2")
print(table_temp0p2.to_string(index=False))
table_temp0p2.to_csv("table_temp0p2.tsv", index=False, sep="\t")

print("\nTable for temp = 1.0")
print(table_temp1p0.to_string(index=False))
table_temp1p0.to_csv("table_temp1p0.tsv", index=False, sep="\t")
