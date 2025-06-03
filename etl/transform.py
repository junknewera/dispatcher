import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import json


def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def transform_data():
    try:
        calls_df = pd.read_json("etl/calls.json", orient="records", lines=True)
        scripts_df = pd.read_json("etl/scripts.json", orient="records", lines=True)

        model = SentenceTransformer("cointegrated/rubert-tiny2")

        calls_df["embedding"] = calls_df["transcript_text"].apply(
            lambda x: model.encode(x)
        )

        scores = []
        for _, call in calls_df.iterrows():
            call_id = call["id"]
            scenario_id = call["scenario_id"]
            call_embedding = call["embedding"]

            relevant_scripts = scripts_df[scripts_df["scenario_id"] == scenario_id]
            if relevant_scripts.empty:
                print(f"No scripts found for scenario {scenario_id} in call {call_id}.")
                continue

            similarities = []
            for _, script in relevant_scripts.iterrows():
                script_embedding = np.array(json.loads(script["embedding"]))
                similarity = cosine_similarity(call_embedding, script_embedding)
                similarities.append(similarity)

            quality_score = max(similarities) if similarities else 0.0
            scores.append({"call_id": call_id, "quality_score": quality_score})

        scores_df = pd.DataFrame(scores)
        scores_df.to_json("etl/quality_scores.json", orient="records", lines=True)

        print(
            f"Transformed data and saved quality scores to 'etl/quality_scores.json'."
        )
    except Exception as e:
        print(f"An error occurred during transformation: {e}")
        raise


if __name__ == "__main__":
    transform_data()
