import os
import pandas as pd
from sqlalchemy import create_engine

db_name = os.getenv("DATABASE")
db_user = os.getenv("USERNAME")
db_password = os.getenv("PASSWORD")
db_host = os.getenv("HOST")
db_port = os.getenv("PORT")

def csv_to_sql(engine, table_name, file_path):

    df = pd.read_csv(file_path)

    # Write DataFrame to PostgreSQL Table
    df.to_sql(table_name, engine, if_exists='replace', index=False)

    print("DataFrame written to PostgreSQL table successfully.")


def main():

    engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

    csv_to_sql(engine, "category_test", "./data/category.csv")
    csv_to_sql(engine, "orders_test", "./data/orders.csv")
    csv_to_sql(engine, "event_test", "./data/event.csv")

    print("Data successfully loaded into tables.")


if __name__ == "__main__":
    main()


