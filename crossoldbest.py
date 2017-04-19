# Name:
# Date:
# Description:
#
#

import math, os, pickle, re , os.path


class review:
    def __init__(self):
        self.summary = ""
        self.emotion = ""

class Bayes_Classifier:
    def __init__(self):
        """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a
        cache of a trained classifier has been stored, it loads this cache.  Otherwise,
        the system will proceed through training.  After running this method, the classifier
        is ready to classify input text."""
        self.posD = {}
        self.negD = {}
        self.dataSet = []
        self.trainSet = []

        if os.path.isfile("posReviews1Best.bat") and os.path.isfile("negReviews1Best.bat") and os.path.isfile("dataSet1Best.bat"):
            #  if the dictionaries have already been made, load them
            self.dataSet = self.load("dataSet1.bat")
            self.posD = self.load("posReviews1.bat")
            self.negD = self.load("negReviews1.bat")
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

    def frequencyCalc2(self,tokenSumm, dictType):
        """calculates frequencies of bigrams (double words) and adds it to respect dictionary"""
        for x in range(len(tokenSumm)):
            if x != len(tokenSumm) - 1:
                w1 = tokenSumm[x]
                w2 = tokenSumm[x + 1]
                token = w1 + "_" + w2
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

        negList = lFileList[0:2735]
        posList = lFileList[2735:]



        negTen = int(2735/10)
        posTen = int(11129/10)

        dataSet1 = negList[0:negTen] + posList[0:posTen]

        dataSet2 = negList[negTen:negTen * 2] + posList[posTen:posTen * 2]

        dataSet3 = negList[negTen * 2:negTen * 3] + posList[posTen * 2:posTen * 3]

        dataSet4 = negList[negTen * 3:negTen * 4] + posList[posTen * 3:posTen * 4]

        dataSet5 = negList[negTen * 4:negTen * 5] + posList[posTen * 4:posTen * 5]

        dataSet6 = negList[negTen * 5:negTen * 6] + posList[posTen * 5:posTen * 6]

        dataSet7 = negList[negTen * 6:negTen * 7] + posList[posTen * 6:posTen * 7]

        dataSet8 = negList[negTen * 7:negTen * 8] + posList[posTen * 7:posTen * 8]

        dataSet9 = negList[negTen * 8:negTen * 9] + posList[posTen * 8:posTen * 9]

        dataSet10 = negList[negTen * 9:negTen * 10] + posList[posTen * 9:posTen * 10]

        trainSet1 = negList[negTen:] + posList[posTen:]

        trainSet2 = negList[0:negTen] + negList[negTen * 2:] + posList[0:posTen] + posList[posTen * 2:]

        trainSet3 = negList[0:negTen * 2] + negList[negTen * 3:] + posList[0:posTen * 2] + posList[posTen * 3:]

        trainSet4 = negList[0:negTen * 3] + negList[negTen * 4:] + posList[0:posTen * 3] + posList[posTen * 4:]

        trainSet5 = negList[0:negTen * 4] + negList[negTen * 5:] + posList[0:posTen * 4] + posList[posTen * 5:]

        trainSet6 = negList[0:negTen * 5] + negList[negTen * 6:] + posList[0:posTen * 5] + posList[posTen * 6:]

        trainSet7 = negList[0:negTen * 6] + negList[negTen * 7:] + posList[0:posTen * 6] + posList[posTen * 7:]

        trainSet8 = negList[0:negTen * 7] + negList[negTen * 8:] + posList[0:posTen * 7] + posList[posTen * 8:]

        trainSet9 = negList[0:negTen * 8] + negList[negTen * 9:] + posList[0:posTen * 8] + posList[posTen * 9:]

        trainSet10 = negList[0:negTen * 9] + negList[negTen * 10:] + posList[0:posTen * 9] + posList[posTen * 10:]



        trainSetList = [trainSet1, trainSet2, trainSet3, trainSet4, trainSet5, trainSet6, trainSet7, trainSet8,
                        trainSet9, trainSet10]



        count = 1
        for trainSet in trainSetList:
            for movie in trainSet:
                if "movies-5" in movie:
                    movieLocation = "movies_reviews/" + movie
                    summary = self.loadFile(movieLocation)
                    tokenSumm = self.tokenize(summary)
                    self.frequencyCalc1(tokenSumm, "positive")
                    self.frequencyCalc2(tokenSumm, "positive")
                elif "movies-1" in movie:
                    movieLocation = "movies_reviews/" + movie
                    summary = self.loadFile(movieLocation)
                    tokenSumm = self.tokenize(summary)
                    self.frequencyCalc1(tokenSumm, "negative")
                    self.frequencyCalc2(tokenSumm, "negative")

            self.save(self.posD, "posReviews"+str(count)+"Best.bat")
            self.save(self.negD, "negReviews"+str(count)+"Best.bat")
            self.negD = {}
            self.posD = {}
            count +=1

        dataSetList = [dataSet1, dataSet2, dataSet3, dataSet4, dataSet5, dataSet6, dataSet7, dataSet8, dataSet9,
                       dataSet10]


        counter = 1
        for dataSet in dataSetList:
            for movie1 in dataSet:

                if "movies-5" in movie1:

                    rev = review()
                    movieLocation = "movies_reviews/" + movie1
                    rev.summary = self.loadFile(movieLocation)
                    rev.emotion = "P"
                    self.dataSet.append(rev)
                elif "movies-1" in movie1:
                    movieLocation = "movies_reviews/" + movie1
                    negrev = review()
                    negrev.summary = self.loadFile(movieLocation)
                    negrev.emotion = "N"
                    self.dataSet.append(negrev)

            self.save(self.dataSet, "dataSet" + str(counter) + "Best.bat")
            self.dataSet = []
            counter += 1


    def classify(self, dataSet):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """

        posFinalProb = 0
        negFinalProb = 0
        negTen = int(2735 / 10)

        negList = []

        posList = []

        totalFreq = float(sum(self.posD.itervalues())) + float(len(self.posD))

        negTotalFreq = float(sum(self.negD.itervalues())) + float(len(self.negD))

        TruePositive = 0
        FalseNegative = 0

        TrueNegative = 0
        FalsePositive = 0

        Neutral = 0




        for review in dataSet:
            summary = review.summary
            summaryTokenized = self.tokenize(summary)

            if review.emotion == "P":
                for word in summaryTokenized:
                    if summaryTokenized.index(word) != len(summaryTokenized)-1: #as long as not last element
                        curr = summaryTokenized.index(word)
                        next = curr +1
                        word1 = summaryTokenized[curr]
                        word2 = summaryTokenized[next]
                        bigram = word1+ "_" + word2

                        if bigram in self.posD:

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

                    unigram = word
                    print "unigram: ", unigram

                    if unigram in self.posD:

                        frequency = float(self.posD.get(unigram)) + float(1)
                        posFrac = frequency / totalFreq
                        posFinalProb += math.log(posFrac)

                        if unigram not in self.negD:
                            negFrequency = float(1)
                            negFrac = negFrequency / negTotalFreq
                            negFinalProb += math.log(negFrac)

                    if unigram in self.negD:
                        negFrequency = float(self.negD.get(unigram)) + float(1)

                        negFinalProb += math.log(negFrequency / negTotalFreq)

                        if unigram not in self.posD:
                            frequency = float(1)
                            posFinalProb += math.log(frequency / totalFreq)

                if abs(posFinalProb - negFinalProb) <= .2:
                    posFinalProb = 0
                    negFinalProb = 0
                    Neutral += 1


                elif posFinalProb > negFinalProb:
                    posFinalProb = 0
                    negFinalProb = 0
                    print "TruePositive"
                    TruePositive += 1

                elif posFinalProb < negFinalProb:

                    posFinalProb = 0
                    negFinalProb = 0
                    print "FalseNegative"
                    FalseNegative += 1

                else:
                    print "else reached"


            if review.emotion == "N":
                for word in summaryTokenized:
                    if summaryTokenized.index(word) != len(summaryTokenized) - 1:  # as long as not last element
                        curr = summaryTokenized.index(word)
                        next = curr + 1
                        word1 = summaryTokenized[curr]
                        word2 = summaryTokenized[next]
                        bigram = word1 + "_" + word2

                        if bigram in self.posD:

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

                    unigram = word

                    if unigram in self.posD:

                        frequency = float(self.posD.get(unigram)) + float(1)
                        posFrac = frequency / totalFreq
                        posFinalProb += math.log(posFrac)

                        if unigram not in self.negD:
                            negFrequency = float(1)
                            negFrac = negFrequency / negTotalFreq
                            negFinalProb += math.log(negFrac)

                    if unigram in self.negD:

                        negFrequency = float(self.negD.get(unigram)) + float(1)

                        negFinalProb += math.log(negFrequency / negTotalFreq)

                        if unigram not in self.posD:
                            frequency = float(1)
                            posFinalProb += math.log(frequency / totalFreq)

                if abs(posFinalProb - negFinalProb) <= .2:
                    posFinalProb = 0
                    negFinalProb = 0
                    Neutral += 1


                elif posFinalProb > negFinalProb:
                    posFinalProb = 0
                    negFinalProb = 0
                    print "FalsePositive"
                    FalsePositive += 1

                elif posFinalProb < negFinalProb:

                    posFinalProb = 0
                    negFinalProb = 0
                    print "TrueNegative"
                    TrueNegative += 1

                else:
                    print "else reached"




        print "falsePositive total: ", FalsePositive
        print "falseNegative total: ", FalseNegative
        precision = float(TruePositive) / float(TruePositive + FalsePositive)
        recall = float(TruePositive) / float(TruePositive + FalseNegative)
        F1 = float(2 * precision * recall) / float(precision + recall)

        print "Precision is: ", precision
        print "Recall is: ", recall
        print "F1 Measure is: ", F1

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
#a.train()

a.classify(a.dataSet)
