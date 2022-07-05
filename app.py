#!/usr/bin/env python3

"""
Requirements: Create /people and /planets endpoints.
Contacting swapi returns a json object with 4 keys: count, next, previous, and results. We shouldn't need any besides results, since previous and next are not required if all are returned at once.

/people endpoint
Should contact swapi and get all people, the swapi doesn't return all at once. It has a key "next" with the value of the next url we want to contact. Allow optional arg "sortBy", which can be set to name, height, or mass, and return the json object sorted according to the argument.

/planets endpoint
Should contact the swapi and return all planets, and should have the resident names rather than URLs to the resident info.
"""

from flask import Flask
import requests
import json

app = Flask(__name__)


@app.route('/planets')
def show_planets():
    """
    First: Want to get all of the planets into one dictionary.
    Second: Want to loop over all planets and change the value of "residents"
    to include names rather than urls.
    """

    all_planets = {"results": []}
    planets_response = requests.get("https://swapi.dev/api/planets")
    while planets_response.json()["next"] is not None:
        next_url = planets_response.json()["next"]
        planets = planets_response.json()["results"]
        for planet in planets:
            all_planets["results"].append(planet)
        planets_response = requests.get(next_url)
    # Done with first requirement. all_planets["results"] should be a list of dictionaries.

    # updated_planets is what we want to return to the user. It should be a dict with the resident names rather than than urls to resident info.
    updated_planets = {"results": []}
    for planet in all_planets["results"]:
        # Add the planet to the dict we want to return. Change the value of residents in that dict. Return as a json.
        # list of urls to residents
        resident_urls = planet["residents"]
        resident_names = []
        for url in resident_urls:
            resident_data = requests.get(url).json()
            name = resident_data["name"]
            resident_names.append(name)
            planet["residents"] = resident_names
            updated_planets["results"].append(planet)

    return updated_planets


@app.route('/people')
def show_people():
    # The default response from swapi only returns 10 people, and has the following keys: count, next, previous, results. Since we are getting all 82 in one response, we only need the results key.
    all_people = {"results": []}
    response = requests.get("https://swapi.dev/api/people")
    while response.json()["next"] is not None:
        next_url = response.json()["next"]
        # Re-define response so that by time we're back to the if statement we have a new val for response.json()["next"].
        response = requests.get(next_url)
        all_people["results"].append(response.json())

    return all_people


@app.route('/')
def wrong_path():
    return "You're in the wrong path"


if __name__ == '__main__':
    app.run()

