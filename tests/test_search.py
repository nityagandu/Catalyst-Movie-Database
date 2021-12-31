from main import app
from flask import json

from MovieList import MovieList

global mList;
mList = MovieList();

def test_titleSearch_valid():
    response = app.test_client().post(
        '/titleSearch',
        data=json.dumps("Pirates of the Caribbean: At World's End"),
        content_type='application/json',
    )
    output = json.loads(response.get_data(as_text=True))

    if( output is not None ):
        #print(json.loads(output[0]))
        movie = json.loads(output[0])
        assert movie['title'] == "Pirates of the Caribbean: At World's End"


def test_titleSearch_invalid():
    response = app.test_client().post(
        '/titleSearch',
        data=json.dumps("invalid movie name"),
        content_type='application/json',
    )
    output = json.loads(response.get_data(as_text=True))

    if( output is not None ):
        #print(output[0])
        movie = output[0]
        assert movie['name'] == "Page Does Not Exist"


def test_ratingSearch_valid():
    response = app.test_client().post(
        '/ratingSearch',
        data=json.dumps("7.2"),
        content_type='application/json',
    )
    output = json.loads(response.get_data(as_text=True))

    if( output is not None ):
        #print(json.loads(output[0]))
        movie = json.loads(output[0])
        assert movie['voteAverage'] == "7.2"


def test_ratingSearch_invalid():
    response = app.test_client().post(
        '/ratingSearch',
        data=json.dumps(-1),
        content_type='application/json',
    )
    output = json.loads(response.get_data(as_text=True))

    if( output is not None ):
        #print(output[0])
        movie = output[0]
        assert movie['name'] == "Page Does Not Exist"


def test_genreSearch_valid():
    response = app.test_client().post(
        '/genreSearch',
        data=json.dumps("Action"),
        content_type='application/json',
    )
    output = json.loads(response.get_data(as_text=True))

    if( output is not None ):
        print(json.loads(output[0])['genres'])
        movie = json.loads(output[0])
        assert movie['genres'] == ['Action', 'Adventure', 'Fantasy', 'Science Fiction']


def test_genreSearch_invalid():
    response = app.test_client().post(
        '/genreSearch',
        data=json.dumps("invalid genre type"),
        content_type='application/json',
    )
    output = json.loads(response.get_data(as_text=True))

    if( output is not None ):
        print(output[0])
        movie = output[0]
        assert movie['name'] == "Page Does Not Exist"
