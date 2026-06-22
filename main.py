from fastapi import FastAPI
from etl_main import main

app = FastAPI()

@app.post("/load-data")
def load_data():
    try:
        main()

        return {
            "status": "success",
            "message": "ETL completed successfully"
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }