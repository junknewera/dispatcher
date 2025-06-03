import sqlite3
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sentence_transformers import SentenceTransformer
import json


def generate_synthetic_data():
    try:
        # Инициализация модели SentenceTransformer
        model = SentenceTransformer("cointegrated/rubert-tiny2")

        # Подключение к базе данных
        conn = sqlite3.connect("data/dispatcher_quality.db")

        # 1. Генерация сценариев
        scenarios = pd.DataFrame(
            [
                {"id": 1, "name": "Обработка заказа"},
                {"id": 2, "name": "Техническая поддержка"},
                {"id": 3, "name": "Консультация клиента"},
            ]
        )

        # 2. Генерация канонических скриптов
        canonical_scripts = pd.DataFrame(
            [
                {
                    "scenario_id": 1,
                    "script_text": "Здравствуйте, это диспетчерская служба. Чем могу помочь? Пожалуйста, назовите номер вашего заказа. Спасибо, заказ принят. До свидания.",
                },
                {
                    "scenario_id": 1,
                    "script_text": "Добрый день! Это диспетчерская служба. Назови номер заказа, пожалуйста. Заказ подтверждён, спасибо!",
                },
                {
                    "scenario_id": 2,
                    "script_text": "Добрый день, это техническая поддержка. Опишите вашу проблему. Мы решим её в ближайшее время. Спасибо за обращение.",
                },
                {
                    "scenario_id": 2,
                    "script_text": "Здравствуйте, техподдержка. В чём проблема? Мы разберёмся и свяжемся с вами. До свидания.",
                },
                {
                    "scenario_id": 3,
                    "script_text": "Здравствуйте, я диспетчер. Чем могу помочь? Расскажите о вашем вопросе, я постараюсь ответить. Спасибо за звонок!",
                },
            ]
        )
        # Генерация эмбеддингов и их сериализация в JSON
        canonical_scripts["embedding"] = canonical_scripts["script_text"].apply(
            lambda x: json.dumps(model.encode(x).tolist())
        )
        canonical_scripts["id"] = range(1, len(canonical_scripts) + 1)

        # 3. Генерация диспетчеров (5 диспетчеров, как в исходном коде)
        dispatchers = pd.DataFrame({"name": [f"Диспетчер {i+1}" for i in range(5)]})
        dispatchers["id"] = range(1, len(dispatchers) + 1)

        # 4. Генерация звонков (~10,000)
        transcript_variants = {
            "good": [
                "Здравствуйте, это диспетчерская служба. Назови номер заказа, пожалуйста. Заказ принят, спасибо!",
                "Добрый день! Чем могу помочь? Назови номер заказа. Всё, заказ подтверждён.",
            ],
            "medium": [
                "Привет, это диспетчерская. Какой у вас заказ? Ок, записал.",
                "Здравствуйте, диспетчер. Что надо? Назови номер, я запишу.",
            ],
            "poor": [
                "Алло, что надо? Заказ? Ну, ладно, давай номер.",
                "Привет, говори быстро, что там у тебя?",
            ],
        }

        num_dispatchers = len(dispatchers)
        calls_per_dispatcher = 10000 // num_dispatchers  # ~2,000 звонков на диспетчера
        calls = []
        start_date = datetime.now() - timedelta(days=7)

        # Оптимизированная генерация звонков
        for disp_id in dispatchers["id"]:
            for _ in range(calls_per_dispatcher):
                scenario_id = random.choice([1, 2, 3])
                quality_type = random.choices(
                    ["good", "medium", "poor"], weights=[0.5, 0.3, 0.2], k=1
                )[0]
                transcript = random.choice(transcript_variants[quality_type])
                random_date = start_date + timedelta(
                    seconds=random.randint(0, 7 * 24 * 60 * 60)
                )
                calls.append(
                    {
                        "dispatcher_id": disp_id,
                        "scenario_id": scenario_id,
                        "date_time": random_date.strftime("%Y-%m-%d %H:%M:%S"),
                        "transcript_text": transcript,
                        "quality_score": None,
                    }
                )

        calls_df = pd.DataFrame(calls)
        calls_df["id"] = range(1, len(calls_df) + 1)

        # 5. Сохранение данных в SQLite
        scenarios.to_sql("scenarios", conn, if_exists="append", index=False)
        canonical_scripts[["id", "scenario_id", "script_text", "embedding"]].to_sql(
            "canonical_scripts", conn, if_exists="append", index=False
        )
        dispatchers.to_sql("dispatchers", conn, if_exists="append", index=False)
        calls_df.to_sql("calls", conn, if_exists="append", index=False)

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()
        print(
            f"Synthetic data generated successfully: {len(calls_df)} calls, {len(canonical_scripts)} scripts, {len(dispatchers)} dispatchers, {len(scenarios)} scenarios."
        )

    except Exception as e:
        print(f"Error during data generation: {str(e)}")
        if "conn" in locals():
            conn.close()
        raise


if __name__ == "__main__":
    generate_synthetic_data()
import sqlite3
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from sentence_transformers import SentenceTransformer
import json


