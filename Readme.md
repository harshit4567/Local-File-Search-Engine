# Local file search engine
This is an basic implementation of a file search engine based on python to answer queries in text files on a local system . We have used  "[tf-idf term weighting" and "cosine similarity](https://www.ir-facility.org/scoring-and-ranking-techniques-tf-idf-term-weighting-and-cosine-similarity)" to rank the relevance of the matching documents . tf-idf computations are precomputed making searching a lot faster . Also to speed up searching Stemming (Porter Stemmer) has been used . A basic User Interface using Python's [Tkinter](https://docs.python.org/2/library/tkinter.html)  library is provided . 



![File search](https://d2mxuefqeaa7sj.cloudfront.net/s_1D41B02FD370E9421BC547A10B33599B65FB1E999AD0406AEADC255FC807DBAD_1531307881991_file_search.png)



# Features 
- Since Vector representation is used to calculate the similarity between two documents , the methods supports **single word queries** as well as **multi-word queries** 
- **Phrase query** or exact match is also there . For example “Search engine” when type in quotes will show results for the exact match rather than combining the matches of “search” and “engine”


## **How to run ?**


    python2 createIndex_tfidf.py stopwords.dat testIndex.dat titleIndex.dat


> createIndex_tfidf.py will run only once to calculate the tdf-idf values over the corpus


    python2 queryIndex_tfidf.py stopwords.dat testIndex.dat titleIndex.dat



## **Create Index** **Script (createIndex_tfidf.py)**

 Overall three different files are created in this step : 

- titleIndex.dat
    
  This file stores the unique docId(document id) which is assigned to each document in the corpus.


-  testIndex.dat


  In this an index file is created (also known as inverted index data structure) which contains information about all the unique terms (except stopwords) appearing in all the documents.Each document is given a unique id starting from 0 as stored in the titleIndex.dat.
  The information about a term is stored in the index file as follows:
  term|docID0:pos1,pos2;docID1:pos3,pos4,pos5;…..|tf0,tf1,tf2...|idf
  Here tf0,tf1,tf2 represents term frequency of term in docID0,docID1,docID2 respectively. idf represent Inverse Document Frequency and pos1 respresents the position of the term in the respective document and so on .
## 
- lines.dat 


  This file stores the information about the lines in which the term is present in various documents.
  This line information is represented as :
  term|docID0:line1,line2;docID1:line3,line4,line5
  
  Before creation of these files, all the terms of the documents are checked in the stopwords list.If a term appears in stopwords then it is skipped else it's information is stored in these above files.
  Also, each term is stemmed by Porter Stemmer before being added to the index.


## Query Index Script(queryIndex_tfidf.py)

In this , first of all , all the informations from the files lines.dat,titleIndex.dat and  testIndex.dat is again stored back using dictionary in Python.

Now, the different types of Queries supported are :

- One Word Queries(OWQ)
  This is a single term query and its output is list of documents containing the asked term along with the line numbers where the term is present in the respective document.


- Multi Word Queries(MWQ)
  The input in MWQ is a sequence of words, and the output is the list of documents that contain any of the query terms along with the line numbers.


- Phrase Queries(PQ)
  The input in PQ is again a sequence of words, and the matching documents are the ones that contain all query terms in the specified order.
# Ranking of Documents

Now that we have have found the list of documents in which the query is present it is time to rank them. The ranking scheme we have used here is based on tf-idf.
Tf-Idf is a weighting scheme that assigns each term in a document a weight based on its term frequency (tf) and inverse document frequency (idf). The terms with higher weight scores are considered to be more important. It’s one of the most popular weighting schemes in Information Retrieval.

## **Term Frequency(Tf)**

Term frequency(tf) of a term is document specific. It is basically the number of occurrences of the term t in the document D. It is quite logical to choose tf as a parameter because as a term appears more in the document it becomes more important. We can represent a document by a vector whose size is equal to the no. of unique terms in the document and each value denotes the count of the term in the given document. The representation of documents as vectors in a common vector space is known as the vector space model and it’s very fundamental to information retrieval.
But here is one drawback. As the document will grow in size the weight of tf is going to increase as the frequency of terms will increase. So a document which contains same information as other document, copied more than one time will be considered more important. To eradicate this drawback we will divide each value in a vector by its norm so that the vector becomes a unit vector.

![](https://d2mxuefqeaa7sj.cloudfront.net/s_C3D649E71119AF3E639E10374FBC226333CEEB81CCC3B97249117BC1106DDBCD_1531311343198_m1.png)

## **Inverse Document Frequency(Idf)**

We can’t only use term frequencies to calculate the weight of a term in the document, because tf considers all terms equally important. However, some terms occur more rarely and they are more discriminative than others. If we purely use tf as measure to rank then if we search a topic like sound waves, we might end up getting a lot of documents containing light waves and other waves, as the frequency of term is the only parameter.

![](https://d2mxuefqeaa7sj.cloudfront.net/s_C3D649E71119AF3E639E10374FBC226333CEEB81CCC3B97249117BC1106DDBCD_1531311436655_m2.png)


To mitigate this effect, we use inverse document frequency. The document frequency of a term is basically the number of documents containing the term. So the inverse document frequency(idf) of a term is the number of documents in the corpus divided by the document frequency of a term. Generally it has been found that the factor of idf is quite large and better results are obtained if we use log(idf). As log is an increasing function, we can use it without hampering our results.

![](https://d2mxuefqeaa7sj.cloudfront.net/s_C3D649E71119AF3E639E10374FBC226333CEEB81CCC3B97249117BC1106DDBCD_1531311512829_m3.png)

## **Tf-Idf Scoring**

We have defined both tf and idf, and now we can combine these to produce the ultimate score of a term t in document d. We will again represent the document as a vector, with each entry being the tf-idf weight of the corresponding term in the document. The tf-idf weight of a term t in document d is simply the multiplication of its tf by its idf.

![](https://d2mxuefqeaa7sj.cloudfront.net/s_C3D649E71119AF3E639E10374FBC226333CEEB81CCC3B97249117BC1106DDBCD_1531311585260_m4.png)


Now that we have built the vectors of each document based on tf-idf weight. It is time to answer a query with using the given document vectors. First of all we will create a query vector itself on similar basis as we made the document vector i.e based on tf-idf score(considering query a document itself). Now that we have our query vector ready, we will find all those documents in which our query is present. Now we will take the dot product of the query vector and the document vector in which the query is present. The **higher the** **dot** **product more similar is query vector with the document vector** which means the angle between the document vector and query vector is small. This technique of finding similarity between query and document is called cosine similarity.


## **Shortcomings of the project**
- Not scalable when Vocabulary size is too large since the document vectors have dimension = Vocabulary size
- So far only text files are supported 

