from Serializable import Serializable
from mCSVRecord import CSVRecord
import json;
import re;

class Movie(Serializable):
    budget = 0
    genres = []
    homepage = ''
    id = 0
    keywords = []
    orgLang = ''
    orgtitle = ''
    overview = ''
    popularity = 0.0
    productionCompanies = []
    productionCountries = []
    releaseDate = ''
    revenue = 0
    runtime = 0
    spokenLanguages = []
    status = ''
    tagline = ''
    title = ''
    voteAverage = 0.0
    voteCount = 0

    def __init__(self):
        self.genres = []
        self.keywords = []
        self.productionCompanies = []
        self.productionCountries = []
        self.spokenLanguages = []

    #load the data from a csv record, data is the CSVRecord
    def load(self, data ):
        #0          1       2           3   4
        #budget	    genres	homepage	id	keywords	original_language	original_title	overview	popularity	production_companies	production_countries	release_date	revenue	runtime	spoken_languages	status	tagline	title	vote_average	vote_count
        #get simple data first
        self.budget = data.get(0)
        self.homepage = data.get(2)
        self.id = data.get(3)
        self.orgLang = data.get(5)
        self.orgtitle = data.get(6)
        self.overview = data.get(7)
        self.popularity = data.get(8)
        self.releaseDate = data.get(11)
        self.revenue = data.get(12)
        self.runtime = data.get(13)
        self.status = data.get(15)
        self.tagline = data.get(16)
        self.title = data.get(17)
        self.voteAverage = data.get(18)
        self.voteCount = data.get(19)

        #get json data
        j = data.getJSON( 1 )
        for x in j:
            self.genres.append( x['name'] )
        j = data.getJSON(4)
        for x in j:
            self.keywords.append( x['name'] )
        j = data.getJSON( 9 )
        for x in j:
            self.productionCompanies.append( x['name'] )
        j = data.getJSON( 10 )
        for x in j:
            self.productionCountries.append( x['name'] )
        j = data.getJSON( 14 )
        for x in j:
            self.spokenLanguages.append( x['name'] )
    #end load fn

    def str(self):
        #todo this is just for testing
        return self.title

    #prints record out in csv form
    def toCSV(self):
        out = self.budget + ','
        temp = []
        for x in self.genres:
            temp.append( { 'name' : x } )
        temp = re.sub( '"', '""', json.dumps( temp ) )
        out += '"' + temp + '",'
        out += '"' + self.homepage + '",'
        out += self.id + ','

        temp = []
        for x in self.keywords:
            temp.append( { 'name' : x } )
        temp = re.sub( '"', '""', json.dumps( temp ) )
        out += '"' + temp + '",'

        out += '"' + self.orgLang + '",'
        out += '"' + self.orgtitle + '",'
        out += '"' + self.overview + '",'
        out += self.popularity + ','
        
        temp = []
        for x in self.productionCompanies:
            temp.append( { 'name' : x } )
        temp = re.sub( '"', '""', json.dumps( temp ) )
        out += '"' + temp + '",'

        temp = []
        for x in self.productionCountries:
            temp.append( { 'name' : x } )
        temp = re.sub( '"', '""', json.dumps( temp ) )
        out += '"' + temp + '",'

        out += self.releaseDate + ','
        out += self.revenue + ','
        out += self.runtime + ','

        temp = []
        for x in self.spokenLanguages:
            temp.append( { 'name' : x } )
        temp = re.sub( '"', '""', json.dumps( temp ) )
        out += '"' + temp + '",'

        out += '"' + self.status + '",'
        out += '"' + self.tagline + '",'
        out += '"' + self.title + '",'
        out += self.voteAverage + ','
        out += self.voteCount + ','
        return out
    #fed toCSV()

    def toJSON( self ):
        o = {}
        o['budget'] = self.budget
        o['genres'] = self.genres
        o['homepage'] = self.homepage
        o['id'] = self.id

        o['keywords'] = self.keywords

        o['orgLang'] = self.orgLang
        o['orgtitle'] = self.orgtitle
        o['overview'] = self.overview
        o['popularity'] = self.popularity
        
        o['productionCompanies'] = self.productionCompanies

        o['productionCountries'] = self.productionCountries

        o['releaseDate']= self.releaseDate
        o['revenue']= self.revenue
        o['runtime']= self.runtime

        o['spokenLanguages'] = self.spokenLanguages
           

        o['status'] = self.status
        o['tagline'] = self.tagline
        o['title'] = self.title
        o['voteAverage']= self.voteAverage
        o['voteCount']= self.voteCount
        return o
    #fed toJSON


    def setbudget(self,x):
        self.budget = x

    def setgenres(self,x):
        self.genres = x

    def sethomepage(self,x):
        self.homepage = x

    def setid(self,x):
        self.id = x

    def setkeywords(self,x):
        self.keywords = x

    def setorgLang(self,x):
        self.orgLang = x

    def setorgtitle(self,x):
        self.orgtitle = x

    def setoverview(self,x):
        self.overview = x

    def setpopularity(self,x):
        self.popularity = x

    def setproductionCompanies (self,x):
        self.productionCompanies = x

    def setproductionCountries (self, x):
        self.productionCountries = x

    def setreleaseDate(self, x):
        self.releaseDate = x

    def setrevenue(self, x):
        self.revenue = x

    def setruntime(self, x):
        self.runtime = x

    def setspokenLanguages(self, x):
        self.spokenLanguages = x

    def setstatus(self, x):
        self.status = x

    def settagline(self, x):
        self.tagline = x

    def settitle(self, x):
        self.title = x

    def setvoteAverage(self, x):
        self.voteAverage = x

    def setvoteCount(self, x):
        self.voteCount = x

    def getbudget(self):
        return self.budget

    def getgenres (self):
        return self.genres

    def gethomepage (self):
        return self.homepage

    def getid(self):
        return self.id

    def getkeywords(self):
        return self.keywords

    def getorgLang(self):
        return self.orgLang

    def getorgtitle(self):
        return self.orgtitle

    def getoverview(self):
        return self.overview

    def getpopularity(self):
        return self.popularity

    def getproductionCompanies(self):
        return self.productionCompanies

    def getproductionCountries (self):
        return self.productionCountries

    def getreleaseDate(self):
        return self.releaseDate

    def getrevenue(self):
        return self.revenue

    def getruntime(self):
        return self.runtime

    def getspokenLanguages (self):
        return self.spokenLanguages

    def getstatus(self):
        return self.status

    def gettagline(self):
        return self.tagline

    def gettitle(self):
        return self.title

    def getvoteAverage(self):
        return self.voteAverage

    def getvote_count(self):
        return self.voteCount
