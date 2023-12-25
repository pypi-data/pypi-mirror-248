from google.cloud import bigquery
from datetime import datetime, timedelta

bq_client = bigquery.Client()

all_status = []


def get_logs(step):

    #Получаем данные для обработки
    query = f"""
        SELECT path FROM  
            (SELECT
            time,
            path,
            step,
            is_completed,
            ROW_NUMBER() OVER(PARTITION BY path ORDER BY time DESC) as num
        FROM `newageriver.config.adriver-logs-test`) as t
        WHERE num = 1 and step = '{step}' and is_completed = TRUE;"""

    query_job = bq_client.query(query)
    return query_job.result()


def update_log(URL):

    moscow_time = datetime.now() + timedelta(hours=3)
    current_timestamp = moscow_time.strftime('%Y-%m-%d %H:%M:%S') 
    parts = URL.split('/')
    name = parts[-2] # Название FTP рекламодателя
    log_type = parts[-1].split('.')[-3] # Название лога
    file_date = URL.split('.')[0].split('__')[-1] # дата лога, для ссылки
    
    query = f"""
        (DATE('{current_timestamp}'),
         DATETIME('{current_timestamp}'),
        '{name}',
        '{log_type}',
        DATE('{file_date}'),
        '{URL}',
        'transform',
        TRUE)"""
    
    all_status.append(query)


def insert_logs(table_id):

    all_status_string = ', '.join(all_status)

    #Обновляем таблицу
    query = f"""
        INSERT INTO `{table_id}` (date, time, ftp, log_type, log_date, path, step, is_completed)
        VALUES
        {all_status_string}"""

    bq_client.query(query)