from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator,
                                LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries
start_date = datetime.utcnow()

default_args = {
    'owner': 'Prashanth',
    'start_date': datetime(2019, 1, 12),
    'depends_on_past': False,
#    'retries': 3,
#    'retry_delay': timedelta(minutes =  5),
    'catchup': False,
    'email_on_retry': False
}

dag = DAG('udac_example_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *',
          max_active_runs = 3
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id = 'Stage_events',
    dag = dag,
    aws_credentials_id = "aws_credentials",
    s3_bucket = "udacity-dend",
    s3_key = "log_data",
    region = "us-west-2",
    file_format = "JSON",
    execution_date = start_date
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id = 'Stage_songs',
    dag = dag,
    provide_context = True,
    table = "songs",
    redshift_conn_id = "redshift",
    aws_credentials_id = "aws_credentials",
    s3_bucket = "udacity-dend",
    s3_key = "song_data",
    region = "us-west-2",
    data_format = "JSON",
    execution_date = start_date
)

load_songplays_table = LoadFactOperator(
    task_id ='Load_songplays_fact_table',
    dag = dag,
    provide_context = True,
    aws_credentials_id = "aws_credentials",
    redshift_conn_id = "redshift",
    sql_query = SqlQueries.songplay_table_insert
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    start_date= datetime(2019, 1, 12),
    table="users",
    sql_query=SqlQueries.user_table_insert,
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    start_date= datetime(2019, 1, 12),
    table="songs",
    sql_query=SqlQueries.song_table_insert,
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    edshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    start_date= datetime(2019, 1, 12),
    table="artists",
    sql_query=SqlQueries.artist_table_insert,
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    edshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    start_date= datetime(2019, 1, 12),
    table="time_table",
    sql_query=SqlQueries.time_table_insert,
)

run_quality_checks = DataQualityOperator(
    task_id = 'Run_data_quality_checks',
    dag = dag,
    provide_context = True,
    aws_credentials_id = "aws_credentials",
    redshift_conn_id = "redshift",
    tables = ["songplay", "users", "song", "artist", "time"]
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

# Setting tasks dependencies

start_operator >> [stage_songs_to_redshift, stage_events_to_redshift]
[stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table
load_songplays_table >> [load_user_dimension_table, load_song_dimension_table, load_artist_dimension_table, load_time_dimension_table] >> run_quality_checks
run_quality_checks >> end_operator
