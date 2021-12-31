import json
from MList import MList
from mCSV import CSV
from Movie import Movie

class MovieList(MList):
    #array
    data = []
    file = ''
    headers = []

    def __init__(self):
        super().__init__()

    def load(self, file):
        csv = CSV( file )
        s = csv.read()
        self.headers = csv.getHeaders()
        data = csv.getData()
        #free up space
        csv = None
        #load the movies
        for x in data:
            m = Movie()
            m.load( x )
            self.data.append( m )
        return self.data

    # abstracted in MList
    #DANGEROUS function call    
    #clears the movies out of the list this is DANGEROUS
    # def clear( self ):
    #     self.data.clear();
    #fed clear

    def getMovies(self):
        return self.data
    
    def exportMovies( self, filename ):
        s = ""
        s += ",".join(f'"{w}"' for w in self.headers)
        s += "\n"
        i = 0
        for x in self.data:
            s += x.toCSV()
            s += '\n'
            # print( i )
            i +=1
            # if( i == 30 ):
            #     break;
        return s

    # abstracted in MList
    # def toJSON(self):
    #     o = [];
    #     for x in self.data:
    #         o.append( x.toJSON() )
    #     return o;

    #seek from a start position to end position
    def seek( self, start, offset, json = False):
        i = start
        j = offset - start
        data = []
        for x in self.data:
            if( i != j ):
                if( json ):
                    data.append( x.toJSON() )
                else:
                    data.append( x )
                i += 1
            else:
                break
        return data

    # abstracted in MList
    # def get(self, i):
    #     return self.data[i];

    def getId(self, id):
        id = str( id )
        for x in self.data:
            if( id == x.id ):
               return x
        return None

    def append( self, m ):
        if( isinstance( m, Movie ) ):
            self.data.append( m )
        else:
            print( "ERROR: " + str( m ) + " tried to insert into a Movie list")
    
    # abstracted in MList
    # def size(self):
    #     return len( self.data )

    def searchTitle(self, q):
        o = []
        for x in self.data:
            if( q.upper() in x.title.upper() ):
                o.append( x.toJSONStr() )
        if( len( o ) == 0 ):
            return None
        return o

    def searchTitleExact(self, q):
        o = []
        for x in self.data:
            if( q.upper() == x.title.upper() ):
                o.append( x.toJSONStr() )
        if( len( o ) == 0 ):
            return None
        return o