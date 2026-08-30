from faker import Faker 
import pandas as pd 
import random 
from datetime import date, timedelta
fake = Faker('pt_BR')


end_date = date.today() - timedelta(days=90)


states = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF',
    'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA',
    'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS',
    'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]

customers = []

for i in range(1, 120):
    customers.append(
        {
            "id_customer": i,
            "customer_name": fake.name(),
            "state": random.choice(states),
            "registration_date": fake.date_between(
                start_date='-2y',
                end_date=end_date
            )
        }
    )

df_customers = pd.DataFrame(customers)

df_customers.to_csv(
    "data/raw/customers.csv",
    index=False,
    encoding="utf-8-sig"

)