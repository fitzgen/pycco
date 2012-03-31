#!/usr/bin/env python
# encoding: utf-8

import sys
import os

class NoFilesFound(Exception):
    def __str__(self):
        return "No files were found to be processed by pycco"

def get_all_files( path, extension ):
    
    def relative( path ):
        relpath = os.path.relpath( path )
        if relpath == '.': 
            return ''
        else:
            return relpath + "/"

    for path, dirs, files in os.walk( path ):
        for filename in files:
            if filename.endswith( extension ):
                yield "%s%s" %( relative( path ), filename )



from os import path

class Source:    
    def __init__(self, name, start):
        self.name       = name
        self.title      = path.basename( self.name )
        self.dirpath    = path.dirname( self.name ) or '.'
        self.dirname    = path.relpath(self.dirpath, start)
        self.start      = start
    
    def save_path(self):
        return "docs/%s/%s" %( self.dirname, self.title )
    
    def relative_path(self, source):
        html = lambda x: "%s.html" %path.splitext(x)[0]
        rel  = path.relpath( source.dirpath, self.dirpath )
        return "%s/%s" %( rel, html(source.title) )  

    def relative_paths(self, sources):
        root_ = ''; list_ = []; dict_ = {}; id_ = 1 
        title    = lambda s: { 'title': s.title, 'url': self.relative_path( s ) }
        new_dict = lambda s: { 'id': id_, 'dirname': s.dirname, 'display': 'none', 'titles': [ title( s ) ], }

        for source in sources:
            if source.dirpath != root_:
                if dict_: 
                    list_.append( dict_ )
                root_  = source.dirpath
                dict_  = new_dict( source )
                id_   += 1
            else:
                dict_[ 'titles' ].append( title( source ) )
        
        list_.append( dict_ )
        if len( list_ ) == 1:
            list_[0]['display'] = 'block'
        return list_   


class Sources:
    def __init__(self, sources, start):
        self.list = [ Source( name, start ) for name in sources ]
        self.get  = lambda x: self.list[ index ]

    def names(self):
        return [i.name for i in self.list]

    def __iter__(self):
        for i in self.list:
            yield i



