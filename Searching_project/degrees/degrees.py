import pandas as pd
import sys
import csv
from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

# Reads the csv files and load data to the dictionaries names, people and movies

# Using pandas to read csv files
def load_data_pandas(directory):

    people_df = pd.read_csv(f"{directory}/people.csv")
    moveis_df = pd.read_csv(f"{directory}/movies.csv")
    stars_df = pd.read_csv(f"{directory}/stars.csv")


    ''' Load data from people csv file into the dictionary people in the form
      {people_id:{name:name, birth:birth_date, movies:{movies1,movies2,..}}}'''
    
    for _, rows in people_df.iterrows():
        people[rows['id']] = {
            'name' : rows['name'],
            'birth' : rows['birth'],
            'movies' : set()
        }

        # load data into names distionary in form {names :{name_id}}
        names_lower = rows['name'].lower()
        if names_lower not in names:
            names[rows['name']] = {rows['id']}
        else:
            names[rows['name']].add(rows['id'])
        
    
    ''' Load data from movies csv file into the dictionary movies in the form
      {movie_id:{title:movie_title, year:release_date, stars:{stars1,stars2,..}}}'''
    
    for _, rows in moveis_df.iterrows():
        movies[rows['id']] = {
            'title' : rows['title'],
            'year' : rows['year'],
            'stars' : set()
        }


    # Read the stars.csv file and load data 
     
    for _, rows in stars_df.iterrows():
        person_id = rows['person_id']
        movie_id = rows['movie_id']
        
        if person_id in people:
            people[person_id]['movies'].add(movie_id)
        
        if movie_id in movies :
            movies[movie_id]['stars'].add('person_id')



'''
# Using file operations to read the file
def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

'''

''' defining a functiont that takes person_id as the parameter and returns
 (movie_id, person_id) pair for people who starred with the given peroson'''    

def neighbor_for_person(person_id):
    movie_ids = people[person_id][movies]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]['stars']:
            neighbors.add((movie_id, person_id))
    return(neighbors)

