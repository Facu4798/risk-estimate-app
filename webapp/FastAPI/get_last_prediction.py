# get_last_prediction.py
from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector

def get_last_prediction():
    creds = Credentials().load(path="/code/db_dev.json")
    conn = MySQLConnector(creds.dict)
    conn.connect()
    query = "SELECT * FROM predicciones ORDER BY Date DESC LIMIT 1"
    df = conn.get_data(query)
    conn.close()
    if df.empty:
        return None
    fila = df.iloc[0]
    return {
        "Ticker": fila["Ticker"],
        "5Days": float(fila["5Days"]),
        "10Days": float(fila["10Days"]),
        "30Days": float(fila["30Days"])
    }

