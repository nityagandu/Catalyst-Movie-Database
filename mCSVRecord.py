import json
import re

class CSVRecord:
    data = []
    delim = ','
    closure = '"'

    #constructor
    def __init__(self, delim = ',', closure = '"'):
        self.data = []
        self.delim = delim
        self.closure = closure
    #fed __init__

    #set data from a list
    def setData( self, l ):
        self.data = l
    #fed setData

    #loads a string into the record
    #returns null
    def loadString(self, line):
        self.data = self.split( line ); #line.split( self.delim );

    #split the single line of the csv into the columns
    #returns list
    def split( self, line):
        line = line.strip( "\r\n")
        data = []
        delim = self.delim
        cl = self.closure
        cols = 0
        #regex to split this mess
        regex = re.escape( delim ) + r'(?=(?:[^' + re.escape( cl ) + r']*' + re.escape( cl ) + r'[^' + re.escape( cl ) + r']*' + re.escape( cl ) + r')*(?![^' + re.escape( cl ) + r']*' + re.escape( cl ) + r'))'
        #fields of the line split into array
        spLine = re.split( regex, line )
        for x in spLine:
            #remove the front & tailing quotes
            if x.startswith( cl ) and x.endswith( cl ):
                x = x[1:-1]
            #if json unescape the quotes
            if x.startswith( '[' ) and x.endswith( ']' ) or x.startswith( '{' ) and x.endswith( '}' ):
                x = re.sub( cl + cl, cl, x )
            data.append( x )
            cols += 1
        return data
    #fed split
      
    #get record as a string
    #returns string
    def str( self ):    
        return self.delim.join( self.data )

    #get record as a list
    #returns list
    def getAsList( self ):
        return self.data

    #get column in the list, i is the int index of the column
    #returns string, if out of bounds returns empty string
    def get( self, i ):
        if( i >= len( self.data ) ):
            return ''
        return self.data[i]

    #get column in the list as json, i is the int index of the column
    #returns json
    def getJSON( self, i ):
        s = self.data[i]
        j = json.loads( s )
        return j

    #get column in the list as json encoded str, i is the int index of the column
    #returns str
    def getJSONStr( self, i ):
        s = self.data[i]
        j = json.loads( s )
        return str( j )
    