import os
import sys
import psycopg2

DEFAULT_URL = "postgresql://sardargiantscloud_user:7KxfRos1KRtX9lSMjdV9KoNQLiZCOktr@dpg-dbd3cggn74is738283m0-a.oregon-postgres.render.com/sardargiantscloud"

def run_query(sql=None):
    db_url = os.environ.get("DATABASE_URL", DEFAULT_URL)
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    if not sql:
        sql = "SELECT id, name, email, role, allocated_storage, created_on FROM users;"
        print("--- Querying Users Table ---")
    else:
        print(f"--- Executing: {sql} ---")
        
    cur.execute(sql)
    
    if cur.description:
        cols = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        
        # Calculate column widths
        col_widths = [max(len(col), max([len(str(r[i])) for r in rows], default=0)) for i, col in enumerate(cols)]
        
        # Header
        header = " | ".join(col.ljust(col_widths[i]) for i, col in enumerate(cols))
        sep = "-+-".join("-" * col_widths[i] for i in range(len(cols)))
        print(header)
        print(sep)
        
        # Rows
        for row in rows:
            print(" | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)))
        print(f"\n({len(rows)} rows)")
    else:
        conn.commit()
        print("Query executed successfully (no rows returned).")
        
    cur.close()
    conn.close()

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else None
    run_query(query)
