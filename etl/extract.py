import sqlite3
import pandas as pd
import json


def extract_data():
    try:
        # Подключение к базе данных
        conn = sqlite3.connect("data/dispatcher_quality.db")

        calls_query = "SELECT id, scenario_id, transcript_text FROM calls WHERE quality_score IS NULL"
        calls_df = pd.read_sql_query(calls_query, conn)

        scripts_query = (
            "SELECT id, scenario_id, script_text, embedding FROM canonical_scripts"
        )
        scripts_df = pd.read_sql_query(scripts_query, conn)

        conn.close()

        calls_df.to_json("etl/calls.json", orient="records", lines=True)
        scripts_df.to_json("etl/scripts.json", orient="records", lines=True)

        print(
            f"Extracted {len(calls_df)} calls and {len(scripts_df)} scripts to JSON files."
        )

    except sqlite3.Error as e:
        print(f"An error occurred while extracting data: {e}")
        raise


if __name__ == "__main__":
    extract_data()
