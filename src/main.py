from sheets_service import SheetsService
from price_service import TCG_Player

def main():
    sheets=SheetsService()
    input_data = sheets.get_input_data()
    results = []
    tcg=TCG_Player()
    tcg.launch_player()

    for row in input_data:
        card_name = row.get("NOMBRE DE LA CARTA")
        if not card_name or str(card_name).strip() == "":
            continue

        price_tcg = tcg.get_tcg_price(card_name+" "+row["NRO"]+" "+row["COLECCIÓN"])
        price_colectr = tcg.get_colectr_price(card_name+" "+row["NRO"])

        results.append({
            "_row": row["_row"],  
            "price_tcg": price_tcg,
            "price_colectr": price_colectr,
        })
    tcg.Close_player()
    sheets.update_prices(results)
    print("Precios actualizados")

if __name__ == "__main__":
    main()