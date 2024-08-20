import sqlite3


def create_indexes(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_manuf ON wheelbearing_LSODS (Manuf)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_model ON wheelbearing_LSODS (Model)")
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_engine_size ON wheelbearing_LSODS (EngineSize)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_mark_series ON wheelbearing_LSODS (mark_series)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_drive_type ON wheelbearing_LSODS (TRWDansDRWDive)"
    )
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_mpos ON wheelbearing_LSODS (Mpos)")
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_transmission ON wheelbearing_LSODS (Transmission)"
    )

    conn.commit()
    conn.close()
