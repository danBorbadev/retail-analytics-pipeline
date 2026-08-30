from faker import Faker
import pandas as pd
import random

fake = Faker("pt_BR")

products_catalog = {

    "Smartphones": [
        ("Samsung Galaxy A15", 899.90),
        ("Samsung Galaxy A35", 1699.90),
        ("Samsung Galaxy S24", 3999.90),
        ("Apple iPhone 13", 3499.90),
        ("Apple iPhone 15", 4299.90),
        ("Motorola Moto G54", 1199.90),
        ("Motorola Edge 50", 2499.90),
        ("Xiaomi Redmi Note 13", 1399.90),
    ],

    "Periféricos": [
        ("Mouse Logitech M170", 79.90),
        ("Mouse Logitech G203", 179.90),
        ("Teclado Logitech K120", 89.90),
        ("Teclado Redragon Kumara", 229.90),
        ("Headset HyperX Cloud Stinger", 299.90),
        ("Mousepad Havit", 59.90),
    ],

    "Monitores": [
        ("Monitor LG 24MK430H", 799.90),
        ("Monitor Samsung T350 24", 899.90),
        ("Monitor AOC 24G2", 1199.90),
        ("Monitor LG UltraGear 27", 1599.90),
        ("Monitor Samsung Odyssey G5", 2499.90),
    ],

    "Games": [
        ("PlayStation 5 Slim", 3499.90),
        ("Xbox Series S", 2299.90),
        ("Nintendo Switch OLED", 2199.90),
        ("Controle DualSense PS5", 449.90),
        ("Controle Xbox Wireless", 499.90),
    ],

    "Acessórios": [
        ("Cabo USB-C Baseus", 49.90),
        ("Carregador Samsung 25W", 99.90),
        ("Carregador Apple 20W", 189.90),
        ("Hub USB-C 6 em 1", 159.90),
        ("Suporte para Notebook", 129.90),
        ("Webcam Logitech C920", 499.90),
    ],

    "Áudio": [
        ("JBL Tune 520BT", 249.90),
        ("JBL Flip 6", 699.90),
        ("Sony WH-CH520", 299.90),
        ("Sony WH-1000XM5", 2299.90),
        ("Edifier W820NB", 399.90),
        ("JBL Go 3", 299.90),
    ],

    "Cadeiras": [
        ("Cadeira Gamer ThunderX3", 1299.90),
        ("Cadeira Gamer Fortrek", 899.90),
        ("Cadeira Office Flexform", 1599.90),
        ("Cadeira Ergonômica Elements", 2199.90),
        ("Cadeira Gamer Husky", 1499.90),
    ]
}

products = []

for i in range(1,201):
    category = random.choice(list(products_catalog.keys()))

    product_name, base_price = random.choice(
        products_catalog[category]
    )

    custo = round(base_price * random.uniform(0.65, 0.85), 2)
    price = round(base_price * random.uniform(0.90, 1.10), 2)

    products.append({
        "id_product": i,
        "name": product_name,
        "category": category,
        "price": price,
        "custo": custo
    })

df_products = pd.DataFrame(products)

print(df_products)


# Gerar CSV

df_products.to_csv(
    "data/raw/products.csv",
    index=False,
    encoding="utf-8-sig"
)