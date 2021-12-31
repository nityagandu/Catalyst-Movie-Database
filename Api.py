import json
from math import degrees
import re
from flask import request, abort
from Ajax import Ajax

from MovieList import MovieList

class Api():
    movies = MovieList
    def __init__(self, list) -> None:
        self.movies = list
        pass
    #fed __init__

    def call( self, method ):
        if method.lower() == 'getmovie':
            return self.getMovie()
        if method.lower() == 'getmovieslist':
            return self.getMoviesList()
        abort( 404 )
    #fed call

    def __getPostInt(self, key ):
        s = request.form.get( key )
        if s is None:
            return None
        return int( s )
    #fed __getPostInt

    def __opt(self, val, desired ):
        if val is None:
            return desired
        return desired
    #fed __opt

    def getMovie( self ):
        if request.method == 'POST':
            id = request.form.get( 'id' )
            if( id is None ):
                abort( 400 )
            ajax = Ajax()
            o = self.movies.getId( id )
            if( o is not None ):
                return ajax.data( o.toJSON() ).success( True ).toAjax();
            return ajax.data( {} ).success( False ).msg('Not Found').toAjax();
        elif request.method == 'GET':
            abort( 403 )
        abort( 400 )
    #def get

    def getMoviesList( self ):
        if request.method == "POST":
            s = self.__getPostInt( 'from')
            to = self.__getPostInt( 'to')
            p = self.__getPostInt('page' )
            limit = self.__getPostInt( 'limit' )

            out = Ajax()
            if( s is not None):
                out.data( self.movies.seek( s, to, True ) ).success( True ).makePagination( (to-s), -1, self.movies.size() )
            return out.toAjax()
        elif request.method == 'GET':
            abort( 403 ) #return "empty"
        else:
            abort( 400 )
            
    #fed getMoviesList

#ssalc Api
