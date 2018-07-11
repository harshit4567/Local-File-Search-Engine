#!/usr/bin/env python
import sys
import re
import os
from porterStemmer import PorterStemmer
from collections import defaultdict
from array import array
import gc
import math

porter=PorterStemmer()

class CreateIndex:

    def __init__(self):
        self.index=defaultdict(list)    #the inverted index
        self.titleIndex={}
        self.tf=defaultdict(list)          #term frequencies of terms in documents
        self.ldict = {}                                        #documents in the same order as in the main index
        self.df=defaultdict(int)         #document frequencies of terms in the corpus
        self.numDocuments=0

    
    def getStopwords(self):
        '''get stopwords from the stopwords file'''
        f=open(self.stopwordsFile, 'r')
        stopwords=[line.rstrip() for line in f]
        self.sw=dict.fromkeys(stopwords)
        f.close()
        

    def getTerms(self, line):
        '''given a stream of text, get the terms from the text'''
        line=line.lower()
        line=re.sub(r'[^a-z0-9 ]',' ',line) #put spaces instead of non-alphanumeric characters
        line=line.split()
        line=[x for x in line if x not in self.sw]  #eliminate the stopwords
        line=[ porter.stem(word, 0, len(word)-1) for word in line]
        return line


    def writelines(self):
        f = open("lines.dat",'w')
        for term,postings in self.ldict.iteritems():
            f.write('%s|'%(term))

            for j in range(0,len(postings)):
                f.write('%s:'%(postings[j][0]))
                for k in range(0,len(postings[j][1])):
                    f.write('%d'%(postings[j][1][k]))
                    if k!= len(postings[j][1])-1:
                        f.write(',')
                if j!= len(postings)-1:
                    f.write(';')
            f.write('\n')


    def writeIndexToFile(self):
        '''write the index to the file'''
        #write main inverted index
        f=open(self.indexFile, 'w')
        #first line is the number of documents
        print >>f, self.numDocuments
        self.numDocuments=float(self.numDocuments)
        for term in self.index.iterkeys():
            postinglist=[]
            for p in self.index[term]:
                docID=p[0]
                positions=p[1]
                postinglist.append(':'.join([str(docID) ,','.join(map(str,positions))]))
            #print data
            postingData=';'.join(postinglist)
            tfData=','.join(map(str,self.tf[term]))
            idfData='%.4f' % (self.numDocuments/self.df[term])
            print >> f, '|'.join((term, postingData, tfData, idfData))
        f.close()
        
        #write title index
        f=open(self.titleIndexFile,'w')
        for pageid, title in self.titleIndex.iteritems():
            print >> f, pageid, title
        f.close()
        

    def getParams(self):
        '''get the parameters stopwords file, collection file, and the output index file'''
        param=sys.argv
        self.stopwordsFile=param[1]
        self.indexFile=param[2]
        self.titleIndexFile=param[3]
        

    def createIndex(self):
        '''main of the program, creates the index'''
        self.getParams()
        self.getStopwords()
                
        #bug in python garbage collector!
        #appending to list becomes O(N) instead of O(1) as the size grows if gc is enabled.
        gc.disable()
        f1 = open("lines.dat",'w')
        for name,filename in enumerate(os.listdir('corpus')):
            if filename.endswith(".txt"):
                print(filename)
                file = open('corpus/' + filename, 'r')
                str = ""
                for line in file:
                    str = str + line
                # print(str)
                file.close()


                pageid = name
                linedict = {}
                ct = 1
                file = open('corpus/' + filename, 'r')

                for line in file:
                        x = line.lower()
                        x = re.sub(r'[^a-z0-9 ]', ' ', x)

                        for word in x.split():
                            if word in self.sw:
                                continue;
                            y = porter.stem(word, 0, len(word) - 1)

                            if y in linedict.keys():
                                linedict[y][1].append(ct)
                            else:
                                linedict[y] = [pageid,array('I',[ct])]
                        ct = ct+1

                #print linedict
                for term, positions in linedict.iteritems():
                        try:
                            self.ldict[term].append(positions)
                        except:
                            self.ldict[term] = [positions]

                terms = self.getTerms(str)
                self.titleIndex[pageid] = filename
                self.numDocuments += 1
                termdictPage = {}
                for position, term in enumerate(terms):
                    try:
                        termdictPage[term][1].append(position)
                    except:
                        termdictPage[term] = [pageid, array('I', [position])]
            
                 #normalize the document vector
                norm=0
                for term, posting in termdictPage.iteritems():
                    norm+=len(posting[1])**2
                    norm=math.sqrt(norm)
            
            #calculate the tf and df weights
                for term, posting in termdictPage.iteritems():
                    self.tf[term].append('%.4f' % (len(posting[1])/norm))
                    self.df[term]+=1
            
            #merge the current page index with the main index
                for termPage, postingPage in termdictPage.iteritems():
                    self.index[termPage].append(postingPage)
            
            else :
                continue
        gc.enable()
        self.writelines()
        self.writeIndexToFile()
        
    
if __name__=="__main__":
    c=CreateIndex()
    c.createIndex()
    

