class MList:
    data = []
    def __init__(self) -> None:
        self.data = []

    def size( self ) -> int:
        return len( self.data )

    def clear( self ):
        self.data.clear()

    def toJSON( self ):
        o = []
        for x in self.data:
            o.append( x.toJSON() )
        return o

    def get( self, i ):
        return self.data[i]

    def set( self, i, d ):
        self.data[i] = d

    def rm( self, i ):
        del self.data[i]
        
    def getData( self ):
        return self.data

    def append( self, m ):
        self.data.append( m )

    