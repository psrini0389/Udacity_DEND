import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
from pyspark.sql.functions import monotonically_increasing_id


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS_KEYS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_KEYS']['AWS_SECRET_ACCESS_KEY']

def create_spark_session():
    '''Creates Spark Session'''
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark

def process_song_data(spark, input_data, output_data):
    '''get filepath to song data file'''
    song_data = os.path.join(input_data, "song_data/*/*/*/*.json")
        
    df = spark.read.json(song_data)
    '''read song data file'''
    
    songs_table = df['song_id', 'title', 'artist_id', 'year', 'duration']
    '''extract columns to create songs table'''  
    
    songs_table.write.partitionBy('year', 'artist_id').parquet(os.path.join(output_data, 'songs.parquet'), 'overwrite')
    '''write songs table to parquet files partitioned by year and artist'''

    artists_table =  df['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']
    ''' extract columns to create artists table''' 
    
    artists_table.write.parquet(os.path.join(output_data, 'artists.parquet'),'overwrite')
    '''write artists table to parquet files'''

def process_log_data(spark, input_data, output_data):
    ''' get filepath to log data file'''
    log_data = os.path.join(input_data, "log_data/*/*/*/*.json")

    df = spark.read.json(log_data)
    '''read log data file'''
    
    songplays_table = df['ts', 'userId', 'level', 'sessionId', 'location', 'userAgent']
    '''filter by actions for song plays'''
 
    users_table = df['userId', 'firstName', 'lastName', 'gender', 'level']
    '''extract columns for users table '''
    
    users_table.write.parquet(os.path.join(output_data,'users.parquet'), 'overwrite')
    '''write users table to parquet files'''

    get_timestamp = udf(lambda x: str(int(int(x)/1000)))
    '''create timestamp column from original timestamp column'''
    df = df.withColumn('timestamp', get_timestamp(df.ts))
    
    get_datetime = udf(lambda x: datetime.fromtimestamp(int(int(x)/1000)))
    '''create start_time column from original timestamp column'''
    df = df.withColumn('start_time', get_datetime(df.ts))
    
    get_hour = udf(lambda x: x.hour)
    '''create hour column from start_time'''
    df = df.withColumn('hour', get_hour(df.start_time))
    
    get_day = udf(lambda x: x.day)
    '''create day column from start_time'''
    df = df.withColumn('day', get_day(df.start_time))
    
    get_week = udf(lambda x: x.isocalendar()[1])
    '''create week column from start_time column using isocalendar method and reading the first index of its output'''
    df = df.withColumn('week', get_week(df.start_time))
    
    get_month = udf(lambda x: x.month)
    '''create month column from start_time'''
    df = df.withColumn('month', get_month(df.start_time))
    
    get_year = udf(lambda x: x.year)
    '''create year column from start_time'''
    df = df.withColumn('year', get_year(df.start_time))
    
    get_weekday = udf(lambda x: x.isocalendar()[2])
    '''create weekday from start_time column using isocalendar method and reading the second index of its output'''
    df = df.withColumn('weekday', get_weekday(df.start_time))
      
    time_table = df['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    ''' Extract columns to create time table'''
    
    time_table.write.partitionBy('year', 'month').parquet(os.path.join(output_data,'timetable.parquet'),'overwrite')
    '''write time table to parquet files partitioned by year and month'''

    song_df = spark.read.parquet('songs.parquet')
    '''read in song data to use for songplays table'''

    df = df.join(song_df, song.df.title == df.song)
    ''' extract columns from joined song and log datasets to create songplays table '''
    songplays_table = df['start_time', 'userId', 'level', 'song_id', 'artist_id', 'sessionId', 'location', 'userAgent']
    songplays_table.select(monotonically_increasing_id().alias('songplay_id')).collect()

    songplays_table.write.parquet(os.path.join(output_data,'songplays.parquet'), 'overwrite')
    '''write songplays table to parquet files partitioned by year and month'''

def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = ""
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()