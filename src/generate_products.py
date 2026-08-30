from faker import Faker
import pandas as pd
import random
import os

fake = Faker("pt_BR")


# ============================================================
# CATÁLOGO BASE
# ============================================================

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


# ============================================================
# VARIAÇÕES POR CATEGORIA
# ============================================================

variations = {

    "Smartphones": [
        ("128GB", 1.00),
        ("256GB", 1.10),
        ("512GB", 1.25),
        ("128GB - Azul", 1.00),
        ("128GB - Preto", 1.00),
    ],

    "Periféricos": [
        ("Preto", 1.00),
        ("Branco", 1.02),
        ("Cinza", 1.02),
        ("RGB", 1.08),
        ("Wireless", 1.20),
    ],

    "Monitores": [
        ("24\"", 1.00),
        ("27\"", 1.15),
        ("27\" - 144Hz", 1.25),
        ("27\" - 165Hz", 1.30),
        ("32\"", 1.45),
    ],

    "Games": [
        ("Standard", 1.00),
        ("Digital", 0.95),
        ("Bundle", 1.12),
        ("+ Jogo", 1.15),
        ("+ Controle", 1.18),
    ],

    "Acessórios": [
        ("Preto", 1.00),
        ("Branco", 1.02),
        ("Azul", 1.02),
        ("Premium", 1.10),
        ("Kit 2 unidades", 1.75),
    ],

    "Áudio": [
        ("Preto", 1.00),
        ("Branco", 1.02),
        ("Azul", 1.02),
        ("Vermelho", 1.02),
        ("Premium", 1.10),
    ],

    "Cadeiras": [
        ("Preta", 1.00),
        ("Cinza", 1.02),
        ("Branca", 1.03),
        ("Azul", 1.03),
        ("Vermelha", 1.03),
    ]
}


# ============================================================
# FUNÇÃO PARA ADICIONAR PRODUTO
# ============================================================

products = []


def add_product(name, category, base_price, variation_multiplier):

    # Pequena variação comercial no preço
    price_variation = random.uniform(0.97, 1.03)

    price = round(
        base_price * variation_multiplier * price_variation,
        2
    )

    # Margem de lucro baseada no preço do produto
    if price < 200:
        margin = random.uniform(0.20, 0.40)

    elif price < 1000:
        margin = random.uniform(0.18, 0.35)

    elif price < 3000:
        margin = random.uniform(0.15, 0.28)

    else:
        margin = random.uniform(0.10, 0.22)

    custo = round(
        price * (1 - margin),
        2
    )

    products.append({
        "name": name,
        "category": category,
        "price": price,
        "custo": custo
    })


# ============================================================
# GERANDO OS PRODUTOS
# ============================================================

for category, catalog in products_catalog.items():

    category_variations = variations[category]

    for product_name, base_price in catalog:

        for variation_name, multiplier in category_variations:

            # Evita nomes estranhos como:
            # "Monitor Samsung T350 24 24\""
            if variation_name in product_name:
                final_name = product_name

            else:
                final_name = f"{product_name} {variation_name}"

            add_product(
                name=final_name,
                category=category,
                base_price=base_price,
                variation_multiplier=multiplier
            )


# ============================================================
# DATAFRAME
# ============================================================

df_products = pd.DataFrame(products)


# ============================================================
# LIMITAR PARA 200 PRODUTOS
# ============================================================

df_products = df_products.sample(
    n=200,
    random_state=42
).reset_index(drop=True)


# Criar ID depois de selecionar os produtos
df_products.insert(
    0,
    "id_product",
    range(1, len(df_products) + 1)
)


# ============================================================
# ORGANIZAR COLUNAS
# ============================================================

df_products = df_products[
    [
        "id_product",
        "name",
        "category",
        "price",
        "custo"
    ]
]


# ============================================================
# ORDENAÇÃO
# ============================================================

df_products = df_products.sort_values(
    by=["category", "name"]
).reset_index(drop=True)


# Recriar IDs depois da ordenação
df_products["id_product"] = range(
    1,
    len(df_products) + 1
)


# ============================================================
# VISUALIZAÇÃO
# ============================================================

print("\n===== PRODUTOS =====\n")
print(df_products)


print("\n===== QUANTIDADE POR CATEGORIA =====\n")
print(
    df_products["category"].value_counts()
)


print("\n===== TOTAL DE PRODUTOS =====\n")
print(
    len(df_products)
)


# ============================================================
# CRIAR PASTA DATA/RAW
# ============================================================

os.makedirs(
    "data/raw",
    exist_ok=True
)


# ============================================================
# EXPORTAR CSV
# ============================================================

df_products.to_csv(
    "data/raw/products.csv",
    index=False,
    encoding="utf-8-sig"
)


print("\nCSV gerado com sucesso!")
print("Arquivo: data/raw/products.csv")