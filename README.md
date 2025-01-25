# Weather  etl_pipeLineProj01

An automated ETL pipeline that collects daily weather data for Chicago using Apache Airflow and PostgreSQL.

## 🔍 Overview

- Extracts weather data from Open-Meteo API
- Transforms raw data into structured format
- Loads data into PostgreSQL database
- Runs daily using Apache Airflow

## 🛠️ Technical Stack

- Apache Airflow
- PostgreSQL 13
- Python
- Docker & Docker Compose

## 📁 Project Structure

├── dags/ │ └── etl_weather.py # ETL pipeline DAG ├── docker-compose.yml # Docker configuration └── README.md # Documentation


## 💾 Data Schema

```sql
CREATE TABLE weather_data(
    latitude FLOAT,
    longitude FLOAT,
    temperature FLOAT,
    wind_speed FLOAT,
    wind_direction FLOAT,
    weather_code INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

ETL Pipeline
Extract

Source: Open-Meteo API
Location: Chicago (41.881832, -87.623177)
Data: Current weather conditions
Transform

Structures raw API data
Extracts relevant weather metrics
Formats data for database storage
Load

Destination: PostgreSQL database
Schedule: Daily execution
Automatic table creation
🚀 Setup Instructions
Clone the repository:

git clone <repository-url>
cd etl_pipeLineProj01

Start Docker containers:

docker-compose up -d

Configure Airflow connections:
postgres_default: PostgreSQL connection
open_meteo_api: Weather API connection
⚙️ Configuration
PostgreSQL
Host: localhost
Port: 5432
Credentials:

User: postgres
Password: postgres
Database: postgres

ocation Settings
Chicago, IL

Latitude: 41.881832
Longitude: -87.623177