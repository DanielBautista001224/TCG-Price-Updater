from playwright.sync_api import sync_playwright
class TCG_Player:
    def launch_tcg_player(self):
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        self.page.goto("https://www.tcgplayer.com/")


    def get_card_price(self,card_name):
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



    def Close_tcg_player(self):
        self.browser.close()
        self.p.stop()