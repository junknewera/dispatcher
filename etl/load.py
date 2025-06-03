import sqlite3
import pandas as pd


def load_data():
    try:
        scored_df = pd.read_json(
            "etl/quality_scores.json", orient="records", lines=True
        )

        conn = sqlite3.connect("data/dispatcher_quality.db")
        cursor = conn.cursor()

        for _, row in scored_df.iterrows():
            cursor.execute(
                "UPDATE calls SET quality_score = ? WHERE id = ?",
                (row["quality_score"], row["call_id"]),
            )

        conn.commit()
        conn.close()

        print(f"Loaded quality scores into the database successfully.")

    except Exception as e:
        print(f"An error occurred during loading: {e}")
        if "conn" in locals():
            conn.close()
        raise


if __name__ == "__main__":
    load_data()
