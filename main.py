import requests
import psycopg
import time
from config import Config

config = Config()

DB_CONNECTION = config.get("DB_CONNECTION")
API_CALL = config.get("API_CALL")


def call_api():
    """A simple function that calls the API and return its response code and response body"""

    # calling the API
    response = requests.get(API_CALL)

    # retrieves the HTTP response code
    response_code = response.status_code

    # retrieves the data from the response
    data = response.json()

    return response_code, data


def get_query_params(data):
    """
    Iterating through the response body gathering the SQL query parameters.
    Two things are collected, the columns and the values to store in them.

    If apart of the response body has a single value then the key will be added in the columns.

    In the other case if it is a dictionary then the key_dictionaryKey for each key in the dictionary
    will be added to the columns.

    Parameters
    ----------
    data -> json
    """

    # columns stores SQL query columns in a string
    columns = ""
    # values stores SQL query values in a list
    values = list()

    for key in data:
        if isinstance(data[key], dict) and key != "weather":
            curr_columns = f"{key}_" + f", {key}_".join(data[key].keys())
            columns = ", ".join([columns, curr_columns])
            values.extend(data[key].values())

        elif key != "weather":
            columns = ", ".join([columns, key])
            values.append(data[key])

    return columns.strip(", "), values


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

    for instance in data["weather"]:
        weather_id = instance["id"]
        weather_pk = cursor.execute(
            f"select id from weather where id = {weather_id}"
        ).fetchall()

        # if the id doesn't already exist in the weather table
        if len(weather_pk) == 0:
            sql_insert = "INSERT INTO weather ({}) VALUES ({});".format(
                (", ".join(instance.keys())), ", ".join("%s" for _ in instance)
            )
            cursor.execute(sql_insert, list(instance.values()))

        # update the relation table
        sql_insert = "INSERT INTO res_weather_relation (res_id, weather_id) VALUES ({}, {});".format(
            PK, instance["id"]
        )
        cursor.execute(sql_insert)
        affected_rows = cursor.rowcount
        if affected_rows > 0:
            print(f"successfully added API call {PK} to the database.")
        else:
            print("failed to add to the database")


while True:
    response_code, data = call_api()

    # handle if the response code indicates an error
    if response_code != 200:
        print(f"Failed to fetch data. Response code: {response_code}.")
        break
    
    # If the response code indicates a successful request continue with the rest of the code
    print(f"successful API call. Response code: {response_code}.")
    connection = psycopg.connect(DB_CONNECTION)

    # Open a cursor to perform database operations
    cursor = connection.cursor()

    # collect the SQL query parameters
    columns, values = get_query_params(data)

    # insert in the DB
    sql_insert = "INSERT INTO api_res ({}) VALUES ({});".format(
        columns, ", ".join("%s" for _ in columns.split(","))
    )
    cursor.execute(sql_insert, values)

    PK = cursor.execute(
        "SELECT res_id FROM api_res ORDER BY res_id DESC LIMIT 1"
    ).fetchone()[0]

    insert_weather()

    cursor.close()
    connection.commit()
    connection.close()

    time.sleep(300)  # 300 sec = 5 min
