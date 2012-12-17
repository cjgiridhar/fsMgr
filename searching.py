import whoosh, sys
import whoosh.fields
import whoosh.index
import whoosh.qparser
from whoosh.fields import Schema, ID, TEXT, STORED
import os
from whoosh import analysis, fields, formats, query, highlight
import datetime

sys.path[0:0] = '/home/ubuntu/Desktop/Whoosh-2.4.1/src/whoosh'

class SearchEngine(object):
    ana = analysis.StandardAnalyzer()
    schema = whoosh.fields.Schema(
        url=whoosh.fields.ID(unique=True, stored=True),
        title=whoosh.fields.TEXT(stored=True, phrase=False),
        content=whoosh.fields.TEXT(spelling=True, stored=True, phrase=False), 
        modtime=whoosh.fields.ID())

    def __init__(self, index_path):
        self.path = index_path
        if not os.path.exists(index_path):
            os.makedirs(index_path)

    def create_index(self):
        whoosh.index.create_in(self.path, self.schema)
	self.open_index()

    def open_index(self):
        self._index = whoosh.index.open_dir(self.path)
        self._writer = self._index.writer()
	return self._index

    def add_document(self, url, title, content,modtime):
        self._writer.add_document(
            url=unicode(url),
            title=unicode(title),
            content=unicode(content,errors='ignore'),
	    modtime =unicode(modtime),)

    def update_document(self, url, title, content,modtime):
        self._writer.update_document(
            url=unicode(url),
            title=unicode(title),
            content=unicode(content),
	    modtime = unicode(modtime),)

    def delete_document(self, url):
        self._index.delete_by_term('url', unicode(url))

    _queryparser = whoosh.qparser.QueryParser('content', schema=schema)
    def find(self):
        searcher = self._index.searcher()
	return searcher,self._queryparser

    def commit(self):
        self._writer.commit()

    def cancel(self):
        self._writer.cancel()

class Searched(object):
    def __init__(self, indexpath, dirpath, q=None):
	self.indexpath = indexpath
	self.dirpath = dirpath 
	self.q = q

    def indexer(self):
        engine = SearchEngine(self.indexpath)
        engine.create_index()
        for root, dirs, files in os.walk(self.dirpath):
                if len(files) is not 0:
                        for f in files:
                                path = os.path.join(root,f)
                                url = "http://localhost:8888/" + path
                                modtime = os.path.getmtime(path)
                                fh = open(path, 'r')
                                contents = fh.read()
                                fh.close()
                                print "Adding file: %s" %f
                                engine.add_document(url, path, contents, modtime)
	print "Commiting index..."
        engine.commit()
	print "Index Commited"

    def searcher(self):
        engine = SearchEngine(self.indexpath)
       	engine.open_index()
	searcher, _queryparser = engine.find()
	results = searcher.search(query.Term('content', self.q), limit=10)
	#docnum = searcher.document_number(url='http://localhost:8888/root/style.css')
	return results

    def highlighted(self):
        engine = SearchEngine(self.indexpath)
        engine.open_index()
        searcher, _queryparser = engine.find()
        results = searcher.search(query.Term('content', self.q), limit=10)
        url = []; content = []
        for hit in results:
                url.append(hit["url"])
                content.append(hit.highlights("content"))
	return (url, content)

    def morelikethis(self, path):
	engine = SearchEngine(self.indexpath)
	engine.open_index()
	searcher, _queryparser = engine.find()
	url = "http://localhost:8888/" + path
	docnum = searcher.document_number(url=url)
	r = searcher.more_like(docnum, 'content')
	like_url = []
        for hit in r:
                like_url.append(hit["url"])
	return like_url

    def didyoumean(self, qstring):
        engine = SearchEngine(self.indexpath)
        engine.open_index()
        searcher, _queryparser = engine.find()
	corrector = searcher.corrector("content")
	r = corrector.suggest(qstring, limit=3)
        hits = []
        for h in r:
                hits.append(h)
	return hits
