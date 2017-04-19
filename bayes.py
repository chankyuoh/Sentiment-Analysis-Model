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

        if os.path.isfile("posReviews.bat") and os.path.isfile("negReviews.bat"):
            #  if the dictionaries have already been made, load them
            self.posD = self.load("posReviews.bat")
            self.negD = self.load("negReviews.bat")
        else:
            self.train()

    def frequencyCalc1(self, tokenSumm, dictType):

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


    def train(self):
        """Trains the Naive Bayes Sentiment Classifier."""
        lFileList = []
        for fFileObj in os.walk("movies_reviews/"):
            lFileList = fFileObj[2]
            break
        for movie in lFileList:
            if "movies-5" in movie: # if the name of the files has 'movies-5' in it
                movieLocation = "movies_reviews/" + movie
                summary = self.loadFile(movieLocation)  # load the string inside that file
                tokenSumm = self.tokenize(summary)  # tokenize it into a list
                self.frequencyCalc1(tokenSumm,"positive") # calculate frequency and add to pos Dictionary
            elif "movies-1" in movie:
                movieLocation = "movies_reviews/" + movie # same as above but for negative
                summary = self.loadFile(movieLocation)
                tokenSumm = self.tokenize(summary)
                self.frequencyCalc1(tokenSumm,"negative")

        self.save(self.posD,"posReviews.bat")  # save the dictionaries
        self.save(self.negD,"negReviews.bat")

    def classify(self, sText):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """


        posFinalProb = 0  # prior probabilities to start with
        negFinalProb = 0


        totalFreq = float(sum(self.posD.itervalues())) + float(len(self.posD))
        negTotalFreq = float(sum(self.negD.itervalues())) + float(len(self.negD))
        # ^ represents summation of the frequencies for every word in the dictionary



        sTextList = self.tokenize(sText) # makes string into list of each WORDS, so we iterate words, not chars

        for word in sTextList:
            if word in self.posD:

                frequency = float(self.posD.get(word)) +1

                posFrac = frequency / totalFreq
                posFinalProb += math.log(posFrac)


                if word not in self.negD:
                    negFrequency = float(1)
                    negFrac = negFrequency/negTotalFreq
                    negFinalProb += math.log(negFrac)




            if word in self.negD:

                negFrequency = float(self.negD.get(word)) + 1
                negFinalProb += math.log(negFrequency / negTotalFreq)


                if word not in self.posD:
                    frequency = float(1)
                    posFinalProb += math.log(frequency / totalFreq)




        if abs(posFinalProb - negFinalProb) <= .2:

            return "neutral"

        elif posFinalProb > negFinalProb:

            return "positive"

        elif posFinalProb < negFinalProb:

            return "negative"

        else:
            return "neutral"






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
