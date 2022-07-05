#!/usr/bin/env python3

"""
Requirements: Create /people and /planets endpoints.
Contacting swapi returns a json object with 4 keys: count, next, previous, and
results. We shouldn't need any besides results, since previous and next are
not required if all are returned at once.

/people endpoint
Should contact swapi and get all people, the swapi doesn't return all at once.
Allow optional arg "sortBy", which can accept parameters name, height, or
mass, and return the json object sorted according to the parameter provided.

/planets endpoint
Should contact the swapi and return all planets, and should have the resident
names rather than URLs to the resident info.
"""

from flask import Flask, request
import requests
# For some reason jsonify still puts an ugly response out.
from json import dumps

app = Flask(__name__)


@app.route('/planets', methods=['GET'])
def show_planets():
    """
    First: Want to get all of the planets into one dictionary.
    Second: Want to loop over all planets and change the value of "residents"
    to include names rather than urls, and put that in another dictionary, and
    return that.
    """

    all_planets = {"results": []}
    planets_response = requests.get("https://swapi.dev/api/planets")
    while planets_response.json()["next"] is not None:
        next_url = planets_response.json()["next"]
        planets = planets_response.json()["results"]
        for planet in planets:
            all_planets["results"].append(planet)
        planets_response = requests.get(next_url)
    # Done with Afirst requirement.

    """
    updated_planets is what we want to return to the user. It should be a dict
    with the resident names rather than than urls to resident info.
    """
    updated_planets = {"results": []}
    for planet in all_planets["results"]:
        """
        For each planet, create a list of resident names, then change the value
        of planets["residents"] to that. Then add the updated planet info to
        updated_planets.
        """
        resident_urls = planet["residents"]
        resident_names = []
        for url in resident_urls:
            resident_data = requests.get(url).json()
            name = resident_data["name"]
            resident_names.append(name)
            planet["residents"] = resident_names
            updated_planets["results"].append(planet)

    return dumps(updated_planets, indent=3)


@app.route('/people', methods=['GET'])
def show_people():
    """
    First: Get all people in a list, make that list the value of a dictionary.
    Second: If the user requested the list be sorted by mass, height, or name,
    then return the sorted list
    """
    all_people = {"results": []}
    response = requests.get("https://swapi.dev/api/people")
    while response.json()["next"] is not None:
        next_url = response.json()["next"]
        response = requests.get(next_url)
        for person in response.json()["results"]:
            all_people["results"].append(person)

    # Now we want to see if they requested sortBy=*.
    sort_by = request.args.get("sortBy")
    if sort_by is not None:
        unsorted_people = all_people["results"]
        supported_sort_params = ["mass", "height", "name"]
        if sort_by not in supported_sort_params:
            return 'Unable to sort by the parameter %s.' % sort_by, 400
        else:
            # Sort the list by the provided parameter.
            sorted_list = (sorted(unsorted_people, key=lambda i: i[sort_by]))
            all_people["results"] = sorted_list
            return dumps(all_people, indent=3)

    else:
        return dumps(all_people, indent=3)


@app.route('/', methods=['GET'])
def show_usage():
    return "Usage:\ncurl http://127.0.0.1:5000/people?sortBy=mass\ncurl http://127.0.0.1:5000/planets\n"


if __name__ == '__main__':
    app.run()

