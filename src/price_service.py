from playwright.sync_api import sync_playwright
class TCG_Player:
    def launch_player(self):
        self.p = sync_playwright().start()
        import os

        headless_mode = os.getenv("HEADLESS", "true").lower() == "true"

        self.browser = self.p.chromium.launch(headless=headless_mode)
    
        self.page = self.browser.new_page()
        self.page.goto("https://www.tcgplayer.com/")

    def get_tcg_price(self,card_name):
        try: 
            #Busqueda directa por URL
            query = card_name.replace(" ", "+")
            url = f"https://www.tcgplayer.com/search/all/product?q={query}&view=grid"
            self.page.goto(url)
            #espera a que cargue la pagina
            self.page.wait_for_selector(".search-result",timeout=20000)

            #revision del precio del primer resultado
            self.page.wait_for_selector("a[data-testid^='product-card__image']",timeout=10000)
            first_product = self.page.locator("a[data-testid^='product-card__image']").first
            price = first_product.locator(".product-card__market-price--value").inner_text()
            result_name = first_product.locator(".product-card__title").inner_text().strip()
            print(card_name)
            print(result_name)
            print(price)
            price_float=float(price.replace("$", "").replace(",", ""))

            return price_float
        except Exception as e:
            print(f"❌ Error con '{card_name}': {e}")
            return ("no encontrado")

    def get_colectr_price(self, card_name):
        try:
            query = card_name.replace(" ", "+")
            url = f"https://app.getcollectr.com/?query={query}"
            self.page.goto(url)

            self.page.wait_for_selector(
                "div.cursor-pointer:has(span.font-bold)",
                timeout=15000
            )

            cards = self.page.locator("div.cursor-pointer:has(span.font-bold)")

            for i in range(cards.count()):
                card = cards.nth(i)

                # Nombre
                name = card.locator("span.font-bold").first.inner_text().strip()

                # Precio (solo el que tiene $)
                price_locator = card.locator("span.font-bold:has-text('$')")

                if price_locator.count() == 0:
                    continue

                price_text = price_locator.inner_text()

                print("MATCH:")
                print(name)
                print(price_text+"\n")

                price = float(price_text.replace("$", "").replace(",", ""))

                return price

            return "no encontrado"

        except Exception as e:
            print(f"❌ Error con '{card_name}': {e}")
            return "no encontrado"

    def Close_player(self):
        self.browser.close()
        self.p.stop()