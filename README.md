# WeatherApp


Steps to run this python script:

1. First, venv needs to be activated

> source weather/bin/activate

2. Set environment variable for GCS 

> export GOOGLE_APPLICATION_CREDENTIALS= file provided 

3. Run python script

> python3 get_weather.py 

4. Run bq CLI to create and upload gcs data to create a table

> bq load   --autodetect --replace  --source_format=NEWLINE_DELIMITED_JSON public.weather_daily_table gs://testweatherdata/testweatherdata.json 
