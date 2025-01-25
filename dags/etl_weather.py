from airflow import DAG
from airflow.providers.https.hooks.http import HttpHook
from airflow.provider.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from airflow.utils.dates import days_ago


### LAT AND LONG OF CHICAGO
LATITUDE = '41.881832'
LONGITUDE = '-87.623177'
POSTGRES_CONN_ID = 'postgres_default'
API_CONN_ID = 'open_meteo_api'

default_args={

    'owner': 'airflow',
    'start_date': days_ago(1),

}

###DAG
with DAG(dag_id='etl_weather',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dags:
    
    @task()
    def extract_weather_data():

        # USING HTTP HOOK TO GET DATA FROM API
        http_hook = HttpHook(http_conn_id=API_CONN_ID, method='GET')

        #BUILDING THE API ENDPOINT
        # https://api.open-meteo.com/v1/forecast?latitude=41.881832&longitude=-87.623177&current_weather=true
        endpoint = f'/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true'


        #Its time to get some response 
        response = http_hook.run(endpoint)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Failed to fetch data from API {response.status_code}')
        
    @task()
    def transform_weather_data(weather_data):
        #Extracting the required data from the response
        data = weather_data['current_weather']
        transformed_data= {
            'latitude': LATITUDE,
            'longitude': LONGITUDE,
            'temperature': data['temperature'],
            'wind_speed': data['wind_speed'],
            'wind_direction': data['wind_direction'],
            'weather_code': data['weather_code'],
        } 
        return transformed_data
    
    @task()
    def load_transformed_data(transformed_data):
        #Loading the data into the database
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        cursor.execute(

            """
            CREATE TABLE IF NOT EXISTS weather_data(
                latitude FLOAT,
                longitude FLOAT,
                temperature FLOAT,
                wind_speed FLOAT,
                wind_direction FLOAT,
                weather_code INT
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


        cursor.execute(

            """
            INSERT INTO weather_data(latitude, longitude, temperature, wind_speed, wind_direction, weather_code) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                transformed_data['latitude'],
                transformed_data['longitude'],
                transformed_data['temperature'],
                transformed_data['wind_speed'],
                transformed_data['wind_direction'],
                transformed_data['weather_code']
            )
        )

        conn.commit()
        cursor.close()

    #DAG- WORKFLOW ETL PIPELINE 
    weather_data = extract_weather_data()
    transformed_data = transform_weather_data(weather_data)
    load_weather_data = load_transformed_data(transformed_data) 

