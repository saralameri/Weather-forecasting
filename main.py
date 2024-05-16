import requests
import psycopg
import time
from config import Config

config = Config()

DB_CONNECTION = config.get("DB_CONNECTION")
API_CALL = config.get("API_CALL")


def callAPI():
    """A simple function that calls the API and return its response code and response body"""

    # calling the API
    response = requests.get(API_CALL)

    # retrieves the HTTP response code
    response_code = response.status_code

    # retrieves the data from the response
    data = response.json()

    return response_code, data


def get_queryParams(data):
    """
    Iterating through the response body gathering the SQL query parameters.
    Two things are collected, the columns (col) and the values to store in them (val).

    If apart of the response body has a single value then the key will be added in the col.

    In the other case if it is a dictionary then the key_dictionaryKey for each key in the dictionary
    will be added to the col.

    Parameters
    ----------
    data -> json
    """

    # col stores SQL query columns in a string
    cols = ""
    # val stores SQL query values in a list
    val = list()

    for key in data:
        if isinstance(data[key], dict) and key != "weather":
            temp = f"{key}_" + f", {key}_".join(data[key].keys())
            cols = ", ".join([cols, temp])
            val.extend(data[key].values())

        elif key != "weather":
            cols = ", ".join([cols, key])
            val.append(data[key])

    return cols.strip(", "), val


def insert_weather():
    """
    Wether in the OpenWeather API contain a list of one or more instance of type dictionary.
    To handle this specific situation a separate function is needed

    in the DB we have 3 tables
        api_res -> storing the response body other than the weather
        weather -> stores the weather
        res_weather_relation -> relationship between weather and the rest of the response

    Weather instances is also an instance of a weather set identified by its id.
    In the DB we store the weather only if it is not already exist as a set of weather.

    then in the relationship table we connect the response with the relates weather.
    """

    for inst in data["weather"]:
        weatherID = inst["id"]
        weatherPK = cursor.execute(
            f"select id from weather where id = {weatherID}"
        ).fetchall()

        # if the id doesn't already exist in the weather table
        if len(weatherPK) == 0:
            sql_insert = "INSERT INTO weather ({}) VALUES ({});".format(
                (", ".join(inst.keys())), ", ".join("%s" for _ in inst)
            )
            cursor.execute(sql_insert, list(inst.values()))

        # update the relation table
        sql_insert = "INSERT INTO res_weather_relation (res_id, weather_id) VALUES ({}, {});".format(
            PK, inst["id"]
        )
        cursor.execute(sql_insert)


while True:
    connection = psycopg.connect(DB_CONNECTION)
    response_code, data = callAPI()

    # handle if the response code indicates an error
    if response_code != 200:
        print(f"Failed to fetch data. Response code: {response_code}")
        break

    # If the response code indicates a successful request
    # Open a cursor to perform database operations
    cursor = connection.cursor()

    # collect the SQL query parameters
    cols, val = get_queryParams(data)

    # insert in the DB
    sql_insert = "INSERT INTO api_res ({}) VALUES ({});".format(
        cols, ", ".join("%s" for _ in cols.split(","))
    )
    cursor.execute(sql_insert, val)

    PK = cursor.execute(
        "SELECT res_id FROM api_res ORDER BY res_id DESC LIMIT 1"
    ).fetchone()[0]

    insert_weather()

    cursor.close()
    connection.commit()
    connection.close()

    time.sleep(300)  # 300 sec = 5 min
