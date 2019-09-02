# Project 1 : Data Modeling with Postgres
### Purpose: 
    The purpose of this project is to create a database to help Sparkify enhance their business goals. 
    This database is created with the intention that it can be used for quick and efficient data retrieval thereby redcuing time to analyze data.
    
#### Database: 
     The type of schema used to create the Sparkify database is a star schema. This schema is chosen particularly as we have one fact table and four dimension tables. 
     There are no multiple parent-child dimension tables. Moreover, a star schema is a good fit as Sparkify's needs are to have a database for quick and fast data retrieval for adhoc-queries.
     
#### Tables :
    The tables that are in the Sparkify database are as follows
    1. Songplay - Fact table 
    2. Artist    - Dimension table
    3. Songs     - Dimension table
    4. Time      - Dimension table
    5. Users     - Dimension table 
    
#### Songplay table: 
        This is the fact table in the Sparkify database. This table provides metric information of the sparkify database.The columns in the Songplays table are,
        1. songplay_id - 'serial' datatype set as 'PRIMARY KEY'. This is the identity column of the table that is auto incremented with every insert.
        2. start_time - 'timestamp' datatype set to NOT NULL. 
        3. user_id    - 'int' datatype set to NOT NULL. 
        4. level      - 'text' datatype set to accept NULLs. This column determines the type of user (Paid, free)
        5. song_id    - 'text' datatype set to accept NULLs. 
        6. artist_id  - 'text' datatype set to accept NULLs. 
        7. session_id - 'int' datatype set to accept NULLs. 
        8. location   - 'text' datatype set to accept NULLs. 
        9. user_agent - 'text' datatype set to accept NULLs.  
#### Artist table: 
        This dimension table provides information about the Artists data. The columns in the Artist table are,
        1. artist_id - 'text' datatype set to NOT NULL. 
        2. name      - 'text' datatype set to accept NULLs. 
        3. location  - 'text' datatype set to accept NULLs. 
        4. latitude  - 'text' datatype set to accept NULLs. 
        5. longitude - 'text' datatype set to accept NULLs.        
#### Songs table: 
        This dimension table has the informtaion on the Songs in the database. The columns in the Song table are,
        1. song_id   - 'text' datatype set to NOT NULL. 
        2. title     - 'text' datatype set to accept NULLs. 
        3. artist_id - 'text' datatype set to NOT NULL. 
        4. year      - 'int' datatype set to accept NULLs.   
        5. duration  - 'decimal' datatype set to accept NULLs.
#### Time table:
        This dimension table has the information on the duration of the songs broken down into various time units. The columns in this table are,
        1. start_time  - 'timestamp' datatype set to NOT NULL
        2. hour        - 'int' datatype set to NOT NULL
        3. day         - 'int' datatype set to NOT NULL
        4. week        - 'int' datatype set to NOT NULL 
        5. month       - 'int' datatype set to NOT NULL
        6. year        - 'int' datatype set to NOT NULL
        7. weekday     - 'int' datatype set to NOT NULL
#### Users table: 
        This dimention table has the information on the users. The columns in this table are,
        1. user_id    - 'int' datatype set to NOT NULL
        2. first_name - 'text' datatype set to accept NULLs.
        3. last_name  - 'text' datatype set to accept NULLs.
        4. gender     - 'text' datatype set to accept NULLs.
        5. level      - 'text' datatype set to accept NULLs.

#### Steps to load data into tables:
    The data files used for this project are in JSON format. We have two data files - 
    1. song file - has information on songs and artists
    2. log file - has information on user activity
    
    We create a data pipeline to insert data into the Postgres tables in the Sparkify database from the JSON files after modifying the data. 
    The data modification is done using dataframes, lists, dictionaries and tuples in Python. These are the files associated with creating the data pipeline,
    1. sql_queries.py - This python file has the queries needed to create the tables and insert data
    2. create_tables.py - This python file is used to establish the data connection to the database to create the tables and insert data into them using sql_queries.py file which has the actual queries.
    2. etl.py - This python file is used to establish the connection to the database, read the data from the JSON files, transform data with respect to the datatype needed in our tables and then insert them into the respective tables row by row. 
    
#### Queries: 
    The database is now ready to be used to perform exploratory data analysis (EDA) to gain some insights into the data. Belwo are as few quick queries that can be used for EDA
    
##### Query to find Top 2 songs
```sql
 SELECT COUNT(song_id) AS ct, title AS SONGS 
 FROM songs 
 GROUP BY title 
 ORDER BY ct DESC LIMIT 2
```

##### Query to find total users by level
```sql
SELECT COUNT(distinct user_id), level 
FROM songplay 
GROUP BY level
```
        
##### Query to find top 3 song duration
 ```sql
 SELECT MAX(duration) AS maxduration, title 
 FROM songs 
 GROUP BY  title 
 ORDER BY maxduration DESC LIMIT 3
 ```

    