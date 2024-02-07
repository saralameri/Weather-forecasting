import pycurl
from io import BytesIO
import json
import psycopg
import time

buffer = BytesIO()
c = pycurl.Curl()
c.setopt(c.URL, 'http://api.openweathermap.org/data/2.5/weather?q=Paris&APPID=4d260396d5b19dc31ea21f597ac164ef&units=metric')
c.setopt(c.WRITEDATA, buffer)

with psycopg.connect("postgres://ergenznr:KuW9kFZvxTrguNmwENy6SMMIFXEUKXRe@jelani.db.elephantsql.com/ergenznr") as conn:
  while(True):
      # emptying the buffer
      buffer.truncate()
      # executes the HTTP request
      c.perform()
      # retrieves the HTTP response code of the request that was just performed. 
      response_code = c.getinfo(c.RESPONSE_CODE)
      response_body = buffer.getvalue().decode('utf-8')
      # If the response code indicates a successful request (e.g., 200)
      if response_code == 200:
          data = json.loads(response_body)
      else:
          # handle if the response code indicates an error
          print(f"Failed to fetch data. Response code: {response_code}")
          break

      # Open a cursor to perform database operations
      with conn.cursor() as cur:
          # collect the insert SQL query requirements 
          col = ''
          val = list()

          for key in data:
            if isinstance(data[key], dict) and key != 'weather':
              temp = f'{key}_'+f', {key}_'.join(data[key].keys())
              col = ', '.join([col, temp])
              val.extend(data[key].values())
            elif key != 'weather':
              col = ', '.join([col, key])
              val.append(data[key])


          col = col.strip(', ')
          sql_insert = "INSERT INTO api_res ({}) VALUES ({});".format(
                col,
                ', '.join('%s' for _ in col.split(','))
                )
          cur.execute(sql_insert, val)


          PK = cur.execute("SELECT res_id FROM api_res ORDER BY res_id DESC LIMIT 1").fetchone()[0]



          for inst in data['weather']:
            weatherID = inst['id']
            weatherPK = cur.execute(f"select id from weather where id = {weatherID}").fetchall()
            if len(weatherPK) == 0 :
              sql_insert = "INSERT INTO weather ({}) VALUES ({});".format(
              (', '.join(inst.keys())),
              ', '.join('%s' for _ in inst)
              )
              cur.execute(sql_insert, list(inst.values()))

            sql_insert = "INSERT INTO res_weather_relation (res_id, weather_id) VALUES ({}, {});".format(
              PK,
              inst['id']
            )
            cur.execute(sql_insert)

          conn.commit()

      time.sleep(300) # 300 sec = 5 min

conn.close()