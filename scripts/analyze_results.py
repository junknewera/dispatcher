import sqlite3
import pandas as pd


def analyze_results():
    try:
        conn = sqlite3.connect("data/dispatcher_quality.db")
        cursor = conn.cursor()

        query_calls = "SELECT id, transcript_text, quality_score FROM calls LIMIT 5"
        calls_df = pd.read_sql_query(query_calls, conn)
        print("Sample Calls Data:")
        print(calls_df)

        query_avg = """
            SELECT d.name, AVG(c.quality_score) as avg_score, COUNT(c.id) as call_count
            FROM calls c
            JOIN dispatchers d ON c.dispatcher_id = d.id
            GROUP BY d.id, d.name
        """
        avg_scores_df = pd.read_sql_query(query_avg, conn)
        print("\nAverage Quality Scores by Dispatcher:")
        print(avg_scores_df)

        query_stats = "SELECT MIN(quality_score) as min_score, MAX(quality_score) as max_score, AVG(quality_score) as avg_score FROM calls WHERE quality_score IS NOT NULL"
        stats_df = pd.read_sql_query(query_stats, conn)
        print("\nQuality Score Statistics:")
        print(f"Minimum Score: {stats_df.iloc[0, 0]:.4f}")
        print(f"Maximum Score: {stats_df.iloc[0, 1]:.4f}")
        print(f"Average Score: {stats_df.iloc[0, 2]:.4f}")

        conn.close()

    except sqlite3.Error as e:
        print(f"An error occurred while analyzing results: {e}")
        raise


if __name__ == "__main__":
    analyze_results()
