import os, glob
import sys
import string

bow_doc_col = {}


class BowDocument:
    def __init__(self, doc_ID, dict_):
        self.documentID = doc_ID
        self.dict = dict_

    def getDocId(self):
        return self.documentID

    def getDict(self):
        return self.dict

    def addTerm(self, term):
        term = term.lower()
        if len(term) > 2:
            try:
                self.dict[term] += 1
            except KeyError:
                self.dict[term] = 1

    def getTermFreqMap(self):
        for item in self.dict.keys():
            print(item, ":", self.dict.get(item, 0))


def getAllDocId(): #returns all document ID
    allDocId = ""
    allDocId = ""
    for bdoc in bow_doc_col.items():
        tempA = bdoc[0]
        allDocId = allDocId + " " + bow_doc_col[tempA].getDocId()
    return "This is all the document's ID: " + allDocId


def displayDocInfo(aDocId): #displays terms by calling getTermFreqMap method
    num_term = 0
    for item in bow_doc_col[str(aDocId)].getDict():
        num_term += len(item[1])
    print("Doc", aDocId, "has", num_term, "different terms:")
    bow_doc_col[str(aDocId)].getTermFreqMap()


def parse_doc(inputpath):
    Path = inputpath
    filelist = os.listdir(Path)
    start_end = False
    for i in filelist:
        if i.endswith(".xml"):
            with open(Path + '/' + i, 'r') as f:
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
                                    bow_doc_col[docid].addTerm(xterm)
                                start_end = False

                f.close()
    return (bow_doc_col)


if __name__ == '__main__':

    import sys

    if len(sys.argv) != 2:
        sys.stderr.write("USAGE: %s <coll-file>\n" % sys.argv[0])
        sys.exit()
    x = parse_doc(sys.argv[1])
    for num in x.keys():
        displayDocInfo(num)