def generate_synthetic_data():
    try:
        # Инициализация модели SentenceTransformer
        model = SentenceTransformer("cointegrated/rubert-tiny2")

        # Подключение к базе данных
        conn = sqlite3.connect("data/dispatcher_quality.db")
        cursor = conn.cursor()

        # Очистка существующих таблиц
        cursor.execute("DELETE FROM calls")
        cursor.execute("DELETE FROM canonical_scripts")
        cursor.execute("DELETE FROM dispatchers")
        cursor.execute("DELETE FROM scenarios")
        conn.commit()

        # 1. Генерация сценариев
        scenarios = pd.DataFrame(
            [
                {"id": 1, "name": "Обработка заказа"},
                {"id": 2, "name": "Техническая поддержка"},
                {"id": 3, "name": "Консультация клиента"},
            ]
        )

        # 2. Генерация канонических скриптов
        canonical_scripts = pd.DataFrame(
            [
                {
                    "scenario_id": 1,
                    "script_text": "Здравствуйте, это диспетчерская служба. Чем могу помочь? Пожалуйста, назовите номер вашего заказа. Спасибо, заказ принят. До свидания.",
                },
                {
                    "scenario_id": 1,
                    "script_text": "Добрый день! Это диспетчерская служба. Назови номер заказа, пожалуйста. Заказ подтверждён, спасибо!",
                },
                {
                    "scenario_id": 2,
                    "script_text": "Добрый день, это техническая поддержка. Опишите вашу проблему. Мы решим её в ближайшее время. Спасибо за обращение.",
                },
                {
                    "scenario_id": 2,
                    "script_text": "Здравствуйте, техподдержка. В чём проблема? Мы разберёмся и свяжемся с вами. До свидания.",
                },
                {
                    "scenario_id": 3,
                    "script_text": "Здравствуйте, я диспетчер. Чем могу помочь? Расскажите о вашем вопросе, я постараюсь ответить. Спасибо за звонок!",
                },
            ]
        )
        canonical_scripts["embedding"] = canonical_scripts["script_text"].apply(
            lambda x: json.dumps(model.encode(x).tolist())
        )
        canonical_scripts["id"] = range(1, len(canonical_scripts) + 1)

        # 3. Генерация диспетчеров
        dispatchers = pd.DataFrame({"name": [f"Диспетчер {i+1}" for i in range(5)]})
        dispatchers["id"] = range(1, len(dispatchers) + 1)

        # 4. Генерация звонков (~100,000)
        transcript_variants = {
            "good": [
                "Здравствуйте, это диспетчерская служба. Назови номер заказа, пожалуйста. Заказ принят, спасибо!",
                "Добрый день! Чем могу помочь? Назови номер заказа. Всё, заказ подтверждён.",
            ],
            "medium": [
                "Привет, это диспетчерская. Какой у вас заказ? Ок, записал.",
                "Здравствуйте, диспетчер. Что надо? Назови номер, я запишу.",
            ],
            "poor": [
                "Алло, что надо? Заказ? Ну, ладно, давай номер.",
                "Привет, говори быстро, что там у тебя?",
            ],
        }

        num_dispatchers = len(dispatchers)
        calls_per_dispatcher = (
            100000 // num_dispatchers
        )  # ~20,000 звонков на диспетчера
        calls = []
        start_date = datetime.now() - timedelta(days=7)

        for disp_id in dispatchers["id"]:
            for _ in range(calls_per_dispatcher):
                scenario_id = random.choice([1, 2, 3])
                quality_type = random.choices(
                    ["good", "medium", "poor"], weights=[0.5, 0.3, 0.2], k=1
                )[0]
                transcript = random.choice(transcript_variants[quality_type])
                random_date = start_date + timedelta(
                    seconds=random.randint(0, 7 * 24 * 60 * 60)
                )
                calls.append(
                    {
                        "dispatcher_id": disp_id,
                        "scenario_id": scenario_id,
                        "date_time": random_date.strftime("%Y-%m-%d %H:%M:%S"),
                        "transcript_text": transcript,
                        "quality_score": None,
                    }
                )

        calls_df = pd.DataFrame(calls)
        calls_df["id"] = range(1, len(calls_df) + 1)

        # 5. Сохранение данных в SQLite
        scenarios.to_sql("scenarios", conn, if_exists="replace", index=False)
        canonical_scripts[["id", "scenario_id", "script_text", "embedding"]].to_sql(
            "canonical_scripts", conn, if_exists="replace", index=False
        )
        dispatchers.to_sql("dispatchers", conn, if_exists="replace", index=False)
        calls_df.to_sql("calls", conn, if_exists="replace", index=False)

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()
        print(
            f"Synthetic data generated successfully: {len(calls_df)} calls, {len(canonical_scripts)} scripts, {len(dispatchers)} dispatchers, {len(scenarios)} scenarios."
        )
    except Exception as e:
        print(f"Error during data generation: {str(e)}")
        if "conn" in locals():
            conn.close()
        raise


if __name__ == "__main__":
    generate_synthetic_data()
