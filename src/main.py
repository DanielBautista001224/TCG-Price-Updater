from sheets_service import get_input_data, uptade_prices
from price_service import TCG_Player

def main():
    input_data = get_input_data()
    results = []
    tcg=TCG_Player()
    tcg.launch_tcg_player()
    for row in input_data:
        card_name = row.get("NOMBRE DE LA CARTA")
        if not card_name or str(card_name).strip() == "":
            
            continue

        price_usd = tcg.get_card_price(card_name+" "+row["NRO"]+" "+row["COLECCIÓN"])
        # price_cop = round(price_usd * 4000, 2)

        results.append({
            "_row": row["_row"],  
            "card_name": row["NOMBRE DE LA CARTA"],
            "set": row["COLECCIÓN"],
            "condition": row["NRO"],
            "price_usd": price_usd,
            #"price_cop": price_cop,
            "source": "mock"
        })
    tcg.Close_tcg_player()
    uptade_prices(results)
    print("Precios actualizados")

if __name__ == "__main__":
    main()