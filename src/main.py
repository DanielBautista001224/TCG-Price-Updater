from sheets_service import get_input_data, uptade_prices
from price_service import get_mock_price

def main():
    input_data = get_input_data()
    results = []

    for row in input_data:
        price_usd = get_mock_price(row["NOMBRE DE LA CARTA"])
        price_cop = round(price_usd * 4000, 2)

        results.append({
            "_row": row["_row"],  
            "card_name": row["NOMBRE DE LA CARTA"],
            "set": row["COLECCIÓN"],
            "condition": row["NRO"],
            "price_usd": price_usd,
            "price_cop": price_cop,
            "source": "mock"
        })

    uptade_prices(results)
    print("Precios actualizados 🚀")

if __name__ == "__main__":
    main()