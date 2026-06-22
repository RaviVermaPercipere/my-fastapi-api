from fastapi import FastAPI
from utils.postgres_utils import connect_postgres
import pandas as pd
import numpy as np

app = FastAPI()

@app.get("/get-data")
def get_data():

    engine = connect_postgres()

    query = """
    SELECT *
    FROM "VKABTEST"
    LIMIT 1000
    """

    df = pd.read_sql(query, engine)

    # Replace NaN with None
    df = df.replace({np.nan: None})

    return df.to_dict(orient="records")