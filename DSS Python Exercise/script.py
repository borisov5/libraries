# You must put this file into a database directory

import sqlite3

# Specify the database file name
database_file = 'identifier.sqlite'

# To connect to the dat file
conn = sqlite3.connect('identifier.sqlite')
cursor = conn.cursor()

# Create the "Ratings" table
cursor.execute('''CREATE TABLE IF NOT EXISTS Ratings (
                    userId INTEGER,
                    movieId INTEGER,
                    rating REAL,
                    timestamp INTEGER
                )''')

# Commit the changes
conn.commit()

# To Open the ratings.dat file and read its contents
with open('ratings.dat', 'r') as file:
    for line in file:
        # Split the line into fields based on the delimiter
        fields = line.strip().split('::')

        # Extract the values from the fields
        userId = int(fields[0])
        movieId = int(fields[1])
        rating = float(fields[2])
        timestamp = int(fields[3])

        # Construct the SQL INSERT statement
        insert_query = "INSERT INTO Ratings (userId, movieId, rating, timestamp) VALUES (?, ?, ?, ?)"

        # Execute the INSERT statement with the extracted values
        cursor.execute(insert_query, (userId, movieId, rating, timestamp))

# Commit the changes and close the connection
conn.commit()

#Create the "Movies" table
cursor.execute('''CREATE TABLE IF NOT EXISTS Movies (
                    movieId INTEGER,
                    title TEXT,
                    genres TEXT
                )''')

# Commit the changes
conn.commit()
# Open the movies.dat file and read its contents
with open('movies.dat', 'r', encoding='latin1') as file:
    for line in file:
        # Split the line into fields based on the delimiter
        fields = line.strip().split('::')

        # Extract the values from the fields
        movieId = int(fields[0])
        title = fields[1]
        genres = fields[2]

        # Construct the SQL INSERT statement
        insert_query = "INSERT INTO Movies (movieId, title, genres) VALUES (?, ?, ?)"

        # Execute the INSERT statement with the extracted values
        cursor.execute(insert_query, (movieId, title, genres))

# Commit the changes and close the connection
conn.commit()

# Create the MovieLens table
cursor.execute('''
    CREATE TABLE MovieLens AS
    SELECT Ratings.userId, Ratings.movieId, Ratings.rating, Ratings.timestamp, Movies.title, Movies.genres
    FROM Ratings
    JOIN Movies ON Ratings.movieId = Movies.movieId
''')

# Commit the changes and close the connection
conn.commit()

# QUESTION 2

# Execute the SELECT query to count the rows
cursor.execute('SELECT COUNT(*) FROM MovieLens')

# Fetch the result
row_count = cursor.fetchone()[0]

# Print the number of rows
print(f"Number of rows in MovieLens: {row_count}")

# Close the connection

# Question 3

# Execute the PRAGMA query to retrieve table schema
cursor.execute('PRAGMA table_info(MovieLens)')

# Fetch all rows of the result
columns = cursor.fetchall()

# Count the number of columns
column_count = len(columns)

# Print the number of columns
print(f"Number of columns in MovieLens: {column_count}")

# Question 4

# Execute the SELECT query to count zero ratings
cursor.execute('SELECT COUNT(*) FROM MovieLens WHERE rating = 0')

# Fetch the result
zero_rating_count = cursor.fetchone()[0]

# Print the number of zero ratings
print(f"Number of zero ratings in MovieLens: {zero_rating_count}")

# Question 5

# Execute the SELECT query to count ratings of 3
cursor.execute('SELECT COUNT(*) FROM MovieLens WHERE rating = 3')

# Fetch the result
rating_three_count = cursor.fetchone()[0]

# Print the number of ratings of 3
print(f"Number of ratings of 3 in MovieLens: {rating_three_count}")

# Question 6

# Execute the SELECT query to count distinct movies
cursor.execute('SELECT COUNT(DISTINCT movieId) FROM MovieLens')

# Fetch the result
distinct_movie_count = cursor.fetchone()[0]

# Print the number of distinct movies
print(f"Number of different movies in MovieLens: {distinct_movie_count}")

# Question 7

# Execute the SELECT query to count distinct users
cursor.execute('SELECT COUNT(DISTINCT userId) FROM MovieLens')

# Fetch the result
distinct_user_count = cursor.fetchone()[0]

# Print the number of distinct users
print(f"Number of different users in MovieLens: {distinct_user_count}")

# Question 8

# Execute the SELECT query to count movie ratings for specific genres
cursor.execute('''
    SELECT Movies.genres, COUNT(*) AS rating_count
    FROM MovieLens
    JOIN Movies ON MovieLens.movieId = Movies.movieId
    WHERE Movies.genres IN ('Drama', 'Comedy', 'Thriller', 'Romance')
    GROUP BY Movies.genres
''')

# Fetch all rows of the result
rating_counts = cursor.fetchall()

# Print the number of movie ratings for specific genres
print("Movie ratings for specific genres:")
for row in rating_counts:
    genre = row[0]
    count = row[1]
    print(f"{genre}: {count}")

# Question 9

# Execute the SELECT query to find the movie with the greatest number of ratings
cursor.execute('''
    SELECT Movies.title, COUNT(*) AS rating_count
    FROM MovieLens
    JOIN Movies ON MovieLens.movieId = Movies.movieId
    GROUP BY Movies.movieId
    HAVING rating_count = (SELECT MAX(rating_count) FROM (SELECT COUNT(*) AS rating_count FROM MovieLens GROUP BY movieId))
''')

# Fetch the result
movie_with_most_ratings = cursor.fetchone()

# Print the movie with the greatest number of ratings
if movie_with_most_ratings:
    title = movie_with_most_ratings[0]
    rating_count = movie_with_most_ratings[1]
    print(f"The movie with the greatest number of ratings is '{title}' with {rating_count} ratings.")
else:
    print("No movies found in the dataset.")

# Question 10

# Execute the SELECT query to find the five most given ratings
cursor.execute('''
    SELECT rating, COUNT(*) AS rating_count
    FROM MovieLens
    GROUP BY rating
    ORDER BY rating_count DESC
    LIMIT 5
''')

# Fetch all rows of the result
most_given_ratings = cursor.fetchall()

# Print the five most given ratings
print("Five most given ratings:")
for row in most_given_ratings:
    rating = row[0]
    rating_count = row[1]
    print(f"Rating: {rating}, Count: {rating_count}")

# Question 11

# Execute the SELECT queries to count ratings for each value from 1 to 5
cursor.execute('SELECT COUNT(*) FROM MovieLens WHERE rating = 1')
rating_1_count = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM MovieLens WHERE rating = 2')
rating_2_count = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM MovieLens WHERE rating = 3')
rating_3_count = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM MovieLens WHERE rating = 4')
rating_4_count = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM MovieLens WHERE rating = 5')
rating_5_count = cursor.fetchone()[0]

# Execute the SELECT query to count ratings not within the range of 1 to 5
cursor.execute('SELECT COUNT(*) FROM MovieLens WHERE rating NOT BETWEEN 1 AND 5')
not_within_range_count = cursor.fetchone()[0]

# Print the counts of ratings for each value from 1 to 5 and ratings not within the range
print(f"Number of ratings equal to 1: {rating_1_count}")
print(f"Number of ratings equal to 2: {rating_2_count}")
print(f"Number of ratings equal to 3: {rating_3_count}")
print(f"Number of ratings equal to 4: {rating_4_count}")
print(f"Number of ratings equal to 5: {rating_5_count}")
print(f"Number of ratings not within the range of 1 to 5: {not_within_range_count}")

# Close the connection
conn.close()
