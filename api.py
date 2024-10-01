from fastapi import FastAPI
from pydantic import BaseModel, Field
import sqlite3
from typing import List, Optional
import uvicorn

app = FastAPI(
    title="RAM Usage API",
    description="API for monitoring and retrieving RAM usage statistics.",
    version="1.0.0"
)

def get_db_connection():
    connection = sqlite3.connect('ram_usage.db')
    connection.row_factory = sqlite3.Row
    return connection

class RAMUsage(BaseModel):
    total: int = Field(..., description="Total RAM in MB")
    used: int = Field(..., description="Used RAM in MB")
    free: int = Field(..., description="Free RAM in MB")
    timestamp: str = Field(..., description="Timestamp of the record")

@app.get("/ram-usage", response_model=List[RAMUsage],
         description="Retrieve RAM usage data.",
         responses={200: {"description": "A list of RAM usage records"}})
async def get_last_ram_usage(limit: Optional[int] = 10):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT total, used, free, timestamp FROM ram_usage ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    ram_usage_list = [
        RAMUsage(total=row['total'], used=row['used'], free=row['free'], timestamp=row['timestamp'])
        for row in rows
    ]

    connection.close()
    return ram_usage_list

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
