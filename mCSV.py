from mCSVRecord import CSVRecord;

class CSV:
    filename = ''
    delimiter = ','
    enclosure = '"'
    hasHeader = True
    count = 0
    data = []
    header = []

    # default constructor
    def __init__(self, file, hasHeader = True, delimit = ',', closure = '"'):
        self.filename = file
        self.hasHeader = hasHeader
        self.delimiter = delimit
        self.enclosure = closure
        self.data = []
        self.header = []
        self.count = 0

    #gets the file name
    #returns string
    def getFile(self):
        return self.filename
    
    #get the delimiter
    #returns string
    def getDelimiter(self):
        return self.delimiter

    #get the enclosure
    #returns string
    def getEnclosure(self):
        return self.enclosure

    # read the data file and parse the info
    def read(self):
        with open( self.filename, "r", encoding="utf8") as file:
        # with open( self.filename, "r") as file:
            while True:
                record = CSVRecord(self.delimiter, self.enclosure)
                line = file.readline()
                # print( self.count );
                if( len( line ) != 0 ):
                    if( self.hasHeader and self.count == 0 ):
                        record.loadString( line )
                        self.header = record
                    else:
                        record.loadString( line )
                        self.data.append( record )
                    self.count += 1
                
                #if eof stop
                if not line:
                    break
            file.close
        #only returned for testing
        #return s

    #gets the csv headers as a list
    #returns list
    def getHeaders(self):
        return self.header.getAsList()

    #get all the data as a list of CSVRecords
    #returns list[CSVRecords]
    def getData(self):
        return self.data

    #gets the row and column of an item in the csv, row is int index of the row, col is the int index of the column
    #returns str|CSVRecord
    def get(self, row, col = -1 ):
        #return the whole record
        if( col == -1 ):
            return self.data[row]
        else:
            return self.data[row].get(col)
