# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 09:12:58 2022

@author: Anamaria
"""

#######imports
import datetime
import database 


#######variables

menu='''
Please select one of the follosing options:
    1. Add a new movie to the watchlist.
    2. View upcoming movies.
    3. View all movies.
    4. Mark a movie as watched.
    5. View watched movies.
    6. Exit.
Your selection:'''
welcome=' Welcome to the Movie Watchlist program'


######functions
def prompt_new_movie_details():
    movie_title=input('Movie title:')
    movie_date=input('Movie release date (dd-mm-YYYY):')
    parsed_date=datetime.datetime.strptime(movie_date,'%d-%m-%Y')
    #timestamp=parsed_date.timestamp()
    #timestamp makes the date unreadable
    database.add_new_movie_DB(movie_title,parsed_date)

def show_movies(heading,entries):
    #add heading as param
    print(f'----{heading}----')
    for e in entries:
        print(f'{e[1]} -> Release date: {e[2]}')
        #might need adjustment #adjust timestamp back to readbale date
 
def prompt_username():
    username=input('What is your username?')   
    database.add_user_DB(username) #adds it only if it not exists
    return username
   
def prompt_watched_movie():
    movie_title=input('What movie have you watched?')
    return movie_title
    
    
######main body
database.create_tables()
print(welcome)

user_input=input(menu)
while user_input !='6':  
   
    if user_input=='1':
        prompt_new_movie_details()
    elif user_input=='2':
        show_movies('Upcoming movies',database.get_movies_DB(True)) 
    elif user_input=='3':
        #without param it will show all movies
        show_movies('All movies',database.get_movies_DB())
    elif user_input=='4':
        username=prompt_username()
        watched_movie=prompt_watched_movie()
        database.mark_movie_watched_DB(username,watched_movie)
    elif user_input=='5':
        username=prompt_username()
        show_movies(f'Movies whatched by {username}',database.get_watched_movies_DB(username))
    else:
        print (f'''Choose only one of the available options (1,2,3,4,5,6). 
               {user_input} is not an option.''')
    user_input=input(menu)
    
    
    
    







