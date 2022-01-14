# movie_watchlist
Based on 
The Complete Python/PostgreSQL Course 2.0 

From < https://www.udemy.com/course/complete-python-postgresql-database-course/> 
Section 5

What I've learned: 
- using Python to connect to PostgreSQL DB
- differences between PostgreSQL and SQLite
  - while in SQLite it is enough to declare a column as primary key to make it autoincrement, in PostgreSQL serial data type does that
  - in PostgreSQL I need to use both a connection and a cursor manager 
  - by default in PostgreSQL you cannot delete a row from the primary table if there is a row referencing it in the other table
  - %s instead of ? Is to be used for query parameters
- psycopg2 and psycopg2-binary should never be installed at once, used psycopg2-binary in this project (psycopg2 only comes in handy for more advanced stuff)
- using virtual environments in Pycharm to prevent different libraries/packages accros projects to interfere
- protecting sensitive data in the code by creating a .env file that is not to be shared and declaring there all the sensitive variables
````
    1 	#MAKING USE OF THE .ENV FILE 
    2 	import os
    3 	import psycopg2
    4 	from dotenv import load_dotenv
    5 	
    6 	load_dotenv()
    7 	#any code after this will be able to use the environment variables in the .env file
    8 	
    9 	#connecting to the DB using the environment variable
   10 	connection=psycopg2.connect(os.environ['database_url'])
   11 	#use os.environ['variable_name'] to get the value of any of the environment variables 
	#->basically a dictionary
````

What I've added to the project:
- unique constraints on the used tables so the user cannot enter duplicate data
 - exceptions caught and a print statement letting the user know that they've attempted to enter duplicate data created
- flow change:
 - from a user standpoint, I considered it redundant to have a separte option to add the user
 - instead I've included it by default on branches where the user is of interest 
