import pandas as pd
import random
import os


SALES_FILE = "data/raw/sales.csv"
PRODUCTS_FILE = "data/raw/products.csv"

OUTPUT_FILE = "data/raw/items_sales.csv"

df_sales = pd.read_csv(SALES_FILE)
df_products = pd.read_csv(PRODUCTS_FILE)

products = df_products.to_dict("records")


# ============================================================
# PRODUTOS POR CATEGORIA
# ============================================================

products_by_category = {}

for product in products:

    category = product["category"]

    if category not in products_by_category:

        products_by_category[category] = []

    products_by_category[category].append(product)


categories = list(products_by_category.keys())



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


def choose_first_product():

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


def choose_related_product(
    main_product,
    selected_product_ids
):

    main_category = main_product["category"]

    possible_categories = related_categories.get(
        main_category,
        categories
    )


    possible_categories = [

        category

        for category in possible_categories

        if category in products_by_category

    ]


    if not possible_categories:

        possible_categories = categories


    category = random.choice(
        possible_categories
    )


    possible_products = [

        product

        for product in products_by_category[category]

        if product["id_product"] not in selected_product_ids

    ]


    # Caso todos os produtos daquela categoria já estejam
    # na venda, escolhe qualquer produto disponível.

    if not possible_products:

        possible_products = [

            product

            for product in products

            if product["id_product"] not in selected_product_ids

        ]


    return random.choice(
        possible_products
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

    probability = random.random()


    # 70% sem desconto
    if probability < 0.70:

        return 0.00


    # 15% desconto pequeno
    elif probability < 0.85:

        return round(
            random.uniform(
                5,
                min(20, price * 0.05)
            ),
            2
        )


    # 10% desconto médio
    elif probability < 0.95:

        return round(
            random.uniform(
                20,
                min(80, price * 0.10)
            ),
            2
        )


    # 5% desconto maior
    else:

        return round(
            random.uniform(
                50,
                min(300, price * 0.15)
            ),
            2
        )




items_sales = []

id_item_sale = 1


for _, sale in df_sales.iterrows():

    id_sale = int(
        sale["id_sale"]
    )



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




    main_product = choose_first_product()


    selected_product_ids = {

        int(main_product["id_product"])

    }



    quantity = generate_quantity(
        main_product
    )


    discount = generate_discount(
        main_product["price"]
    )


    items_sales.append({

        "id_item_sale": id_item_sale,

        "id_sale": id_sale,

        "id_product": int(
            main_product["id_product"]
        ),

        "quantity": quantity,

        "unity_price": round(
            main_product["price"],
            2
        ),

        "discount": discount

    })


    id_item_sale += 1




    for _ in range(
        number_of_products - 1
    ):

        related_product = choose_related_product(

            main_product,

            selected_product_ids

        )


        product_id = int(
            related_product["id_product"]
        )


 
        if product_id in selected_product_ids:

            continue


        selected_product_ids.add(
            product_id
        )


        quantity = generate_quantity(
            related_product
        )


        discount = generate_discount(
            related_product["price"]
        )


        items_sales.append({

            "id_item_sale": id_item_sale,

            "id_sale": id_sale,

            "id_product": product_id,

            "quantity": quantity,

            "unity_price": round(
                related_product["price"],
                2
            ),

            "discount": discount

        })


        id_item_sale += 1


df_items_sales = pd.DataFrame(
    items_sales
)


df_items_sales = df_items_sales[

    [
        "id_item_sale",
        "id_sale",
        "id_product",
        "quantity",
        "unity_price",
        "discount"
    ]

]


df_items_sales.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"

)
