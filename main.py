from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import psycopg2
from psycopg2.extras import RealDictCursor
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# データベース設定
DB_CONFIGS = {
    "crm": {
        "host": "localhost",
        "port": 5432,
        "user": "crm_user",
        "password": "crm123",
        "database": "crm"
    },
    "productmaster": {
        "host": "localhost",
        "port": 5432,
        "user": "productmaster_user",
        "password": "productmaster123",
        "database": "productmaster"
    },
    "aichat": {
        "host": "localhost",
        "port": 5432,
        "user": "aichat_user",
        "password": "aichat123",
        "database": "aichat"
    }
}

def get_db_connection(db_name="crm"):
    """データベース接続"""
    try:
        config = DB_CONFIGS.get(db_name, DB_CONFIGS["crm"])
        connection = psycopg2.connect(**config)
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """メインページ"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/tables/{db_name}")
async def get_tables(db_name: str):
    """テーブル一覧取得"""
    try:
        connection = get_db_connection(db_name)
        if not connection:
            return {"status": "error", "error": f"データベース接続エラー ({db_name})"}
        
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
        tables = cursor.fetchall()
        connection.close()
        
        return {
            "status": "success",
            "tables": [table["table_name"] for table in tables]
        }
    except Exception as e:
        if "connection" in locals():
            connection.close()
        return {"status": "error", "error": str(e)}

@app.post("/api/execute-sql")
async def execute_sql(request: Request):
    """手動SQL実行"""
    try:
        data = await request.json()
        sql = data.get("sql", "").strip()
        db_name = data.get("database", "crm")
        
        if not sql:
            return {"status": "error", "error": "SQLクエリが空です"}
        
        connection = get_db_connection(db_name)
        if not connection:
            return {"status": "error", "error": f"データベース接続エラー ({db_name})"}
        
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sql)
        
        # SELECT系のクエリの場合結果を取得
        if sql.upper().strip().startswith(("SELECT", "WITH", "SHOW")):
            results = cursor.fetchall()
            results_list = [dict(row) for row in results]
            connection.commit()
            connection.close()
            return {
                "status": "success",
                "results": results_list,
                "count": len(results_list)
            }
        else:
            # INSERT/UPDATE/DELETE系のクエリ
            connection.commit()
            affected_rows = cursor.rowcount
            connection.close()
            return {
                "status": "success",
                "message": f"{affected_rows}行が影響されました",
                "count": affected_rows
            }
            
    except Exception as e:
        if "connection" in locals():
            connection.rollback()
            connection.close()
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8006)
