# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 08:32:04 2022

@author: Anamaria
"""
import os
import datetime
import psycopg2
from dotenv import load_dotenv

load_dotenv()
#any code after this will be able to use the environment variables in the .env file

connection=psycopg2.connect(os.environ['database_url'])

def create_tables():
    #tried to execute all 3 create statements in a single connection.execute -did not work - check for other options
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
            '''create table if not exists movies 
                        (id serial primary key, 
                         title text, 
                         release_date timestamp without time zone,
                         unique (title, release_date)
                        );'''
            )
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
            'create table if not exists users (id serial primary key, name text, unique (name));'
            )
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
            '''
            create table if not exists 
            watchlist (
            movie_id integer, 
            user_id integer, 
            watched integer,
            FOREIGN KEY(user_id) references users(id),
            FOREIGN KEY(movie_id) references movies(id),
            unique (movie_id,user_id)
            );
            '''
            )

def add_user_DB(username):
    #check if it works with a separate option of adding an user -maybe it needs a diff commit to see the user
    #check if the username already exists - no longer need this addded unique constraint

    #with connection:
        #with connection.cursor() as cursor:
            #cursor.execute(
                            #'select count(*) from users where name= %s',(username,)
                           # )

            #user_cnt=cursor.fetchone()[0]
            #print(f'user cnt {user_cnt}')
            #if user_cnt==0:
    with connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    'insert into users (name) values (%s);',(username,)
                    )
        except psycopg2.errors.UniqueViolation:
            #doing nothing, from a user standpoint I do not care if my user is there or not
            # from a dev standpoint I'm assuring the user is unique - all good
            pass

def add_new_movie_DB(title,date):
    with connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    'insert into movies (title, release_date) values (%s,%s);',
                    (title,date))
        except psycopg2.errors.UniqueViolation:
            print(f'Movie {title} released on {date} is already on the watchlist')

def get_movies_DB(upcoming=False):
    if not upcoming:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute('select * from movies;')
                #print(cursor.fetchall()) #list of tuples
                return cursor.fetchall()
    else:
        today_timestamp=datetime.datetime.today() #this can be used in comparison
        #print(today_timestamp)
        with connection:
            with connection.cursor() as cursor:
                cursor.execute('select * from movies where release_date > %s;',(today_timestamp,))
                #even if only one param is provide param still needs to be provided as a tuple (date) fails, while (date,) works
                return cursor.fetchall()

def mark_movie_watched_DB(user,movie):
    #improve by letting the user know if a movie has already been watched -with conttrsian on dups and catching the er?
    with connection:
    #tried to nest cursor under cursor so the 3rd one can use values from 1st and 2nd, but it gets there empty
        with connection.cursor() as movie_id_cursor:
            movie_id_cursor.execute('select id from movies where title= %s;',(movie,))
            movie_id=movie_id_cursor.fetchall()[0][0]
        with connection.cursor() as user_id_cursor:
            user_id_cursor.execute('select id from users where name=%s;',(user,))
            #print(user_id_cursor.fetchall())
            user_id=user_id_cursor.fetchall()[0][0]
        try:
            with connection.cursor() as cursor:
                cursor.execute('insert into watchlist values (%s,%s,1);',(movie_id,user_id))
        except psycopg2.errors.UniqueViolation:
            print(f'User {user} has already watched {movie}')

def get_watched_movies_DB(username):
    with connection:
        with connection.cursor() as watched_cursor:
            watched_cursor.execute('select movies.* from movies, users, watchlist where movies.id=watchlist.movie_id and users.id=watchlist.user_id and users.name=%s;',(username,))
            #print(watched_cursor.fetchall())
            return watched_cursor.fetchall()

