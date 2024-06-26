# Weather Forecasting 
when this file is ran it will fetch the current weather from OpenWeathermap API every 5 minutes. After fetching from OpenWeathermap it will store the result in a PostgreSQL database.

# Tech stack
- Python
- PostgreSQL 
- Elephantsql
- Python libraries 
  - requests
  - psycopg
  - Bytest
  - json
  - time
  - os
  - dotenv
 
# Running the Project
***Before running this code you need to have PostgreSQL on your system. this code uses `psycopg-c` which needs `pg_config` provided by PostgreSQL.***


**1. to import the database schema:**
1. open command  prompt 
2. change the directory to Postgres bin file (where psql exist) the default path is: "C:\Program Files\PostgreSQL\version\bin"
3. before continuing, this command will create a database named "weather_forecast" so to avoid errors make sure you don't have a database with that name 
	- run this command -> `psql -h <host name> -U <username> -f <sql file path>`
	- replace the `<host name>` and `<username>` with your host name 
	- find the SQL file you are importing and copy its path replacing `<sql file path>`


**2. after importing the schema you will need to set the database access string to do so:**

Note:
The Config class allows you to retrieve and overwrite variables.
follow the following access string format:
`postgresql://username:password@host:port/dbname[?paramspec]`

you can follow either of those approaches: 
a. create a `.env` and add in it the database access string. with using this approach the be set when creating an instance of the Config file.
b. use the function `set(key, value)` to set the database access from the main file. the key I used is `DB_CONNECTION`


after doing one of the options you will need to get the values in your main file as so
```
DB_CONNECTION = config.get(key)
API_CALL = config.get(key)
```


**3. finally you will need to add your API call:**

To do that you can follow the same steps as adding the database access string. the key I used for the API call variable is `API_CALL`.


***now you are ready to run the code!***


# Design Issues 
### Database tables 
After dissecting the API Json response, I could see that is has some keys with Json values.  To acknowledge this structure, I started by creating a separate table for each of those keys which are connected back to a table that contains the rest of keys. For the code purpose this database schema is impractical and unnecessary. 

After a deeper review of the API result, I opted to have just 3 tables. The only table I couldn’t merge to the main table was the weather since it has a many-to-many relationship with the rest of the API response. to connect weather table and the main table I created a relation table. The rest of the API response is in one table this was achieved by forming each key with Json values into attributes in the main table.

Reconstructing the tables simplified the query to retrieve the data and made the data make sense and logical.

### inserting in the table 
to insert all the values in the table I made sure to name each value in the key with a Json fila as "key_eachKeyInJson". later to insert every thing in the main table (api_res) other that the weather key, I had a for loop iterating through the API response appending to the the column names sting and values of those column name list. after having all the column names and values insert to the database.

To insert the weather, get the PK of the row in api_res related to this weather (the API response we are inserting). then iterate through the weather list and for each weather insert in the relation table the api_res PK and the weather id. at the end if the weather isn't already in the weather table insert it.




