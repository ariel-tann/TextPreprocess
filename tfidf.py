import math
import os, glob
import sys
import string
from porter2stemmer import Porter2Stemmer

bow_doc_col = {}
DF = {}
TFIDF = {}


class BowDocument:
    def __init__(self, doc_ID, dict_):
        self.documentID = doc_ID
        self.dict = dict_
        self.wordCount = 0
        self.tfDict = {}
        self.idfDict = {}
        self.tfidfDict = {}

    def getDocId(self):
        return self.documentID

    def getDict(self):
        return self.dict

    def getTFDict(self):
        return self.tfDict

    def getWordCount(self):
        return self.wordCount

    def addTerm(self, term): #add term to dictionary (self.dict)
        term = Porter2Stemmer().stem(term.lower())  # Q1b
        if len(term) > 2 and term not in stopWordsList:  # Q1b
            try:
                self.dict[term] += 1
            except KeyError:
                self.dict[term] = 1

    def getTermFreqMap(self): #sort and print out dictionary values
        sortedList = sorted(self.dict.items(), key=lambda x: x[1])  # Q1c
        for elem in sortedList:
            print(elem[0], ":", elem[1])

    def computeTF(self, docid): #calculate TF value for Bow Document (only body)
        for item in bow_doc_col[docid].dict.keys():
            self.tfDict[item] = (bow_doc_col[docid].dict.get(item, 0) / float(self.wordCount))

    def computeIDF(self): #calculate IDF value (only body)
        N = len(bow_doc_col)
        for item in DF.keys():
            self.idfDict[item] = math.log10(N / float(DF.get(item, 0)) + 1)

    def computeTFIDF(self): #calculate TFIDF value (only body)
        for item in self.tfDict.keys():
            self.tfidfDict[item] = self.tfDict.get(item, 0) * self.idfDict.get(item, 0)
        return self.tfidfDict


def calculateTfIdf():
    for items in bow_doc_col.keys():
        bow_doc_col[items].computeIDF()
        TFIDF[items] = bow_doc_col[items].computeTFIDF() #generate term:tfidf dict for each doc and fill al dictionary of docID: term:tfidf

    for item in TFIDF.items(): #print out top 20 terms
        print("-------Document", item[0], "contains", len(item[1]), "terms-------")
        temp = item[1]
        if len(item[1]) > 20:
            sortedList = sorted(temp.items(), reverse=True, key=lambda x: x[1])  # Q1c
            for elem in sortedList [:20]:
                print(elem[0], ":", elem[1])

        else:
            sortedList = sorted(temp.items(), reverse=True, key=lambda x: x[1])  # Q1c
            for elem in sortedList:
                print(elem[0], ":", elem[1])


def addDFTerm(term, docid):
    term = Porter2Stemmer().stem(term.lower())  # Q1b
    if len(term) > 2 and term not in stopWordsList:  # Q1b
        try:
            DF[term].add(docid)
        except KeyError:
            DF[term] = {docid}


def parse_doc(inputpath, stop_wds): #returns dictionary collection of BowDoc {docid: BowDoc}
    Path = inputpath
    filelist = os.listdir(Path)
    start_end = False
    for i in filelist:
        if i.endswith(".xml"):
            with open(Path + '/' + i, 'r') as f:
                word_count = 0
                myfile = f.readlines()
                # print(f)
                for line in myfile:
                    line = line.strip()
                    if line.startswith("<newsitem") | line.startswith("<p>"):
                        if (start_end == False):
                            if line.startswith("<newsitem "):
                                for part in line.split():
                                    if part.startswith("itemid="):
                                        docid = part.split("=")[1].split("\"")[1]
                                        bow_doc_col[docid] = BowDocument(docid, {})
                                        break
                                if line.startswith("<text>"):
                                    start_end = True
                            elif line.startswith("</text>"):
                                break
                            else:
                                line = line.replace("<p>", "").replace("</p>", "").replace("quot", "")
                                line = line.translate(str.maketrans('', '', string.digits)).translate(
                                    str.maketrans(string.punctuation, ' ' * len(string.punctuation)))
                                line = line.replace("\\s+", " ")
                                for xterm in line.split():
                                    word_count += 1
                                    bow_doc_col[docid].addTerm(xterm)
                                    addDFTerm(xterm, docid)  # Q2a
                                bow_doc_col[docid].wordCount = word_count
                                bow_doc_col[docid].computeTF(docid) #Q2b
                                start_end = False

                f.close()
    return (bow_doc_col)


if __name__ == '__main__':

    import sys

    if len(sys.argv) != 2:
        sys.stderr.write("USAGE: %s <coll-file>\n" % sys.argv[0])
        sys.exit()

    stopwords_f = open('common-english-words.txt', 'r')
    stopWordsList = stopwords_f.read().split(',')
    stopwords_f.close()

    x = parse_doc(sys.argv[1], stopWordsList)

    for i in DF: #changing the value of DF dict from dict to int freq value
        DF[i] = len(DF[i])

    calculateTfIdf()

