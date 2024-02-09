# Paris Weather Forecasting 
when this file is ran it will fetch Paris current weather from OpenWeathermap API every 5 minutes. After fetching from OpenWeathermap it will store the result in a PostgreSQL database.

# Tech stack
- Python
- PostgreSQL 
- Elephantsql
- Python libraries 
  - pycurl
  - psycopg
  - Bytest
  - json
  - time
# Design Issues 
### Database tables 
After dissecting the API Json response, I could see that is has some keys with Json values.  To acknowledge this structure, I started by creating a separate table for each of those keys which are connected back to a table that contains the rest of keys. For the code purpose this database schema is impractical and unnecessary. 

After a deeper review of the API result, I opted to have just 3 tables. The only table I couldn’t merge to the main table was the weather since it has a many-to-many relationship with the rest of the API response. to connect weather table and the main table I created a relation table. The rest of the API response is in one table this was achieved by forming each key with Json values into attributes in the main table.

Reconstructing the tables simplified the query to retrieve the data and made the data make sense and logical.



