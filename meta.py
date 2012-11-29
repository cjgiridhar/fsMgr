import os

class MetaData(object):
    def __new__(self, path):
        x=0; y=0;
        for root, dirs, files in os.walk(path):
                for f in files:
                        x += 1
        for root, dirs, files in os.walk(path):
                for d in dirs:
                        y += 1
	return (x,y)
