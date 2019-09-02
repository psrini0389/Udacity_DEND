import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')
IAM_ROLE = config['IAM_ROLE']['ARN']
LOG_DATA = config['S3']['LOG_DATA']
SONG_DATA = config['S3']['SONG_DATA']
LOG_JSONPATH = config['S3']['LOG_JSONPATH']

# DROP TABLES

staging_events_table_drop    = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop     = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop          = "DROP TABLE IF EXISTS songplay"
user_table_drop              = "DROP TABLE IF EXISTS users"
song_table_drop              = "DROP TABLE IF EXISTS song"
artist_table_drop            = "DROP TABLE IF EXISTS artist"
time_table_drop              = "DROP TABLE IF EXISTS time_table"

# CREATE TABLES

staging_events_table_create= (""" CREATE TABLE IF NOT EXISTS staging_events
                                   (
                                      artist        VARCHAR NULL
                                    , auth          VARCHAR NULL
                                    , first_name    VARCHAR NULL
                                    , gender        VARCHAR NULL 
                                    , itemInSession INTEGER NULL
                                    , last_name     VARCHAR NULL
                                    , length        NUMERIC NULL
                                    , level         VARCHAR NULL
                                    , location      VARCHAR NULL
                                    , method        VARCHAR NULL
                                    , page          VARCHAR NULL
                                    , registration  NUMERIC NULL 
                                    , session_id    INTEGER NULL
                                    , song          VARCHAR NULL
                                    , status        INTEGER NULL
                                    , ts            TIMESTAMP NULL
                                    , user_agent    VARCHAR NULL
                                    , user_id       INTEGER NULL
                                  )
""")

staging_songs_table_create = (""" CREATE TABLE IF NOT EXISTS staging_songs  
                                  ( 
                                   num_songs        INTEGER NULL
                                 , artist_id        VARCHAR NULL
                                 , artist_latitude  NUMERIC NULL
                                 , artist_longitude NUMERIC NULL
                                 , artist_location  VARCHAR NULL
                                 , artist_name      VARCHAR NULL
                                 , song_id          VARCHAR NULL
                                 , title            VARCHAR NULL
                                 , duration         NUMERIC NULL
                                 , year             INTEGER NULL
                                )
""")

songplay_table_create = ("""  CREATE TABLE IF NOT EXISTS songplay
                                (
                                  songplay_id   INTEGER IDENTITY(0,1) PRIMARY KEY
                                , start_time    TIMESTAMP NOT NULL REFERENCES time_table(start_time)
                                , user_id       INTEGER NOT NULL
                                , level         VARCHAR NULL
                                , song_id       VARCHAR NOT NULL REFERENCES song(song_id)
                                , artist_id     VARCHAR NOT NULL REFERENCES artist(artist_id)
                                , session_id    INTEGER NULL
                                , location      VARCHAR NULL
                                , user_agent    VARCHAR NULL
                                )
""")

user_table_create = ("""  CREATE TABLE IF NOT EXISTS users
                          (
                            user_id       INTEGER PRIMARY KEY 
                          , first_name    VARCHAR NOT NULL
                          , last_name     VARCHAR NOT NULL
                          , gender        CHAR(1) NULL
                          , level         VARCHAR NULL
                          ) 
""")

song_table_create = (""" CREATE TABLE IF NOT EXISTS song
                          (
                              song_id     VARCHAR PRIMARY KEY
                            , title       VARCHAR NULL
                            , artist_id   VARCHAR NOT NULL REFERENCES artist(artist_id)
                            , year        INTEGER NULL
                            , duration    NUMERIC NULL
                          ) 
""")

artist_table_create = ("""  CREATE TABLE IF NOT EXISTS artist
                            (
                              artist_id VARCHAR PRIMARY KEY
                            , name      VARCHAR NULL
                            , location  VARCHAR NULL
                            , latitude VARCHAR NULL
                            , longitude VARCHAR NULL
                            ) 
""")

time_table_create = (""" CREATE TABLE IF NOT EXISTS time_table
                         (
                            start_time  TIMESTAMP PRIMARY KEY
                           , hour       INTEGER NULL
                           , day        INTEGER NULL
                           , week       INTEGER NULL
                           , month      INTEGER NULL
                           , year       INTEGER NULL
                           , weekday    INTEGER NULL
                         ) ;
""")

# STAGING TABLES

"""Copy data from the JSON log files to the staging tables using the COPY command"""

staging_events_copy = ("""  copy staging_events 
                            from {}
                            iam_role {}
                            TIMEFORMAT as 'epochmillisecs'
                            json {};
                        """).format(LOG_DATA, IAM_ROLE, LOG_JSONPATH)

staging_songs_copy = (""" copy staging_songs 
                            from {}
                            iam_role {}
                            json 'auto'
                         """).format(SONG_DATA, IAM_ROLE)

# FINAL TABLES - INSERT STATEMENTS

songplay_table_insert = (""" INSERT INTO songplay (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)    
                            SELECT timestamp 'epoch' + (st.ts/1000) * interval '1 second' as start_time
                                , st.user_id
                                , st.level
                                , ss.song_id
                                , ss.artist_id
                                , st.session_id
                                , st.location
                                , st.user_agent
                            FROM staging_events as st
                            INNER JOIN staging_songs as ss
                                ON st.song = ss.title 
                                    AND st.artist = ss.artist_name 
                                    AND st.length = ss.duration
                            WHERE st.page = 'NextSong'                           
""")

user_table_insert = (""" INSERT INTO users (user_id, first_name, last_name, gender, level)
                         SELECT DISTINCT st.user_id
                             , st.first_name
                             , st.last_name
                             , st.gender
                             , st.level
                         FROM staging_events as st
                         WHERE st.page = 'NextSong'
""")

song_table_insert = (""" INSERT INTO song ( song_id, title, artist_id, year, duration)  
                        SELECT DISTINCT s.song_id
                            , s.title
                            , s.artist_id
                            , s.year
                            , s.duration
                        FROM staging_songs as s
                        WHERE s.song_id IS NOT NULL
""")

artist_table_insert = (""" INSERT INTO artist( artist_id, name, location, latitude, longitude)
                           SELECT DISTINCT s.artist_id
                               , s.artist_name
                               , s.artist_location
                               , s.artist_latitude
                               , s.artist_longitude
                           FROM staging_songs as s
                           WHERE s.artist_id IS NOT NULL
""")

time_table_insert = (""" INSERT INTO time_table( start_time, hour, day, week, month, year, weekday)
                         SELECT DISTINCT s.start_time
                         , extract(hour  from s.start_time) as hour
                         , extract(day   from s.start_time) as day
                         , extract(week  from s.start_time) as week
                         , extract(month from s.start_time) as month
                         , extract(year  from s.start_time) as year
                         , extract(dow   from s.start_time) as weekday
                         FROM songplay as s
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, time_table_create, artist_table_create, song_table_create, songplay_table_create, user_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]