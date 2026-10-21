import sqlite3
from pathlib import Path

DATABASE_PATH = f"{Path(__file__).resolve().parent}/log_DB_store/sqlit3LogDB.db"
print(DATABASE_PATH)
def initialise_fts_db():
    """Create a persistant FTS5 table if does noyt exists already."""
    conn = sqlite3.connect(DATABASE_PATH)

    try:
        conn.execute("""CREATE VIRTUAL TABLE IF NOT EXISTS logs_ftss USING FTS5(
        chunk_id UNINDEXED,
        file_id UNINDEXED,
        start UNINDEXED,
        end UNINDEXED,
        start_line UNINDEXED,
        end_line UNINDEXED,
        version UNINDEXED,
        file_name UNINDEXED,
        file_path UNINDEXED,
        log_category UNINDEXED,
        text
        )""")

        conn.commit()
    finally:
        conn.close()

def insert_chunks(file_id,file_name,file_path,log_category,chunks,verbose=True):
    """Insert chunks into the sql FTS table, the same that are inserted into vector DB."""

    if not chunks:
        raise ValueError("Cannot index empty chunk list.")

    try:
        initialise_fts_db()
        
        conn = sqlite3.connect(DATABASE_PATH)

        conn.execute("BEGIN IMMEDIATE")
        result = conn.execute("""SELECT COALESCE(MAX(VERSION),0) FROM logs_ftss WHERE file_id = ?""", (file_id,)).fetchone()
    
        if verbose:
            print(f"version fetch result: {result}")
    
        current_version = result[0]+1
    
        rows=[] 
    
        for id,chunk in enumerate(chunks):
            metadata = chunk["meta_data"].copy()
            rows.append((
                f"{file_id}_{id}",
                file_id,
                metadata["Start Index"],
                metadata["End Index"],
                metadata["Start Line"],
                metadata["End Line"],
                current_version,
                file_name,
                file_path,
                log_category,
                chunk["text"]
            ))   

            if verbose:
                print(f"rows: {rows}")
    
            conn.executemany("""INSERT INTO logs_ftss(
                    chunk_id,
                    file_id,
                    start,
                    end,
                    start_line,
                    end_line,
                    version,
                    file_name,
                    file_path,
                    log_category,
                    text
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?)""", rows)

            conn.commit()

    except Exception as e:
            conn.rollback()
            raise        

    insertCheckResult = conn.execute("""SELECT COUNT(*) FROM logs_ftss WHERE file_id = ? AND version = ?""",(file_id,current_version)).fetchall()

    if verbose:
        print(f"insertCheckResult:: {insertCheckResult}")
    if insertCheckResult:
        conn.execute("""DELETE FROM logs_ftss where file_id = ? and CAST(version AS INTEGER) < ?""",(file_id,current_version))
    
    conn.close()
    return insertCheckResult

        











