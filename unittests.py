from searching import *
import unittest

class fsMgr(unittest.TestCase):
	"""
	Test of indexing capabilities of fsMgr searching class
		root - tree structure that needs to be index
		index - where the index should get created
		q - search keyword
	"""
	def setUp(self):
		self.index = "/home/ubuntu/index"
		self.root = "/home/ubuntu/fsMgr/root/"
		self.srch = None

        def test_indexing(self):
		self.srch = Searched(self.index,self.root,None)
	        self.srch.indexer()

	def test_searching(self):
		self.srch = Searched(self.index,self.root,'python')
                self.srch.indexer()
		results = self.srch.searcher()

        def test_didyoumean(self):
		self.srch = Searched(self.index,self.root)
		self.srch.indexer()
		r=self.srch.didyoumean('piethon')
		self.assertTrue('python' in r)

	def tearDown(self):
		self.index = None
		self.root = None
		self.srch = None


if __name__ == '__main__':
    unittest.main()
