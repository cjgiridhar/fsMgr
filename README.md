fsMgr
=====

FileSystem Search Manager (fsMgr) is implemented with Tornado and Whoosh.

fsMgr is developed to introduce and demonstrate the concepts of 
- 'Abstraction in Search' for mid-scaled real time website
- SVC (Search View Controller) design based on MVC pattern

More about 'Abstraction in Search' can be read @ http://technobeans.wordpress.com/2012/10/03/abstraction-in-search/

fsMgr was developed on Linux ubuntu 2.6.32-38-generic #83-Ubuntu and Python 2.6

Features
========
Search facilities exported:

- Highlighted
--	Highlights the searched keywords

- Did you mean
--	Spell check for searched keywords
 
- More like this
--	Document based search

Usage
=====
Assuming your home directory points to /home/ubuntu

- Create a directory fsMgr under /home/ubuntu
- Copy the project contents under fsMgr
- Browse to /home/ubuntu/fsMgr at the terminal
- Run fsMgr as 'python fsMgr.py'

Dependencies
============
- Python 2.6
- Tornado 2.2
- Whoosh 2.4.1

Opportunities
=============
By adding a class in search.py, you could leverage more search engines under fsMgr.

Abstraction to the new search engine can be implemented in fsMgr.py.

Contact
=======

Chetan Giridhar , cjgiridhar@gmail.com

License
=======
GNU General Public License v3.0

Copyright (c) Chetan Giridhar, http://technobeans.com
