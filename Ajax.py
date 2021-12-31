import json, math
from re import L

class Ajax:
    def __init__(self):
        self.__data = None
        self.__pagination = None
        self.__success = None
        self.__msg = None

    def data( self, data ):
        self.__data = data
        return self

    def success( self, success ):
        self.__success = success
        return self

    def pagination( self, pagination ):
        self.__pagination = pagination
        return self

    def makePagination( self, limit, page = 0, count = 0 ):
        o = { 'limit' : limit, 'page': page, 'count': count}
        o['pages'] = math.ceil( count / limit )
        self.__pagination = o
        return self

    def msg( self, msg ):
        self.__msg = msg
        return self

    def toAjax( self ):
        o = {}
        if( self.__data is not None ): 
            o['payload'] = self.__data
        if( self.__msg is not None ): 
            o['msg'] = self.__msg
        if( self.__pagination is not None ): 
            o['pagination'] = self.__pagination
        if( self.__success is not None ): 
            o['success'] = self.__success
        
        return json.dumps( o )