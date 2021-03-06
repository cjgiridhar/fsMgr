import tornado.ioloop
import tornado.web
import tornado.escape
import subprocess,os
from stat import *
import time
from tornado.options import define, options
from searching import Searched
from meta import MetaData
import urlparse
import datetime

fsMgr = "/home/ubuntu/fsMgr/"
define("port", default="8888")
define("image_url", default=r"/home/ubuntu/fsMgr/images/(.*)")
define("image_path", default=fsMgr + r"/images/")
define("css_url", default=r"/home/ubuntu/fsMgr/css/(style.\css)")
define("css_path", default=fsMgr + r"/css")
define("root_url",default=r"/root/(.*)")
define("__ROOT__", default=r"root/")
define("index", default=r"./index")

class Search(tornado.web.RequestHandler):

    def initialize(self):
	self.q = None

    def get(self):
	self.clear()
        self.q = self.get_argument('q')
	srch = Searched(options.index,options.__ROOT__,self.q)
	#srch.indexer()
	results = srch.searcher()
	runtime = results.runtime
	occurences = len(results)
	title = []; url = []
	for index in range(10):
		url.append(results[index]["url"])

	self.render('templates/search.html', q=self.q, runtime=runtime, occurences=occurences, url=url)


class Highlighted(tornado.web.RequestHandler):

    def get(self):
	self.clear()
        self.q = self.get_argument('q')
        srch = Searched(options.index,options.__ROOT__,self.q)
	url, content = srch.highlighted()
	self.render('templates/highlighted.html', url=url, content=content)

class AdvSearch(tornado.web.RequestHandler):
    def get(self):
	self.render('templates/advsearchform.html')
	
class MoreLikeThis(tornado.web.RequestHandler):

    def get(self):
	docpath = self.get_argument('docpath')
	srch = Searched(options.index,options.__ROOT__)
	like_url = srch.morelikethis(docpath)
 	self.render('templates/morelikethis.html',  docpath=docpath, like_url=like_url)

class DidYouMean(tornado.web.RequestHandler):

    def get(self):
        from whoosh import qparser
        qstring = self.get_argument('qstring')
        print qstring
        srch = Searched(options.index,options.__ROOT__)
        hits = srch.didyoumean(qstring)
        self.render('templates/didyoumean.html', hits=hits, qstring=qstring)

class FS(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, arg):
	self.root = options.__ROOT__
	if not arg:
		arg = self.root
		self.path = self.root
	else:
		self.path = self.root + str(arg)
	if os.path.isfile(self.path):
		f = open(self.path, 'r')
		self.write(tornado.escape.xhtml_escape(f.read()))
		f.close()
		self.finish()
	else:
		items = os.listdir(self.path)
        	self._async_callback(items)
    
    def _async_callback(self, items):
	fs = {}
	count = 0; size=0
	for f in items:
		fs[count] = []
		mode = os.stat(self.path + f).st_mode
		if S_ISDIR(mode):
        		mode = 'dir'
			url = "http://localhost:8888/" + self.path + f + "/"
		else:
			mode = 'file'
			url = "http://localhost:8888/" + self.path + f
		size = os.stat(self.path + f)[6]
		mtime = time.ctime(os.path.getmtime(self.path + f))
		fs[count]=[f, mode, size, mtime, url]
		count += 1
        self.render('templates/fsMgr.html',dict=fs)

class Meta(tornado.web.RequestHandler):
    def get(self):
	x,y = MetaData(options.__ROOT__)
	root = options.__ROOT__
	metadata = {
		"files":x,
		"directories":y,
		"root":root
	}
	self.write(tornado.escape.json_encode(metadata))


application = tornado.web.Application([
    (options.root_url, FS),
    (options.image_url,tornado.web.StaticFileHandler, {"path": options.image_path},),
    (options.css_url,tornado.web.StaticFileHandler, {"path": options.css_path},),
    (r"/meta", Meta),
    (r"/search", Search),
    (r"/advsearch", AdvSearch),
    (r"/advsearch/morelikethis", MoreLikeThis),
    (r"/advsearch/didyoumean", DidYouMean),
    (r"/advsearch/highlighted", Highlighted),
    
],debug=True)

if __name__ == "__main__":
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
