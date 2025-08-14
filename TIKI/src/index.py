from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from config import setup
from pymongo import MongoClient
from Database import MONGO_URI,MONGO_DB,MONGO_COLLECTION
from datetime import datetime

class Tiki(webdriver.Chrome):
    def __init__(self):
        option = setup()
        super().__init__(options=option)
        self.implicitly_wait(15)
        self.database()
    def website(self):
        url = ("https://tiki.vn/khuyen-mai/tikivip-khach-hang-than-thiet?utm_source=facebook-non-cpas&utm_medium=os_partner_tms&utm_campaign=COM_OPS_FB_IMG_BRAND-TIKIVN-KHACHHANGTHANTHIETTIKIVIP_All_VN_ALL_UNK_UNK_X.%7B%7Bcampaign.id%7D%7D_Y.%7B%7Badset.id%7D%7D_Z.%7B%7Bad.id%7D%7D_TMSX.bb9decf1-50d9-4039-b1de-1d1924df5b87&tclid=e7f1c6af-fb59-41f7-8c6e-b8386e8a0545")
        self.get(url)
    
    def database(self):
        client =MongoClient(MONGO_URI)
        db =client[MONGO_DB]
        self.collection =db[MONGO_COLLECTION]

    def scroll(self, element):
        self.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", element)
        sleep(1)

    def Product(self):
        try:
            products = self.find_elements(By.CSS_SELECTOR, 'div[data-brick-type="PRODUCT"]')
            return products
        except Exception as e:
            print(f"Error products: {e}")
            return []
    def insertData(self, data):
        product = self.collection.find_one({"name": data["name"], "link": data["link"]})
        if not product:
            self.collection.insert_one(data)
        else:
            if (product.get('price') != data['price'] or product.get('discount') != data['discount'] or product.get('original_price') != data['original_price']):
                self.collection.insert_one(data)
    def item(self, products):
        all_products = []
        try:
            for i, product in enumerate(products):
                self.scroll(product)
                items = product.find_elements(By.CSS_SELECTOR, 'a[data-view-id="product_list_item"]')
                for item_elem in items:
                    try:
                        self.scroll(item_elem)
                        name = item_elem.find_element(By.CSS_SELECTOR, '.sc-8b415d9d-5.izNpeL')
                        sold = item_elem.find_element(By.CSS_SELECTOR, 'span.quantity.has-border')
                        price = item_elem.find_element(By.CSS_SELECTOR, 'div.price-discount__price')
                        original_price = item_elem.find_element(By.CLASS_NAME, "price-discount__original-price")
                        discount = item_elem.find_element(By.CLASS_NAME, "price-discount__discount")
                        image = item_elem.find_element(By.TAG_NAME, 'img').get_attribute("srcset").split(",")[0].split()[0]
                        link = item_elem.get_attribute('href')
                        data = {
                            'name': name.text.strip(),
                            'price': price.text.strip(),
                            'original_price': original_price.text.strip(),
                            'discount': discount.text.strip(),
                            'sold': sold.text.replace("Đã bán", "").strip(),
                            'image': image.strip(),
                            'link': link,
                            'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'Label': f"{i+1}"
                        }
                        self.insertData(data)
                        if data not in all_products:
                            all_products.append(data)
                            print(f"[Product {i+1}]: {data}")
                    except NoSuchElementException:
                        continue
            return all_products
        except Exception as e:
            print(f"Error: {e}")
            return []
if __name__ == '__main__':
    app = Tiki()
    app.website()
    products = app.Product()
    app.item(products)
    sleep(2)
    app.quit()
