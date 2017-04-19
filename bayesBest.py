# Name: Chankyu Oh, Akshat Palnitikar, Shrivant Bhartia sbf324
# Date: 5/19/16
# Description: All group members were present and contributing during all work on this project
#
#

import math, os, pickle, re , os.path


class Bayes_Classifier:
    def __init__(self):
        """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a
        cache of a trained classifier has been stored, it loads this cache.  Otherwise,
        the system will proceed through training.  After running this method, the classifier
        is ready to classify input text."""
        self.posD = {}
        self.negD = {}

        if os.path.isfile("posReviewsBest.bat") and os.path.isfile("negReviewsBest.bat"):
            #  if the dictionaries have already been made, load them
            self.posD = self.load("posReviewsBest.bat")
            self.negD = self.load("negReviewsBest.bat")
        else:
            self.train()


    def frequencyCalc1(self, tokenSumm, dictType):
        """Calculates frequencies of unigram's and adds to respective dictionary"""

        if dictType == "positive":
            for token in tokenSumm:
                if self.posD.get(token, False) == False:  # if it's first time token in dictionary
                    self.posD[token] = 1
                else:
                    self.posD[token] += 1
        elif dictType == "negative":
            for token in tokenSumm:
                if self.negD.get(token, False) == False:  # if it's first time token in dictionary
                    self.negD[token] = 1
                else:
                    self.negD[token] += 1

    def frequencyCalc2(self,tokenSumm, dictType):
        """calculates frequencies of bigrams (double words) and adds it to respective dictionary"""
        for x in range(len(tokenSumm)):
            if x != len(tokenSumm) - 1:
                w1 = tokenSumm[x]
                w2 = tokenSumm[x + 1]
                token = w1 + "_" + w2  # i represented the key for bigrams as the two words attached by "_"
                if dictType == "positive":
                    if self.posD.get(token, False) == False:
                        self.posD[token] = 1
                    else:
                        self.posD[token] += 1
                elif dictType == "negative":
                    if self.negD.get(token, False) == False:
                        self.negD[token] = 1
                    else:
                        self.negD[token] += 1


    def train(self):
        """Trains the Naive Bayes Sentiment Classifier."""
        lFileList = []
        for fFileObj in os.walk("movies_reviews/"):
            lFileList = fFileObj[2]
            break
        for movie in lFileList:
            if "movies-5" in movie:
                movieLocation = "movies_reviews/" + movie
                summary = self.loadFile(movieLocation)
                tokenSumm = self.tokenize(summary)
                self.frequencyCalc1(tokenSumm,"positive")
                self.frequencyCalc2(tokenSumm,"positive")
            elif "movies-1" in movie:
                movieLocation = "movies_reviews/" + movie
                summary = self.loadFile(movieLocation)
                tokenSumm = self.tokenize(summary)
                self.frequencyCalc1(tokenSumm,"negative")
                self.frequencyCalc2(tokenSumm,"negative")

        self.save(self.posD,"posReviewsBest.bat")
        self.save(self.negD,"negReviewsBest.bat")

    def classify(self, sText):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """

        posFinalProb = 0
        negFinalProb = 0




        totalFreq = float(sum(self.posD.itervalues())) + float(len(self.posD))
        negTotalFreq = float(sum(self.negD.itervalues())) + float(len(self.negD))
        #  sum(posD.itervalues) sums the values of every key, which represents the sum of frequencies of every word
        # add the length of the dictionary b/c of smooth add one process


        sTextList = self.tokenize(sText)# makes string into list of each WORDS, so we iterate words, not chars

        for x in range(len(sTextList)): # iterate through every word
            if x != len(sTextList) - 1: # protects against index error in the case we are at last element
                word1 = sTextList[x]
                word2 = sTextList[x + 1]
                bigram = word1 + "_" + word2

                if bigram in self.posD:  # if the bigram was found in the positive dictionary

                    frequency = float(self.posD.get(bigram)) + float(1)  # add one for add-one smoothing
                    posFrac = frequency / totalFreq
                    posFinalProb += math.log(posFrac)

                    if bigram not in self.negD:  # add-one smoothing, if word in posD but not negD,
                        #  imagine that the word existed in negD but with frequency one
                        negFrequency = float(1)
                        negFrac = negFrequency / negTotalFreq
                        negFinalProb += math.log(negFrac)



                if bigram in self.negD:


                    negFrequency = float(self.negD.get(bigram)) + float(1)  # add-one smoothing

                    negFinalProb += math.log(negFrequency / negTotalFreq)

                    if bigram not in self.posD:
                        # if word is in negD but not posD, imagine that the word did occur, but just once in posD
                        frequency = float(1)
                        posFinalProb += math.log(frequency / totalFreq)



            unigram = sTextList[x]


            if unigram in self.posD:

                frequency = float(self.posD.get(unigram)) + float(1)
                posFrac = frequency / totalFreq
                posFinalProb += math.log(posFrac)


                if unigram not in self.negD:  # add-one smoothing process
                    negFrequency = float(1)
                    negFrac = negFrequency / negTotalFreq
                    negFinalProb += math.log(negFrac)



            if unigram in self.negD:

                negFrequency = float(self.negD.get(unigram)) + float(1)

                negFinalProb += math.log(negFrequency /negTotalFreq)


                if unigram not in self.posD:
                    frequency = float(1)
                    posFinalProb += math.log(frequency / totalFreq)



        if abs(posFinalProb - negFinalProb) <= .2:  # if values are not too diff. just classify as neutral

            return "neutral"


        elif posFinalProb > negFinalProb:

            return "positive"

        elif posFinalProb < negFinalProb:


            return "negative"







    def loadFile(self, sFilename):
        """Given a file name, return the contents of the file as a string."""

        f = open(sFilename, "r")
        sTxt = f.read()
        f.close()
        return sTxt

    def save(self, dObj, sFilename):
        """Given an object and a file name, write the object to the file using pickle."""

        f = open(sFilename, "w")
        p = pickle.Pickler(f)
        p.dump(dObj)
        f.close()

    def load(self, sFilename):
        """Given a file name, load and return the object stored in the file."""

        f = open(sFilename, "r")
        u = pickle.Unpickler(f)
        dObj = u.load()
        f.close()
        return dObj

    def tokenize(self, sText):
        """Given a string of text sText, returns a list of the individual tokens that
        occur in that string (in order)."""

        lTokens = []
        sToken = ""
        for c in sText:
            if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
                sToken += c
            else:
                if sToken != "":
                    lTokens.append(sToken)
                    sToken = ""
                if c.strip() != "":
                    lTokens.append(str(c.strip()))

        if sToken != "":
            lTokens.append(sToken)

        return lTokens


a = Bayes_Classifier()
#b = "movies-5-8843.txt"
#texter =  "movies_reviews/" + b
#txt = a.loadFile(texter)
#print(txt)
#print a.tokenize(txt)


#print a.posD

#print "negative reviews: ", a.negD

print a.classify("not good")
#a.train()


#print a.posD

#print a.negD
