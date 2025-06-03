import sqlite3


def init_db():
    conn = sqlite3.connect("data/dispatcher_quality.db")
    cursor = conn.cursor()

    # Создание таблицы scenarios
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS scenarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
            )
        """
    )

    # Создание таблицы canonical_scripts
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS canonical_scripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scenario_id INTEGER NOT NULL,
            script_text TEXT NOT NULL,
            embedding TEXT,
            FOREIGN KEY (scenario_id) REFERENCES scenarios(id)
            )
    """
    )

    # Создание таблицы dispatchers
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS dispatcher (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL)
        """
    )

    # Создание таблицы calls
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dispatcher_id INTEGER,
            scenario_id INTEGER,
            date_time TEXT NOT NULL,
            transcript_text TEXT NOT NULL,
            quality_score FLOAT,
            FOREIGN KEY (dispatcher_id) REFERENCES dispatcher(id),
            FOREIGN KEY (scenario_id) REFERENCES scenarios(id))
    """
    )

    conn.commit()
    conn.close()
    print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()
    print("Database initialization script executed.")
