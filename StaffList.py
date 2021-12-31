from MList import MList
from Person import Staff;
from mCSV import CSV
class StaffList( MList ):
    def __init__(self) -> None:
        super().__init__()

    def load( self, file):
        csv = CSV( file )
        s = csv.read()
        self.headers = csv.getHeaders()
        data = csv.getData()
        #free up space
        csv = None
        #load the movies
        for x in data:
            m = Staff()
            m.load( x )
            self.append( m )
        return self.data

