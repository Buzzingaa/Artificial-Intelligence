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
    movies_df = pd.read_csv(f"{directory}/movies.csv")
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
            names[rows['name'].lower()] = {rows['id']}
        else:
            names[rows['name'].lower()].add(rows['id'])
        
    
    ''' Load data from movies csv file into the dictionary movies in the form
      {movie_id:{title:movie_title, year:release_date, stars:{stars1,stars2,..}}}'''
    
    for _, rows in movies_df.iterrows():
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
            movies[movie_id]['stars'].add(person_id)



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

# Define the main funtion
def main():
    if len(sys.argv)>2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from file into memory
    print("Loading data...")
    load_data_pandas(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


# Define the fucntion that takes two person's id as input and reutrns the shortest path 
def shortest_path(source, target):
     """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
     
     # Initialize the frontier with the starting node
     frontier = QueueFrontier()
     start = Node(state = source, parent = None, action = None)
     frontier.add(start)
     
     # Initialize an empty set of explored nodes
     explored = set()

     # Perfom the search
     while not frontier.empty():
         node = frontier.remove()

         #check the node, if its the target node then reconstruct the path
         if node.state == target:
            path = []
            while node.parent != None:
                path.append((node.action, node.state))
                node = node.parent
            path.reverse()
            return path
         
         explored.add(node.state)
         
         # Explore the neighbor of the node
         for movie_id, person_id in neighbor_for_person(node.state):
             if person_id not in explored and not frontier.contains_state(person_id):
                 child = Node(state = person_id, parent = node, action = movie_id )
                 frontier.add(child)
     return None            
        
            






''' defining a functiont that takes person_id as the parameter and returns
 (movie_id, person_id) pair for people who starred with the given peroson'''    

def neighbor_for_person(person_id):
    movie_ids = people[person_id]['movies']
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]['stars']:
            neighbors.add((movie_id, person_id))
    return(neighbors)



""" Define a function that returns the IMDB id of a person's name
    and solves the ambiguities if necessary """
 
def person_id_for_name(name):
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which {name}")
        for person in person_ids:
            print(f"Person : {people[person]}")
            print(f"Name : {people[person]['name']}")
            print(f"Birth : {people[person]['birth']}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]

if __name__ == "__main__":
    main()
