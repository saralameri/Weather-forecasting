import pycurl
from io import BytesIO
import json
import psycopg
import time
from configparser import ConfigParser

print("hi")
configFile = "config.ini"
config = ConfigParser()
config.read(configFile)

buffer = BytesIO()
curl = pycurl.Curl()
curl.setopt(
    curl.URL,
    config["API"]["call"],
)
curl.setopt(curl.WRITEDATA, buffer)

with psycopg.connect(config["database"]["connection"]) as connection:
    while True:
        # emptying the buffer
        buffer.seek(0)
        buffer.truncate()
        # executes the HTTP request
        curl.perform()
        # retrieves the HTTP response code of the request that was just performed.
        response_code = curl.getinfo(curl.RESPONSE_CODE)
        response_body = buffer.getvalue().decode("utf-8")
        # If the response code indicates a successful request (e.g., 200)
        if response_code == 200:
            data = json.loads(response_body)
        else:
            # handle if the response code indicates an error
            print(f"Failed to fetch data. Response code: {response_code}")
            break

        # Open a cursor to perform database operations
        with connection.cursor() as cursor:
            # collect the insert SQL query requirements
            col = ""
            val = list()

            for key in data:
                if isinstance(data[key], dict) and key != "weather":
                    temp = f"{key}_" + f", {key}_".join(data[key].keys())
                    col = ", ".join([col, temp])
                    val.extend(data[key].values())
                elif key != "weather":
                    col = ", ".join([col, key])
                    val.append(data[key])

            col = col.strip(", ")
            sql_insert = "INSERT INTO api_res ({}) VALUES ({});".format(
                col, ", ".join("%s" for _ in col.split(","))
            )
            cursor.execute(sql_insert, val)

            PK = cursor.execute(
                "SELECT res_id FROM api_res ORDER BY res_id DESC LIMIT 1"
            ).fetchone()[0]

            for inst in data["weather"]:
                weatherID = inst["id"]
                weatherPK = cursor.execute(
                    f"select id from weather where id = {weatherID}"
                ).fetchall()
                if len(weatherPK) == 0:
                    sql_insert = "INSERT INTO weather ({}) VALUES ({});".format(
                        (", ".join(inst.keys())), ", ".join("%s" for _ in inst)
                    )
                    cursor.execute(sql_insert, list(inst.values()))

                sql_insert = "INSERT INTO res_weather_relation (res_id, weather_id) VALUES ({}, {});".format(
                    PK, inst["id"]
                )
                cursor.execute(sql_insert)

            connection.commit()
        print("see you in 5 min")
        time.sleep(300)  # 300 sec = 5 min

connection.close()
