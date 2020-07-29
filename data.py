from sodapy import Socrata
import pandas as pd

# Add your Socrata key here
client = Socrata("data.cityofnewyork.us", "")
client.timeout = 12000

data_codes = {2017: "2upf-qytp", 2018: "t29m-gskq", 2019: "2upf-qytp"}


def csv_generation(year, code):
    pickup_query = """select pulocationid, count(pulocationid) as totalcount
        where dolocationid <= 262 and pulocationid <= 262 and total_amount >= 0
        group by pulocationid
        offset 0 limit 10000000"""

    results = client.get(code, query=pickup_query)
    pickup_count = pd.DataFrame.from_records(results)
    pickup_count.to_csv(f"pickup_count_{year}csv", index=False)

    dropoff_query = """select dolocationid, count(dolocationid) as totalcount
                    where pulocationid <= 262 and dolocationid <= 262 and total_amount >= 0
                    group by dolocationid
                    offset 0 limit 10000000"""

    results = client.get(code, query=dropoff_query)
    dropoff_count = pd.DataFrame.from_records(results)
    dropoff_count.to_csv(f"dropoff_count_{year}.csv", index=False)

    mapping_query = """select pulocationid, dolocationid, count(dolocationid) as totalcount
                        where pulocationid <= 262 and dolocationid <= 262 and total_amount >= 0
                        group by pulocationid, dolocationid
                        offset 0 limit 10000000"""

    results = client.get(code, query=mapping_query)
    pickup_dropoff_mapping = pd.DataFrame.from_records(results)

    pickup_dropoff_mapping.to_csv(f"pickup_dropoff_mapping_{year}.csv", index=False)


for yr, code in data_codes.items():
    csv_generation(yr, code)
