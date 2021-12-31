from typing import OrderedDict
from flask import Flask, redirect, url_for, render_template, request, Response, abort, jsonify
import json, os, random, os.path, copy, datetime, time

from werkzeug.datastructures import Headers
from werkzeug.utils import secure_filename
from ActorList import ActorList
from Api import Api
from MList import MList
from Movie import Movie
from Person import Actor
from UtilData import UtilData
from mCSV import CSV #this is not python csv
from MovieList import MovieList

from StaffList import StaffList
import concurrent.futures;

UPLOAD_FOLDER = 'data/'
ALLOWED_EXTENSIONS = {'csv', 'txt'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.static_folder = 'static'

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

def loadMovies():
    print( 'loading movies...')
    m = MovieList()
    m.load("data/movies.csv"); #change to data/movies.csv later when done testing
    print( 'loaded movies')
    return m

def loadActors():
    print( 'loading actors...')
    a = ActorList()
    a.load( "data/data_actors.csv" )
    print( 'loaded actors')
    return a

def loadStaff():
    print( 'loading staff...')
    s = StaffList()
    s.load( "data/data_staff.csv" )
    print( 'loaded staff')
    return s

#global variables
global mList
global aList
global sList
global API
API = None
mList = MovieList()
aList = ActorList()
sList = StaffList()

global incrementalProduction
incrementalProduction = {}

global incrementalProfit
incrementalProfit = {}

def init():
    futures=[]
    with concurrent.futures.ThreadPoolExecutor() as exec:
        futures.append( exec.submit( loadMovies ) )
        futures.append( exec.submit( loadActors ) )
        futures.append( exec.submit( loadStaff ) )
        for future in concurrent.futures.as_completed(futures):
            if( type( future.result() ) == MovieList ):
                globals()['mList'] = future.result()
                globals()['API'] = Api( globals()['mList'] )
            elif( type( future.result() ) == ActorList ):
                globals()['aList'] = future.result()
            elif( type( future.result() ) == StaffList ):
                globals()['sList'] = future.result()
    
    print( "Done!")
    
init()


#homepage
@app.route("/", methods=["POST", "GET"])
def home():
    return movieTable()
    if request.method == "POST":
        input = request.form["search-input"]
        return redirect(url_for("content", input=input))
    else:
        return render_template("index.html")


@app.route("/titleSearch", methods=["POST", "GET"])
def titleSearch():
    titleFound = False
    if request.method == "POST":
        title = request.get_json()
        d = mList.searchTitle( title )
        if( d is not None ):
            return json.dumps( d )
        return json.dumps([{'name': "Page Does Not Exist"}])
    else:
        return render_template("titleTemplate.html")


@app.route("/ratingSearch", methods=["POST", "GET"])
def ratingSearch():
    voteAverageFound = False
    if request.method == "POST":
        voteAverage = request.get_json() #grabs the user search value
        li = mList.getData()
        search_list = []
        for movie in li:
            #print(movie.getvoteAverage())
            if (voteAverage == movie.getvoteAverage()):
                voteAverageFound = True
                search_list += mList.searchTitleExact( movie.gettitle() )

        if voteAverageFound:
            return json.dumps( search_list )
        else:
            return json.dumps([{'name': "Page Does Not Exist"}])
    else:
        return render_template("ratingTemplate.html")


@app.route("/genreSearch", methods=["POST", "GET"])
def genreSearch():
    genreFound = False
    if request.method == "POST":
        user_val = request.get_json().upper()
        li = mList.getData()
        search_list = []
        for movie in li: #for each movie
            #print(movie.getvoteAverage())
            for genre in movie.getgenres(): #for each genre in movie
                #print(genre)
                if genre.upper() == user_val:
                    genreFound = True
                    search_list += mList.searchTitleExact( movie.gettitle() )
                    break

        if genreFound:
            return json.dumps( search_list )
        else:
            return json.dumps([{'name': "Page Does Not Exist"}])
    else:
        return render_template("genreTemplate.html")

@app.route("/releaseDateSearch", methods=["POST", "GET"])
def releaseDateSearch():
    releaseDateFound = False
    if request.method == "POST":
        releaseDate = request.form["search-input"]
        li = mList.getData()
        for x in li:
            print(x.releaseDate)
            if (releaseDate == x.releaseDate):
                releaseDateFound = True
                return redirect(url_for("content", input=releaseDate))
        
        if not releaseDateFound:
            return redirect(url_for("content", input="Page Does Not Exist"))
    else:
        return render_template("releaseDateTemplate.html")

#the most expensive movie given a time period
@app.route("/datePeriodSearch", methods=["POST", "GET"])
def datePeriodSearch():
    startTime = time.time()
    tempList = []
    sDateFound = False
    eDateFound = False
    if request.method == "POST":
        print( 'here' )
        startDate = request.form["trip-start"] 
        endDate = request.form["trip-end"]
        #time.
        sDate = datetime.datetime.strptime(startDate, "%Y-%m-%d") 
        eDate =  datetime.datetime.strptime(endDate, "%Y-%m-%d") 
        li = mList.getData()
        for x in li:
            releaseDate = x.releaseDate 
            if releaseDate == '':
                continue
            #TODO edge case of years before 1/1/1970
            rDate = datetime.datetime.strptime(releaseDate, "%Y-%m-%d")
            if (sDate < rDate):
                sDateFound = True
                if (eDate > rDate):
                    eDateFound = True
                    x.budget = int( x.budget )
                    tempList.append(x.toJSON())
        expMovies = sorted(tempList, key=lambda Movies: Movies.get('budget'), reverse=True)
        #TODO what if 0 movies match
        for x in range( len( expMovies ) ):
            expMovies[x]['budget'] = UtilData.moneyFormat( expMovies[x]['budget'] )
            expMovies[x]['revenue'] = UtilData.moneyFormat( expMovies[x]['revenue'] )
        # return redirect(url_for("content", input=releaseDate))
        endTime = time.time()
        print("--- %s seconds ---" % (endTime - startTime))
        return render_template("dateCalendar.html", data=expMovies)

        
        if not sDateFound or eDateFound:
            return redirect(url_for("content", input="Page Does Not Exist"))
    else:
        return render_template("dateCalendar.html")

@app.route("/productionCountriesSearch", methods=["POST", "GET"])
def productionCountriesSearch():
    tempList = [];
    productionCountriesFound = False
    if request.method == "POST":
        productionCountries = request.form["search-input"]
        li = mList.getData()
        for x in li:
            print(x.productionCountries)
            for z in x.productionCountries:
                if ( productionCountries.upper() in z.upper() ):
                    productionCountriesFound = True
                    tempList.append( x )
        rateMovies = sorted( tempList, key=lambda Movies: Movies.voteAverage, reverse=True )
        
        return render_template("productionCountryTemplate.html", data=rateMovies)
        
        if not productionCountriesFound:
            return redirect(url_for("content", input="Page Does Not Exist"))
    else:
        return render_template("productionCountryTemplate.html", data=None)

@app.route("/productionCompaniesSearch", methods=["POST", "GET"])
def productionCompaniesSearch():
    productionCompaniesFound = False
    if request.method == "POST":
        productionCompanies = request.form["search-input"]
        li = mList.getData()
        for x in li:
            for z in x.productionCompanies:
                if ( productionCompanies.upper() in z.upper() ):
                    productionCompaniesFound = True
                    return redirect(url_for("content", input=z))
        
        if not productionCompaniesFound:
            return redirect(url_for("content", input="Page Does Not Exist"))
    else:
        return render_template("productionCompanyTemplate.html")


#top 25 rated movies by production company
@app.route("/productionCompany", methods=["POST", "GET"])
def productionCompany():
    topNMovies = 25
    startTime = time.time()

    if request.method == "POST":
        li = mList.getData()
        searchComp = request.form["search-input"]

        topFiveMovies = []
        incremental = globals()['incrementalProduction']

        if( incremental.get(searchComp) ):
            #one gross hotfix
            sortl = []
            for k,v in incremental.get(searchComp).items():
                sortl.append( v )
            sortl = sorted( sortl, key=lambda x: x.get("voteAverage"), reverse=True)
            sortl = {sub['id'] : sub for sub in sortl}
            #end gross hotfix
            endTime = time.time()
            print("--- %s seconds ---" % (endTime - startTime))
            return render_template("productionCompanyTemplate.html", data=sortl)

        for movie in li:
            for company in movie.productionCompanies:
                if ( searchComp.upper() in company.upper() ): #if same production company as the one given by user
                    topFiveMovies.append( movie.toJSON() )
 
        tempList = sorted(topFiveMovies, key=lambda x: x.get("voteAverage"), reverse=True)
        #trim to 25 entries
        #map-reduce the data to remove duplicates
        orderedMap = OrderedDict()
        #map reduce to 
        for x in tempList:
            #keep the limit only at 25 stop once we reach this
            if( len( orderedMap ) == topNMovies ):
                break
            orderedMap[ x['id'] ] = x
        
        
        # print( json.dumps(res, indent=4, sort_keys=True))

        # removed pretty print for final value
        globals()['incrementalProduction'] = { searchComp: orderedMap }
        endTime = time.time()
        print("--- %s seconds ---" % (endTime - startTime))
        return render_template("productionCompanyTemplate.html", data=orderedMap)

    else:
        endTime = time.time()
        print("--- %s seconds ---" % (endTime - startTime))
        return render_template("productionCompanyTemplate.html", data=None)
    

@app.route("/directorsSuccess", methods=["POST", "GET"])
def directorsSuccess():
    if request.method == "POST":
        searchDirector = request.form["search-input"]
        templist1 = []
        templist2 = []
        li = mList.getData()

        staffList = sList.getData()
        for x in staffList:
            if searchDirector.upper() in x.name.upper():
                if x.role.upper() == 'director'.upper():
                    print(x.movieId)
                    templist1.append(x)

        for i in templist1:
            o = i.toJSON()
            m = mList.getId(i.movieId)
            print(m.title)
            o['title'] = m.title
            o['revenue'] = float(m.revenue)
            print(m.title)
            templist2.append(o)
        
        directorsSucList = sorted(templist2, key= lambda x: (x['name'], x['revenue']), reverse=True)

        return render_template('directorsSuc.html', data=directorsSucList)
    else:
        return render_template('directorsSuc.html', data=None)

@app.route("/actorPopularity", methods=["POST", "GET"])
def actorPopularity():
    if request.method == "POST":
        searchActor = request.form["search-input"]
        tempList = []
        outs = []
        li = aList.getData()
        
        for x in li:
            # print(x.name)
            if searchActor.upper() in x.name.upper():
                tempList.append(x)
        
        for i in tempList:

            o = i.toJSON()
            # print( i.movieId )
            m = mList.getId( i.movieId )
            # print( mList.getData()[0].toJSON() )
            o['title'] = m.title
            o['popularity'] = float( m.popularity )
            o['movieId'] = m.id
            outs.append( o )
        
        actorPop = sorted( outs , key=lambda x: ( x['name'], x['popularity'] ), reverse=True)

        return render_template("actorPopTemp.html", data=actorPop)
    else:
        return render_template("actorPopTemp.html", data=None)

@app.route("/inputData", methods=["POST", "GET"])
def inputData():
    if request.method == 'POST':
        # if request.form.get('action') == 'add':
        movieName = request.form["movieName"]
        movieStatus = request.form["movieStatus"]
        movieReleaseDate = request.form["movieReleaseDate"]
        movieBudget = request.form["movieBudget"] or "0"
        movieGenres = request.form["movieGenres"].split(",")
        
        movieHomepage = request.form["movieHomepage"]
        movieKeywords = request.form["movieKeywords"].split(",")

        movieOrgLang = request.form["movieOrgLang"]
        movieOrgTitle = request.form["movieOrgTitle"]
        movieOverview = request.form["movieOverview"]
        moviePopularity = request.form["moviePopularity"]
        movieProductionCompany = request.form["movieProductionCompany"].split(",")

        movieProductionCountries = request.form["movieProductionCountries"].split(",")

        movieRevenue = request.form["movieRevenue"] or "0"
        movieRuntime = request.form["movieRuntime"]
        movieSpokenLang = request.form["movieSpokenLang"].split(",")

        movieTagline = request.form["movieTagline"]
        movieVoteAv = request.form["movieVoteAv"]  or "0.0"
        movieVoteCount = request.form["movieVoteCount"]

        temp = Movie()

        #get an unused id
        id = -1
        while True:
            id = random.randint(1, 555555)
            if( mList.getId( id ) is None ):
                break
        temp.setid( str( id ) )
        temp.settitle(movieName)
        temp.setstatus(movieStatus)
        temp.setreleaseDate(movieReleaseDate)
        temp.setbudget(movieBudget)
        temp.setgenres(movieGenres)
        temp.sethomepage(movieHomepage)
        temp.setkeywords(movieKeywords)
        temp.setorgLang(movieOrgLang)
        temp.setorgtitle(movieOrgTitle)
        temp.setoverview(movieOverview)
        temp.setpopularity(moviePopularity)
        temp.setproductionCompanies(movieProductionCompany)
        temp.setproductionCountries(movieProductionCountries)
        temp.setrevenue(movieRevenue)
        temp.setruntime(movieRuntime)
        temp.setspokenLanguages(movieSpokenLang)
        temp.settagline(movieTagline)
        temp.setvoteAverage(movieVoteAv)
        temp.setvoteCount(movieVoteCount)
        
        mList.append(temp)

        if( movieVoteAv != ""):
            #update the incremental analytics
            incremental = globals()['incrementalProduction']
            key = ''
            if( incremental ):
                key = list( incremental.keys() )[0]
            
            if( key and key.upper() in request.form["movieProductionCompany"].upper() ):
                print( u"\u001b[31m key matches enough with the production company \u001b[0m" )
                #update the incremental thingy
                for k, v in incremental[key].items():
                    if float( temp.voteAverage ) > float(incremental[key][k].get("voteAverage")):
                        print( 'Added movie')
                        incremental[key][temp.id] = temp.toJSON()
                        break

                sortList = []            
                for k,v in incremental[key].items():
                    sortList.append( v )

                sortList = sorted(sortList, key=lambda x: x.get("voteAverage"), reverse=True)
                #print( json.dumps( sortList ) )
                orderedMap = OrderedDict()
                for x in sortList:
                    #keep the limit only at 25 stop once we reach this
                    if( len( orderedMap ) == 25 ):
                        break
                    orderedMap[ x['id'] ] = x
                incremental[key] = orderedMap
                #to limit a dict to 25 have to convert to a list. slice the list to 5 items, re dict it for ease to read in the tmeplate file
                # incremental[key] = dict( list( incremental[key].items() )[0:25] )
                globals()['incrementalProduction'] = incremental
        
        
        #profit table one here YAY <(-_-<)
        if(movieBudget != "" and movieRevenue != ""):
            incremental = globals()['incrementalProfit']
            key = ''
            if( incremental ):
                key = list( incremental.keys() )[0]

            if (key and key.upper() in request.form["movieProductionCompany"].upper() ):
                print( u"\u001b[31m key matches enough with the production company \u001b[0m" )
                for k, v in incremental[key].items():
                    if (float(temp.revenue) - float(temp.budget)) > incremental[key][k].get("profit"):
                        print( 'Added movie')
                        incremental[key][temp.id] = temp.toJSON()
                        incremental[key][temp.id]['profit'] = float(temp.revenue) - float(temp.budget)
                        incremental[key][temp.id]['jsprofit'] = incremental[key][temp.id]['profit']
                        break               
                #to limit a dict to 25 have to convert to a list. slice the list to 5 items, re dict it for ease to read in the tmeplate file
                sortList = []            
                for k,v in incremental[key].items():
                    sortList.append( v )
                sortList = sorted(sortList, key=lambda x: x.get("profit"), reverse=True)

                orderedMap = OrderedDict()
                for x in sortList:
                    #keep the limit only at 25 stop once we reach this
                    if( len( orderedMap ) == 25 ):
                        break
                    orderedMap[ x['id'] ] = x
                incremental[key] = orderedMap

                # incremental[key] = dict( list( incremental[key].items() )[0:25] )
                globals()['incrementalProfit'] = incremental

    elif request.method == 'GET': 
        return render_template('insertData.html')
    
    return render_template("insertData.html")

#ajax only method
@app.route("/deleteData", methods=["POST", "GET"])
def deleteData():
    idFound = False
    if request.method == 'POST':
        id = request.form["id"] #dont know where the id input is coming from yet
        li = mList.getData()
        for i, x in enumerate( li ):
            if (id == x.id):
                idFound = True
                MList.rm( i )
                break
     
        if not idFound:
            return json.dumps( {'success': False, 'error': 'Movie does not exist'} )#redirect(url_for("content", input="Page Does Not Exist"))
        else:
            return json.dumps( {'success': True, 'msg': 'Movie deleted'} )#redirect(url_for("content", input="Page Does Not Exist"))
    else:
        abort( 404 )
        #return render_template("deleteTemplate.html") #again not sure on the html side
            
@app.route("/movieTable")
def movieTable():
    #this is mutable so dont change it
    DATA = mList.getData()
    res = [];
    for x in range( len( DATA ) ):
        res.append( DATA[x].toJSON() )
        res[x]['budget'] = UtilData.moneyFormat( res[x]['budget'] )
        res[x]['revenue'] = UtilData.moneyFormat( res[x]['revenue'] )
    return render_template('displayTable.html', value=res )

@app.route("/data")
def data():
    data = mList.toJSON()
    return(json.dumps(data))

@app.route("/updateData", methods=['GET', 'POST']) #here too
def updateData():
    if request.method == 'POST':
        id = request.form["id"]
        li = mList.getData()
        for i, x in enumerate( li ):
            if (id == x.id):
                movieName = request.form["movieName"]
                movieStatus = request.form["movieStatus"]
                movieReleaseDate = request.form["movieReleaseDate"]
                movieBudget = request.form["movieBudget"]
                movieGenres = request.form["movieGenres"].split(',')
            
                movieHomepage = request.form["movieHomepage"]
                movieKeywords = request.form["movieKeywords"].split(',')

                movieOrgLang = request.form["movieOrgLang"]
                movieOrgTitle = request.form["movieOrgTitle"]
                movieOverview = request.form["movieOverview"]
                moviePopularity = request.form["moviePopularity"]
                movieProductionCompany = request.form["movieProductionCompany"].split(',')

                movieProductionCountries = request.form["movieProductionCountries"].split(',')

                movieRevenue = request.form["movieRevenue"]
                movieRuntime = request.form["movieRuntime"]
                movieSpokenLang = request.form["movieSpokenLang"].split(',')

                movieTagline = request.form["movieTagline"]
                movieVoteAv = request.form["movieVoteAv"]
                movieVoteCount = request.form["movieVoteCount"]
                
                x.settitle(movieName)
                print(x.gettitle())
                x.setstatus(movieStatus)
                print(x.getstatus())
                x.setreleaseDate(movieReleaseDate)
                print(x.getreleaseDate())
                x.setbudget(movieBudget)
                print(x.getbudget())
                x.setgenres(movieGenres)
                print(x.getgenres())
                x.sethomepage(movieHomepage)
                print(x.gethomepage())
                x.setkeywords(movieKeywords)
                print(x.getkeywords())
                x.setorgLang(movieOrgLang)
                print(x.getorgLang())
                x.setorgtitle(movieOrgTitle)
                print(x.getorgtitle())
                x.setoverview(movieOverview)
                print(x.getoverview())
                x.setpopularity(moviePopularity)
                print(x.getpopularity())
                x.setproductionCompanies(movieProductionCompany)
                print(x.getproductionCompanies())
                x.setproductionCountries(movieProductionCountries)
                print(x.getproductionCountries())
                x.setrevenue(movieRevenue)
                print(x.getrevenue())
                x.setruntime(movieRuntime)
                print(x.getruntime())
                x.setspokenLanguages(movieSpokenLang)
                print(x.getspokenLanguages())
                x.settagline(movieTagline)
                print(x.gettagline())
                x.setvoteAverage(movieVoteAv)
                print(x.getvoteAverage())
                x.setvoteCount(movieVoteCount)
                print(x.getvote_count())
                #because this is static TODO remove all movies_list
                mList.set( i, x )

                if( movieVoteAv != ""):
                    #update the incremental analytics
                   
                    incremental = globals()['incrementalProduction']
                    key = ''
                    if( incremental ):
                        key = list( incremental.keys() )[0]
                    
                    if( key and key.upper() in request.form["movieProductionCompany"].upper() ):
                        print( u"\u001b[31m key matches enough with the production company \u001b[0m" )
                        #update the incremental thingy
                        for k, v in incremental[key].items():
                            if x.id == k or ( float( x.voteAverage ) > float(incremental[key][k].get("voteAverage")) ):
                                print( 'Added movie')
                                incremental[key][x.id] = x.toJSON()
                                print(incremental[key][x.id])
                                break

                        sortList = []            
                        for k,v in incremental[key].items():
                            sortList.append( v )

                        sortList = sorted(sortList, key=lambda x: x.get("voteAverage"), reverse=True)
                        #print( json.dumps( sortList ) )
                        orderedMap = OrderedDict()
                        for i in sortList:
                            #keep the limit only at 25 stop once we reach this
                            if( len( orderedMap ) == 25 ):
                                break
                            orderedMap[ i['id'] ] = i
                        incremental[key] = orderedMap
                        #to limit a dict to 25 have to convert to a list. slice the list to 5 items, re dict it for ease to read in the tmeplate file
                        globals()['incrementalProduction'] = incremental
                         
                
                
                #profit table one here YAY <(-_-<)
                if(movieBudget != "" and movieRevenue != "" ):
                    incremental = globals()['incrementalProfit']
                    key = ''
                    if( incremental ):
                        key = list( incremental.keys() )[0]

                    if (key and key.upper() in request.form["movieProductionCompany"].upper() ):
                        print( u"\u001b[31m key matches enough with the production company \u001b[0m" )
                        for k, v in incremental[key].items():
                            if x.id == k or ( (float(x.budget) - float(x.revenue)) > incremental[key][k].get("profit") ):
                                print( 'Added movie')
                                incremental[key][x.id] = x.toJSON()
                                incremental[key][x.id]['profit'] = float(x.revenue) - float(x.budget)
                                incremental[key][x.id]['jsprofit'] = incremental[key][x.id]['profit']
                                break
                        sortList = []            
                        for k,v in incremental[key].items():
                            sortList.append( v )
                        sortList = sorted(sortList, key=lambda x: x.get("profit"), reverse=True)
                        
                        orderedMap = OrderedDict()
                        for x in sortList:
                            #keep the limit only at 25 stop once we reach this
                            if( len( orderedMap ) == 25 ):
                                break
                            orderedMap[ x['id'] ] = x
                        incremental[key] = orderedMap

                        globals()['incrementalProfit'] = incremental

                return render_template('displayTable.html', value=mList.getData() )

    elif request.method == 'GET':
        id = request.args['id']
        a = mList.getId( id )
        return render_template('updateData.html', value=a)
    #should never be a case
    return abort(404) #render_template("updateData.html", value=movies_list[x])

@app.route("/profitTable")
def profitTable():
    return render_template('profitTable.html')

@app.route("/profitData" , methods=["POST", "GET"])
def profitData():
    startTime = time.time()
    if request.method == "POST":
        productionCompanies = request.form["search-input"]
        li = mList.getData()
        foundL = []
        incremental = globals()['incrementalProfit']
        c = 0

        if( incremental.get(productionCompanies)):
            endTime = time.time()
            print("--- %s seconds ---" % (endTime - startTime))
            jsonOut = json.dumps( incremental.get(productionCompanies) ).replace( "'", "\\'" )
            return render_template("profitTable.html", data=incremental.get(productionCompanies), json=jsonOut )

        #search through all the movies
        for x in range( len( li ) ) :
            #search through this movies production companies
            for ii in li[x].productionCompanies:
                #if the entered text is a close enough match add it to table
                if productionCompanies.upper() in ii.upper():
                    foundL.append( li[x].toJSON() ); #add the movie as a dict to array
                    # if (int(li[x].revenue) - int( li[x].budget)) > 0:
                    foundL[c]['profit'] = int(li[x].revenue) - int( li[x].budget)
                    # else:
                    #     foundL[c]['profit'] = 0
                    foundL[c]['revenue'] = int( foundL[c]['revenue'] )
                    foundL[c]['budget'] = int( foundL[c]['budget'] )
                    c = c + 1
        #sort the data
        newArray= sorted(foundL, key=lambda x: x.get('profit'), reverse=True )
        #map-reduce the data to remove duplicates
        result = {sub['id'] : sub for sub in newArray}
        #format the int to currency

        #to limit a dict to 25 have to convert to a list. slice the list to 5 items, re dict it for ease to read in the tmeplate file
        res = dict( list( result.items() )[0:25] )

        globals()['incrementalProfit'] = { productionCompanies: res}

        for key, v in res.items():
            result[key]['jsprofit'] = result[key]['profit']
            # result[key]['revenue'] = UtilData.moneyFormat( result[key]['revenue'] )
            # result[key]['profit'] = UtilData.moneyFormat( result[key]['profit'] )
            # result[key]['budget'] = UtilData.moneyFormat( result[key]['budget'] )
            result[key].pop( 'overview' )
            result[key].pop( 'tagline' )


        endTime = time.time()
        print("--- %s seconds ---" % (endTime - startTime))
        jsonOut = json.dumps( res ).replace( "'", "\\'" )
        print( jsonOut )
        return render_template("profitTable.html", data=res, json=jsonOut )

#this function is called when url is redirected to content page
@app.route("/<input>/")
def content(input):
    return f"<h1>{input}</h1>"

@app.route('/export')
@app.route('/route/<fname>')
def export(fname=None):
    if( fname == None ):
        fname = "export"
    fname = fname + '.csv'
    h = Headers()
    h.add( 'Conent-Type', 'text/plain')
    h.add( 'Content-Disposition', 'attachment', filename=fname)
    res = mList.exportMovies( 'test.csv')
    return Response( res, 200, h )

def allowedFileTypes(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/import', methods=['GET', 'POST'])
def importdata():
    if request.method == 'POST':
        if 'file' not in request.files:
            msg = 'No file part <br> <a href="/import">import again</a>'
            return render_template('message.html', msg=msg)
            #return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            msg = 'Empty filename <br> <a href="/import">import again</a>'
            return render_template('message.html', msg=msg)
        if file and allowedFileTypes(file.filename):
            filename = secure_filename(file.filename)
            file.save( os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
            mList.clear();
            # movies_list = mList.load( app.config['UPLOAD_FOLDER'] + filename)
            msg = 'Uploaded succesfully'
            return render_template('message.html', msg=msg)
    return render_template('import.html')

@app.route( '/api/<method>/', methods=["POST", "GET"] )
def api( method ):
    print( method )
    return API.call( method )
    return f"methods{method} - {params}"

@app.route( '/movie/<id>')
def movie( id ):
    print( id )
    m = mList.getId( id ).toJSON()
    if( m ):
        m['budget'] = UtilData.moneyFormat(m['budget'])
        m['revenue'] = UtilData.moneyFormat(m['revenue'])
        m['genres'] = ", ".join( m['genres'] )
        m['keywords'] = ", ".join( m['keywords'] )
        m['spokenLanguages'] = ", ".join( m['spokenLanguages'] )
        m['productionCompanies'] = ", ".join( m['productionCompanies'] )
        m['productionCountries'] = ", ".join( m['productionCountries'] )
        m['spokenLanguages'] = ", ".join( m['spokenLanguages'] )
        return render_template( "movie.html", m=m )
    else:
        abort( 404 )

#fed import
@app.route("/test/", methods=['GET', 'POST'])
def test():
    # return json.dumps( movies_list[0].toJSON() );
    # mList = MovieList(); #MovieList object mList
    # movies_list = mList.load("data/shortmovies.csv")
    # print( request.args['id'] )
    # return request.args['id']
    

    # csv = CSV("data/credits.csv")
    # csv.read();
    # h = Headers();
    # h.add( 'Conent-Type', 'text/plain')
    # h.add( 'Content-Disposition', 'attachment', filename='data/staff.csv')
    # ud = UtilData( csv.getData() )
    # return Response( ud.makeXrefStaff(), 200, h );

    # csv = CSV("data/data_actors.csv")
    # csv.read();
    # a = ActorList()
    # # a.load( "data/data_actors.csv" )
    # a.load( "data/data_staff.csv" )
    # return a.get(0).toJSONStr();

    m = mList.getData()[0].toJSON()
    print( m['id'] )
    m['budget'] = UtilData.moneyFormat(m['budget'])
    m['revenue'] = UtilData.moneyFormat(m['revenue'])
    m['genres'] = ", ".join( m['genres'] )
    m['keywords'] = ", ".join( m['keywords'] )
    m['spokenLanguages'] = ", ".join( m['spokenLanguages'] )
    m['productionCompanies'] = ", ".join( m['productionCompanies'] )
    m['productionCountries'] = ", ".join( m['productionCountries'] )
    m['spokenLanguages'] = ", ".join( m['spokenLanguages'] )

    # m.budget = '{:20,.2f}'.format( int( m.budget ) )
    return render_template( "movie.html", m=m )
    
# This is so we don't have to keep running python -m flask run everytime we make a change
if __name__ == '__main__':
    app.run(debug=True)
