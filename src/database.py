import sqlite3

# This script provides functions to interact with an SQLite database of boot parts.
# Each function retrieves distinct values from the database based on various criteria
# such as manufacturer, model, engine size, mark series, drive type, position, and transmission.

# Function List:
# - get_unique_manufacturers(db_path): Retrieves a list of unique manufacturers.
# - get_models(db_path, manufacturer): Retrieves a list of models for a given manufacturer.
# - get_engine_sizes(db_path, manufacturer, model): Retrieves a list of engine sizes for a given manufacturer and model.
# - get_mark_series(db_path, manufacturer, model, engine_size): Retrieves a list of mark series for a given manufacturer, model, and engine size.
# - get_drive_types(db_path, manufacturer, model, engine_size, mark_series): Retrieves a list of drive types for a given manufacturer, model, engine size, and mark series.
# - get_positions(db_path, manufacturer, model, engine_size, mark_series, drive_type): Retrieves a list of positions for a given manufacturer, model, engine size, mark series, and drive type.
# - get_transmissions(db_path, manufacturer, model, engine_size, mark_series, drive_type, position): Retrieves a list of transmissions for a given manufacturer, model, engine size, mark series, drive type, and position.
# - get_parts(db_path, criteria): Retrieves a list of parts based on multiple criteria.

# Note:
# The `get_unique_manufacturers` function is called from `ui_components.py` to populate the manufacturer dropdown.
# The other functions are called from `ui_logic.py` to populate subsequent dropdowns based on user selections.


import sqlite3


def get_unique_manufacturers(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT Manuf FROM wheelbearing_LSODS ORDER BY Manuf ASC")
    manufacturers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return manufacturers


def get_models(db_path, manufacturer):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT Model FROM wheelbearing_LSODS WHERE Manuf = ? ORDER BY Model ASC",
        (manufacturer,),
    )
    models = [row[0] for row in cursor.fetchall()]
    conn.close()
    return models


def get_engine_sizes(db_path, manufacturer, model):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT EngineSize FROM wheelbearing_LSODS WHERE Manuf = ? AND Model = ? ORDER BY EngineSize ASC",
        (manufacturer, model),
    )
    engine_sizes = [str(row[0]) for row in cursor.fetchall()]
    conn.close()
    return engine_sizes


def get_mark_series(db_path, manufacturer, model, engine_size):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT mark_series FROM wheelbearing_LSODS WHERE Manuf = ? AND Model = ? AND EngineSize = ? ORDER BY mark_series ASC",
        (manufacturer, model, engine_size),
    )
    mark_series = [row[0] for row in cursor.fetchall()]
    conn.close()
    return mark_series


def get_drive_types(db_path, manufacturer, model, engine_size, mark_series):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT TRWDansDRWDive FROM wheelbearing_LSODS WHERE Manuf = ? AND Model = ? AND EngineSize = ? AND mark_series = ? ORDER BY TRWDansDRWDive ASC",
        (manufacturer, model, engine_size, mark_series),
    )
    drive_types = [row[0] for row in cursor.fetchall()]
    conn.close()
    return drive_types


def get_positions(db_path, manufacturer, model, engine_size, mark_series, drive_type):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT Mpos FROM wheelbearing_LSODS WHERE Manuf = ? AND Model = ? AND EngineSize = ? AND mark_series = ? AND TRWDansDRWDive = ? ORDER BY Mpos ASC",
        (manufacturer, model, engine_size, mark_series, drive_type),
    )
    positions = [row[0] for row in cursor.fetchall()]
    conn.close()
    return positions


def get_parts(db_path, criteria):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "SELECT DISTINCT LSODS_PartNumber, Bearing_1_Size FROM wheelbearing_LSODS WHERE Manuf = ?"
    params = [criteria["manufacturer"]]

    if criteria["model"]:
        query += " AND Model = ?"
        params.append(criteria["model"])
    if criteria["engine_size"]:
        query += " AND EngineSize = ?"
        params.append(criteria["engine_size"])
    if criteria["mark_series"]:
        query += " AND mark_series = ?"
        params.append(criteria["mark_series"])
    if criteria["drive_type"]:
        query += " AND TRWDansDRWDive = ?"
        params.append(criteria["drive_type"])
    if criteria["position"]:
        query += " AND MPos = ?"
        params.append(criteria["position"])

    query += " ORDER BY LSODS_PartNumber ASC"

    cursor.execute(query, params)
    parts = cursor.fetchall()
    conn.close()
    return parts
