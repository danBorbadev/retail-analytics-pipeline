import pandas as pd
import random
import os



NUM_SALES = 50000

CUSTOMERS_FILE = "data/raw/customers.csv"
STORES_FILE = "data/raw/stores.csv"
PRODUCTS_FILE = "data/raw/products.csv"

SALES_OUTPUT = "data/raw/sales.csv"
ITEMS_OUTPUT = "data/raw/items_sales.csv"



df_customers = pd.read_csv(CUSTOMERS_FILE)
df_stores = pd.read_csv(STORES_FILE)
df_products = pd.read_csv(PRODUCTS_FILE)


customer_ids = df_customers["id_customer"].tolist()
store_ids = df_stores["id_store"].tolist()


products = df_products.to_dict("records")




products_by_category = {}

for product in products:

    category = product["category"]

    if category not in products_by_category:
        products_by_category[category] = []

    products_by_category[category].append(product)




categories = list(products_by_category.keys())


def choose_product():

    category = random.choices(
        categories,
        weights=[
            25,  # Smartphones
            18,  # Periféricos
            15,  # Acessórios
            15,  # Áudio
            10,  # Monitores
            10,  # Games
            7    # Cadeiras
        ]
    )[0]

    return random.choice(
        products_by_category[category]
    )


def generate_quantity(product):

    category = product["category"]

    if category == "Smartphones":
        return random.choices(
            [1, 2],
            weights=[98, 2]
        )[0]

    elif category == "Monitores":
        return random.choices(
            [1, 2, 3],
            weights=[90, 8, 2]
        )[0]

    elif category == "Games":
        return random.choices(
            [1, 2, 3],
            weights=[85, 12, 3]
        )[0]

    elif category == "Cadeiras":
        return random.choices(
            [1, 2],
            weights=[97, 3]
        )[0]

    else:
        return random.choices(
            [1, 2, 3, 4, 5],
            weights=[65, 20, 10, 4, 1]
        )[0]


def generate_discount(price):

    discount_probability = random.random()

    # 70% das vendas sem desconto
    if discount_probability < 0.70:
        return 0.00

    # 15% com desconto pequeno
    elif discount_probability < 0.85:
        return round(
            random.uniform(5, 20),
            2
        )

    # 10% com desconto médio
    elif discount_probability < 0.95:
        return round(
            random.uniform(20, 80),
            2
        )

    # 5% com desconto maior
    else:
        return round(
            random.uniform(80, min(300, price * 0.15)),
            2
        )

def choose_related_product(main_product, selected_products):

    category = main_product["category"]

    related_categories = {

        "Smartphones": [
            "Acessórios",
            "Áudio",
            "Periféricos"
        ],

        "Monitores": [
            "Periféricos",
            "Acessórios"
        ],

        "Games": [
            "Periféricos",
            "Áudio",
            "Acessórios"
        ],

        "Cadeiras": [
            "Periféricos"
        ],

        "Periféricos": [
            "Periféricos",
            "Acessórios"
        ],

        "Áudio": [
            "Acessórios"
        ],

        "Acessórios": [
            "Acessórios",
            "Áudio"
        ]
    }

    possible_categories = related_categories.get(
        category,
        categories
    )

    possible_categories = [
        cat for cat in possible_categories
        if cat in products_by_category
    ]

    if not possible_categories:
        return choose_product()

    related_category = random.choice(
        possible_categories
    )

    possible_products = products_by_category[
        related_category
    ]

    available_products = [
        product
        for product in possible_products
        if product["id_product"] not in selected_products
    ]

    if not available_products:
        return choose_product()

    return random.choice(
        available_products
    )



sales = []
items_sales = []

item_sale_id = 1


for sale_id in range(1, NUM_SALES + 1):

    customer_id = random.choice(
        customer_ids
    )

    store_id = random.choice(
        store_ids
    )


    payment_method = random.choices(

        [
            "PIX",
            "Cartão de Crédito",
            "Cartão de Débito",
            "Dinheiro"
        ],

        weights=[
            35,
            45,
            15,
            5
        ]

    )[0]



    sales.append({

        "id_sale": sale_id,

        "id_customer": customer_id,

        "id_store": store_id,

        "payment_method": payment_method

    })


    number_of_products = random.choices(

        [1, 2, 3, 4, 5],

        weights=[
            45,
            30,
            15,
            7,
            3
        ]

    )[0]


    selected_products = []


    first_product = choose_product()

    selected_products.append(
        first_product["id_product"]
    )


    quantity = generate_quantity(
        first_product
    )

    discount = generate_discount(
        first_product["price"]
    )

    items_sales.append({

        "id_item_sale": item_sale_id,

        "id_sale": sale_id,

        "id_product": first_product["id_product"],

        "quantity": quantity,

        "unity_price": round(
            first_product["price"],
            2
        ),

        "discount": discount

    })

    item_sale_id += 1


    for _ in range(number_of_products - 1):

        main_product = first_product

        related_product = choose_related_product(

            main_product,

            selected_products

        )


        # Evitar duplicação na mesma venda
        if related_product["id_product"] in selected_products:
            continue


        selected_products.append(
            related_product["id_product"]
        )


        quantity = generate_quantity(
            related_product
        )

        discount = generate_discount(
            related_product["price"]
        )


        items_sales.append({

            "id_item_sale": item_sale_id,

            "id_sale": sale_id,

            "id_product": related_product["id_product"],

            "quantity": quantity,

            "unity_price": round(
                related_product["price"],
                2
            ),

            "discount": discount

        })


        item_sale_id += 1


df_sales = pd.DataFrame(
    sales
)

df_items_sales = pd.DataFrame(
    items_sales
)



df_sales.to_csv(

    SALES_OUTPUT,

    index=False,

    encoding="utf-8-sig"

)


df_items_sales.to_csv(

    ITEMS_OUTPUT,

    index=False,

    encoding="utf-8-sig"

)



