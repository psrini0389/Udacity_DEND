# Project 3: Data Warehouse
### Purpose: 
    The purpose of this project is to build a Data Warehouse for a music streaming company called Sparkify.
    The company wants to analyse the user's daily activies and provide song recommendations based on JSON data files generated from the appliaction.
    This can be achieved by creating cloud data warehouse as data processing, querying, data retreival would be much faster, robust and scalable.
    The data warehouse that we build for this project would be a STAR schema in a Redshift cluster.
    The company can analyse the data to get insights pertaining to user behavior, listening patterns, genres to provide future recommendations, playlists. 
    
### Tables:
    The STAR schema consists of one fact table with multiple dimension tables associated/referencing to it. 
    1. Fact table - songplay 
    2. Dimension tables:
        a. users 
        b. songs 
        c. artists 
        d. timetable
        
### Configurations for Data Warehouse 
     1. Create a new IAM user in the AWS console. 
     2. Provide administrative acess to the IAM user and attach policies (S3 ReadOnly Access and Redshift Full Access)
     3. Use Access Key and Secret Access Key to create EC2, S3, Redshift clients. Note down the Access Key, Secret Access Key and the endpoint to use in the config file to access Redshift with the IAM user. 
     4. Use the end point of the Redshift cluster in the config file along with other access details for the cluster (DB_NAME, DB_USER, DB_PASSWORD, DB_PORT)
       
### Data transfer - ETL Pipeline
    1. Created staging and main tables in Redshift to store the data from the S3 buckets.
    2. Loaded data from S3 buckets that hold the JSON files to staging tables in the Redshift cluster using the copy command. 
    3. Inserted data to the destination fact and dimension tables from the staging tables. 
    
### Files used in the project
    1. sql_queries.py - This python file has the queries necessary to create the staging tables, destination tables, and the queries to insert data into them.
    2. dwh.cfg - This is the configuration file that holds the connection parameters to the AWS console and the path for the data files in the S3 bucket.
    3. create_tables.py - This python file is used to drop and create the tables in the sql_queries.py file
    4. etl.py - The funtion used in this python file is used to initiate the data load steps in the sql_queries.py file. Successful data load can be later validated by querying the database.
    
### Excecution steps: 
    1. Setup the Redshift cluster, IAM users, roles and attach policies
    2. Provide credentials in the dwh.cfg config file
    3. Run create_tables.py to create tables in Redshift - %run create_tables.py
    4. Run etl.py to load the data from S3 to Redshift -%run etl.py
    5. Validate successful data transfer by querying the data in Redshift. 
    

    