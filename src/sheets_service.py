import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials
import json

class SheetsService:
    def __init__(self):
        load_dotenv()

        self.sheet_name = os.getenv("GOOGLE_SHEET_NAME", "").strip()
        self.worksheet_name = os.getenv("WORKSHEET_NAME", "").strip()

        print("Sheet:", self.sheet_name)
        print("Worksheet:", self.worksheet_name)

        self.client = self._connect()
        self.sheet = self.client.open(self.sheet_name)
        self.worksheet = self.sheet.worksheet(self.worksheet_name)

    def _connect(self):
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds_json = os.getenv("GOOGLE_CREDENTIALS")

        if not creds_json:
            raise ValueError("No se encontró GOOGLE_CREDENTIALS en variables de entorno")

        creds_dict = json.loads(creds_json)

        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=scope
        )

        return gspread.authorize(creds)

    def get_input_data(self):
        data = self.worksheet.get_all_values()

        headers = data[2]
        rows = data[3:]

        headers = [h if h != "" else f"col_{i}" for i, h in enumerate(headers)]

        records = []
        for idx, row in enumerate(rows, start=4):
            record = dict(zip(headers, row))
            record["_row"] = idx
            records.append(record)

        return records


    def update_prices(self, data):
        headers = self.worksheet.row_values(3)
        col_map = {name: idx for idx, name in enumerate(headers)}

        tcg_col = col_map["P.TCGPLAYER"] + 1
        colectr_col = col_map["P.COLECTR"] + 1

        requests = []

        for row in data:
            row_number = row["_row"]

            requests.append({
                "range": gspread.utils.rowcol_to_a1(row_number, tcg_col),
                "values": [[row["price_tcg"]]]
            })

            requests.append({
                "range": gspread.utils.rowcol_to_a1(row_number, colectr_col),
                "values": [[row["price_colectr"]]]
            })

        self.worksheet.batch_update(requests,value_input_option="USER_ENTERED")