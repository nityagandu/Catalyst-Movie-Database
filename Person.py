from datetime import datetime
import json

from Serializable import Serializable


class Person(Serializable):
    def __init__(self) -> None:
        self.name = ''
        self.role = ''
        self.id = -1
        self.movieId = -1

    def load(self, data):
        self.movieId = int( data.get(0) )
        self.id = int( data.get(1) )
        self.name = data.get(2)
        self.role = data.get(3)
        pass

    def toJSON( self ):
        o = {}
        o['name'] = self.name
        o['role'] = self.role
        o['id'] = self.id
        o['movieId'] = self.movieId
        return o


class Actor(Person):
    def __init__(self) -> None:
        super().__init__()

class Staff(Person):
    def __init__(self) -> None:
        super().__init__()