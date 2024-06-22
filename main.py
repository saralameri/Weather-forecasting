import logging
import requests
import psycopg
import time
from config import Config

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s[%(asctime)s]: %(message)s"
)

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


def get_query_params(data, columns):
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

    # values stores SQL query values (initialized to NONE) in a list
    cols = columns.split(",")
    values = [None] * 31

    for key in data:
        if isinstance(data[key], dict) and key != "weather":
            for internal_key in data[key]:
                name = f"{key}_{internal_key}"
                if name in cols:
                    index = cols.index(name)
                    values[index] = data[key][internal_key]
                else:
                    raise Exception("key in API is not recognized")

        elif key != "weather":
            if key in cols:
                index = cols.index(key)
                values[index] = data[key]
            else:
                raise Exception("key in API is not recognized")

    return values


def insert_weather(data):
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
        cols = ["id", "main", "description", "icon"]
        values = [None] * 4
        for i in instance:
            if i in cols:
                index = cols.index(i)
                values[index] = instance[i]
            else:
                raise Exception("key in API is not recognized")

        # if the id doesn't already exist in the weather table
        if len(weather_pk) == 0:
            # checking if the insert was successful
            try:
                place_holder = "%s" + ", %s" * 3
                sql_insert = f"INSERT INTO weather (id, main, description, icon) VALUES ({place_holder});"
                cursor.execute(sql_insert, list(instance.values()))
            except Exception as error:
                raise Exception(
                    f"Failed to inserting the weather key to the database. {error}"
                )

            # if cursor.rowcount == 0:
            #     raise Exception("Failed to inserting the weather key to the database")

        # update the relation table
        try:
            cols = "res_id, weather_id"
            sql_insert = f"INSERT INTO res_weather_relation ({cols}) VALUES (%s, %s);"
            cursor.execute(sql_insert, (PK, instance["id"]))
            logging.info(f"Successfully added API call {PK} to the database.")
        except Exception as error:
            raise Exception(
                f"Failed to inserting into res_weather_relation table. {error}"
            )

        # checking if the insert was successful
        # if cursor.rowcount > 0:
        #     logging.info(f"Successfully added API call {PK} to the database.")
        # else:
        #     raise Exception("Failed to inserting into res_weather_relation table.")


while True:
    response_code, data = call_api()
    # handle if the response code indicates an error
    if response_code != 200:
        logging.error(f"Failed to fetch data. Response code: {response_code}.")
        break

    # If the response code indicates a successful request continue with the rest of the code
    logging.info(f"Successful API call. Response code: {response_code}.")
    connection = psycopg.connect(DB_CONNECTION)

    # Open a cursor to perform database operations
    cursor = connection.cursor()

    # insert in the DB
    try:
        columns = "coord_lon,coord_lat,base,main_temp,main_feels_like,main_temp_min,main_temp_max,main_pressure,main_humidity,main_sea_level,main_grnd_level,visibility,wind_speed,wind_deg,wind_gust,dt,sys_type,sys_id,sys_message,sys_country,sys_sunrise,sys_sunset,timezone,id,name,cod,clouds_all,rain_1h,rain_3h,snow_1h,snow_3h"
        place_holder = "%s" + ",%s" * 30
        # collect the SQL query parameters
        values = get_query_params(data, columns)
        sql_insert = f"INSERT INTO api_res ({columns}) VALUES ({place_holder});"

        cursor.execute(sql_insert, values)
        if cursor.rowcount == 0:
            raise Exception("Failed to insert into api_res table")

        PK = cursor.execute(
            "SELECT res_id FROM api_res ORDER BY res_id DESC LIMIT 1"
        ).fetchone()[0]
        if cursor.rowcount == 0:
            raise Exception(
                "Failed to fetch the primary key of the later row in the api_res table"
            )

        insert_weather(data)

    except Exception as error:
        connection.rollback()
        logging.error(error)

    cursor.close()
    connection.commit()
    connection.close()

    logging.info("Pausing for 5 minutes")
    time.sleep(300)  # 300 sec = 5 min
