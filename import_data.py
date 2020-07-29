import requests, psycopg2, psycopg2.extras, csv
from sodapy import Socrata
import pandas as pd
from datetime import datetime
from pprint import pprint

client = Socrata("data.cityofnewyork.us", "ZTkGdN3ECjDsOsNMKtqqfqhPM")
client.timeout = 12000

connection = psycopg2.connect(
    host="localhost", database="testing", user="postgres", password="",
)
connection.autocommit = True

columns = {
    "tpep_pickup_datetime": "date",
    "tpep_dropoff_datetime": "date",
    "passenger_count": "integer",
    "trip_distance": "real",
    "PULocationID": "integer",
    "DOLocationID": "integer",
    "payment_type": "integer",
    "fare_amount": "real",
    "extra": "real",
    "mta_tax": "real",
    "tip_amount": "real",
    "tolls_amount": "real",
    "total_amount": "real",
}


def create_staging_table(cursor) -> None:
    cursor.execute(
        """
        DROP TABLE IF EXISTS taxi_data;
        CREATE TABLE taxi_data (dummy INTEGER NOT NULL PRIMARY KEY);
        ALTER TABLE taxi_data DROP COLUMN dummy;
        """
    )
    for col, col_type in columns.items():
        cursor.execute(f"ALTER TABLE taxi_data ADD {col.lower()} {col_type};")


def filter_datetime(text):
    return datetime.strptime(text, "%m/%d/%Y %H:%M:%S %p")


select = ", ".join(f"{key}" for key in columns.keys())
print(select)


def from_api(page_size):
    page = 0

    with open("2018_Yellow_Taxi_Trip_Data.csv", "r") as results:
        reader = csv.DictReader(results)

        for ride in reader:
            for k in [
                "ï»¿VendorID",
                "RatecodeID",
                "store_and_fwd_flag",
                "improvement_surcharge",
            ]:
                ride.pop(k)
            if len(ride.keys()) == 13:
                ride["tpep_pickup_datetime"] = (
                    filter_datetime(ride["tpep_pickup_datetime"]),
                )
                ride["tpep_dropoff_datetime"] = (
                    filter_datetime(ride["tpep_dropoff_datetime"]),
                )
                ride["passenger_count"] = int(ride["passenger_count"].replace(",", ""))
                ride["trip_distance"] = float(ride["trip_distance"].replace(",", ""))
                ride["PULocationID"] = int(ride["PULocationID"].replace(",", ""))
                ride["DOLocationID"] = int(ride["DOLocationID"].replace(",", ""))
                ride["payment_type"] = int(ride["payment_type"].replace(",", ""))
                ride["fare_amount"] = float(ride["fare_amount"].replace(",", ""))
                ride["extra"] = float(ride["extra"].replace(",", ""))
                ride["mta_tax"] = float(ride["mta_tax"].replace(",", ""))
                ride["tip_amount"] = float(ride["tip_amount"].replace(",", ""))
                ride["tolls_amount"] = float(ride["tolls_amount"].replace(",", ""))
                ride["total_amount"] = float(ride["total_amount"].replace(",", ""))

            if (
                ride["PULocationID"] > 262
                or ride["DOLocationID"] > 262
                or ride["total_amount"] < 0
            ):
                continue
            if page % 1000000 == 0:
                print(page)
            yield ride
            page += 1


types = {"real": float, "integer": int, "date": filter_datetime}


def insert_execute_batch_iterator(connection, rides):
    with connection.cursor() as cursor:
        create_staging_table(cursor)

        psycopg2.extras.execute_batch(
            cursor,
            """
            INSERT INTO taxi_data VALUES (
                %(tpep_pickup_datetime)s,
                %(tpep_dropoff_datetime)s,
                %(passenger_count)s,
                %(trip_distance)s,
                %(PULocationID)s,
                %(DOLocationID)s,
                %(payment_type)s,
                %(fare_amount)s,
                %(extra)s,
                %(mta_tax)s,
                %(tip_amount)s,
                %(tolls_amount)s,
                %(total_amount)s
            );
        """,
            rides,
        )


data = from_api(500000)
# print(list(data))
# print(len(list(results)))
# insert_execute_batch_iterator(connection, data)
# with connection.cursor() as cursor:
#     create_staging_table(cursor)
