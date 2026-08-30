from faker import Faker
import pandas as pd
import random

fake = Faker("pt_BR")

stores_catalog = [
    ("TechStore Vitória", "Vitória", "Brasil"),
    ("TechStore Vila Velha", "Vila Velha", "Brasil"),
    ("TechStore Serra", "Serra", "Brasil"),
    ("TechStore Cariacica", "Cariacica", "Brasil"),
    ("TechStore Linhares", "Linhares", "Brasil"),
    ("TechStore Colatina", "Colatina", "Brasil"),
    ("TechStore Cachoeiro", "Cachoeiro de Itapemirim", "Brasil"),
    ("TechStore São Paulo", "São Paulo", "Brasil"),
    ("TechStore Campinas", "Campinas", "Brasil"),
    ("TechStore Santos", "Santos", "Brasil"),
    ("TechStore Rio", "Rio de Janeiro", "Brasil"),
    ("TechStore Niterói", "Niterói", "Brasil"),
    ("TechStore Belo Horizonte", "Belo Horizonte", "Brasil"),
    ("TechStore Curitiba", "Curitiba", "Brasil"),
    ("TechStore Porto Alegre", "Porto Alegre", "Brasil"),
]


stores = []

for i, store in enumerate(stores_catalog, start=1):
    store_name, city, country = store 
    stores.append({
        "id_store": i,
        "store_name": store_name,
        "city": city,
        "Country": country
    })

df_stores = pd.DataFrame(stores)
print(df_stores)


df_stores.to_csv(
    "data/raw/stores.csv",
    index=False,
    encoding="utf-8-sig"
)
