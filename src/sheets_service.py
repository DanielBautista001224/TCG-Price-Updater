import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

load_dotenv()
SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME")
WORKSHEET_NAME = os.getenv("WORKSHEET_NAME")

def connect_to_sheets():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=scope
    )

    client = gspread.authorize(creds)
    return client


def get_input_data():
    client = connect_to_sheets()
    sheet = client.open(SHEET_NAME)
    worksheet = sheet.worksheet(WORKSHEET_NAME)
    data = worksheet.get_all_values()

    headers = data[2]  
    rows = data[3:]    
    
    headers = [h if h != "" else f"col_{i}" for i, h in enumerate(headers)]
    records = []

    for idx, row in enumerate(rows, start=4):  
        record = dict(zip(headers, row))
        record["_row"] = idx  
        records.append(record)

    return records

def uptade_prices(data):
    client = connect_to_sheets()
    sheet = client.open(SHEET_NAME).worksheet(WORKSHEET_NAME)

    headers = sheet.row_values(3)
    col_map = {name: idx for idx, name in enumerate(headers)}

    usd_col = col_map["P.TCGPLAYER"]+1
    requests=[]
    
    for row in data:
        row_number = row["_row"]

        requests.append({
            "range": f"{gspread.utils.rowcol_to_a1(row_number, usd_col)}",
            "values": [[row["price_usd"]]]
        })

    sheet.batch_update(requests, value_input_option="USER_ENTERED")

