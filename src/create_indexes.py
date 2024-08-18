import sqlite3


def create_indexes(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_manuf ON boots (Manuf)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_model ON boots (Model)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_engine_size ON boots (EngineSize)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_mark_series ON boots (MarkSeries)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_trans_drive ON boots (TransDrive)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_mpos ON boots (MPos)")
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_transmission ON boots (Transmission)"
    )

    conn.commit()
    conn.close()
