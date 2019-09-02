# Project 4 - Data Lake
### Purpose: 
    The purpose of this project is to build a data lake in Amazon S3 using Spark and Amazon EMR for Sparkify as they have grown their user base and are looking to move their data to a larger environment. 
    The data resides in S3 as JSON files on the user's activity along with metadata on the songs. 
    The data can be read from S3 and converted to meaningful tables for analysis using a spark cluster running on EC2 instances. 
  
### Tables: 
    We have one fact and four dimension tables, 
    1. Fact table - songplay 
    2. Dimension tables:
        a. users 
        b. songs 
        c. artists 
        d. timetable
        
### Configurations for Data Warehouse:
    1. Create a new IAM Role with S3 Full Access to read and write data to and from S3 buckets
    2. Use the AWS IAM Key and secret access keys in the Config file to access the AWS environment from jupyter notebooks.
    2. Create an EMR cluster with spark to run our data analysis and ELT using spark in this cluster
    3. Once we have our cluster ready, use the S3 bucket link as the output of the data that we are about to ingest
    
### Execution steps for the data transfer:
    1. We read the song and the log data from the json files from our input S3 bucket and extract the columns we need from the dataframe for the songs and the artists table
    2. Upon extraction to dataframes, we then write to our destination table with the parquet format partitioning by year and artist_id for the songs table
    3. We use lambda functions to create a timestamp column(using spark 'withColumn' method) and time related fields (start_time, hour, day, week, month, year, weekday)
    4. We then create the songplays table by joining the song and the log files and then insert into the destination with the parquet format
    5. We now have separate folders for each of our tables in the destination S3 bucket. 
    