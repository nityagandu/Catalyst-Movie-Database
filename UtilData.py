from flask import json

import locale


class UtilData:
    data = 0

    def __init__(self, data) -> None:
        self.data = data

    #make the actors have zoomies!!
    def makeXrefActors( self ):
        s = "movie_id,id,name,role"
        s += "\n"
        i = 0
        for x in self.data:
            #rip the data out for cast
            j = json.loads( x.get( 2 ) )
            for k in j:
                s += x.get( 0 ) + "," + str( k['cast_id'] ) + "," + self.escape( k['name']) + ',' + self.escape( k['character'] )
                s += '\n'
            print( i )
            i += 1
        return s


    def makeXrefStaff( self ):
        s = "movie_id,id,name,role"
        s += "\n"
        i = 0
        for x in self.data:
            #rip the data out for cast
            j = json.loads( x.get( 3 ) )
            for k in j:
                s += x.get( 0 ) + "," + str( k['id'] ) + "," + self.escape( k['name']) + ',' + self.escape( k['job'] )
                s += '\n'
            print( i )
            i += 1
        return s
    
    #quotize that string
    def escape( self, s ):
        return '"' + s + '"'

    
    def moneyFormat( val, group = True ):
        locale.setlocale( locale.LC_ALL, '' )
        try:
            return locale.currency( int( val ), grouping=group )
        except Exception as e:
            return val
            

#endclass