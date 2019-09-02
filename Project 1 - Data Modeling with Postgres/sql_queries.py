'''DROP TABLES'''

songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS songs"

'''CREATE TABLES'''

songplay_table_create = ("""
                            CREATE TABLE IF NOT EXISTS songplay(songplay_id serial PRIMARY KEY, start_time timestamp NOT NULL, user_id int NOT NULL\
                                 , level text NULL, song_id text NULL UNIQUE, artist_id text NULL, session_id int NULL, location text NULL, user_agent text NULL);  
""")

user_table_create = ("""
                        CREATE TABLE IF NOT EXISTS users(user_id int NOT NULL UNIQUE, first_name text NULL, last_name text NULL, gender text NULL, level text NULL);
""")

song_table_create = ("""
                        CREATE TABLE IF NOT EXISTS songs(song_id text NOT NULL UNIQUE, title text NULL, artist_id text NOT NULL, year int NULL, duration decimal NULL);
                        
""")

artist_table_create = ("""
                         CREATE TABLE IF NOT EXISTS artists(artist_id text NOT NULL UNIQUE, name text NULL, location text NULL, latitude text NULL, longitude text NULL);
""")

time_table_create = ("""
                        CREATE TABLE IF NOT EXISTS time (start_time timestamp NOT NULL UNIQUE, hour int NOT NULL, day int NOT NULL, week int NOT NULL, month int\
                                                              , year int NOT NULL, weekday int NOT NULL );
""")

'''INSERT RECORDS'''

songplay_table_insert = ("""INSERT INTO songplay (start_time, user_id, level,song_id,artist_id,session_id,location,user_agent) VALUES (%s, %s, %s, %s,%s, %s, %s, %s) ON CONFLICT(song_id) DO NOTHING""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level) VALUES (%s, %s, %s, %s, %s) ON CONFLICT(user_id) DO UPDATE SET level = EXCLUDED.level """)

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration) VALUES (%s, %s, %s, %s, %s) ON CONFLICT(song_id) DO NOTHING""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, latitude, longitude) VALUES (%s, %s, %s, %s, %s) ON CONFLICT(artist_id) DO NOTHING""")

time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT(start_time) DO NOTHING""")

'''FIND SONGS'''

song_select = (""" SELECT S.song_id, S.artist_id from songs AS S JOIN artists AS A ON A.artist_id = S.artist_id WHERE s.title = (%s) AND a.name = (%s) AND s.duration=(%s); """)

'''QUERY LISTS'''

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]