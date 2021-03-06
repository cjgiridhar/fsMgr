fsMgr - FileSystem Search Manager
==================================

fsMgr is prototype developed to introduce and demonstrate the concepts of: 
- 'Abstraction in Search' for mid-scaled real time website
- SVC (Search View Controller) design based on MVC architecture

More about 'Abstraction in Search' and 'SVC Architecture' [here](http://technobeans.wordpress.com/2012/10/03/abstraction-in-search/)

fsMgr is implemented with Tornado & Whoosh Python libraries on Linux ubuntu 2.6.32-38-generic

Features
========
Search facilities exported:

- Highlighted

	Highlights the searched keywords

- Did you mean

	Spell check for searched keywords
 
- More like this

	Document based search

Documentation
=============
fsMgr is implemented with fsMgr.py, searching.py and meta.py modules
Refer the documentation of these classes [here](http://cjgiridhar.github.com/fsMgr/overview.html)

Setup
=====

- git clone https://github.com/cjgiridhar/fsMgr.git
- copy the folder [that needs to be indexed/searched] under fsMgr/root


Usage
=====
- Login to /home/ubuntu/fsMgr at the terminal
- Run fsMgr as 'python fsMgr.py'
- Browse to http://localhost:8888/root/ & start searching

Note: Indexing happens on the tree under root/ when you search for a keyword. Time taken for indexing depends on size of root/
If you want reindexing everytime you search, one needs to uncomment the indexer for preparing the index. fsMgr.py --> srch.indexer, else keep the indexer commented

start searching at super sonic speed! :)

Dependencies
============
- Python 2.6
- Tornado 2.2
- Whoosh 2.4.1

Installing Dependencies
=======================
sudo pip install tornado==2.2
sudo pip install Whoosh==2.4.1

Opportunities
=============

- By adding a class in searching.py, you could leverage more search engines under fsMgr.
- Abstraction to the new search engine can be implemented in fsMgr.py. For instance, pyLucene can be implemenetd in searching.py and exposed to fsMgr.py.


Known Issues
============
- File contents cant be viewed if the file name contains white-spaces
- Robust error handling is not taken care of as its a prototype implementation

Contact
=======

Chetan Giridhar , cjgiridhar@gmail.com

License
=======
GNU General Public License v3.0

Copyright (c) Chetan Giridhar, [technobeans](http://technobeans.com)
