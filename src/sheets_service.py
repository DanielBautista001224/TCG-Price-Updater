import gspread
from google.oauth2.service_account import Credentials

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
    sheet = client.open("pokemon-price-bot")
    worksheet = sheet.worksheet("Carpeta 1")
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
    sheet = client.open("pokemon-price-bot").worksheet("Carpeta 1")

    headers = sheet.row_values(3)
    col_map = {name: idx for idx, name in enumerate(headers)}

    usd_col = col_map["P.TCGPLAYER"]
    cop_col = col_map["Precio COP"]

    # Obtener todos los valores actuales
    all_data = sheet.get_all_values()

    
    for row in data:
        row_index = row["_row"] - 1  

        all_data[row_index][usd_col] = row["price_usd"]
        all_data[row_index][cop_col] = row["price_cop"]

    
    sheet.update("A1", all_data, value_input_option="USER_ENTERED")

    print("✅ precios actualizados (modo eficiente)")