# Name:
# Date:
# Description:
#
#

import math, os, pickle, re , os.path, random


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
        self.mPrecision = []
        self.mRecall = []
        self.mF1 = []

        if os.path.isfile("posReviews1Best.bat") and os.path.isfile("negReviews1Best.bat"):
            #  if the dictionaries have already been made, load them
            self.dataSet = self.load("dataSet1.bat")
            self.posD = self.load("posReviews1Best.bat")
            self.negD = self.load("negReviews1Best.bat")
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
        posList = lFileList[2735:(2735*2)]

        random.shuffle(negList)
        random.shuffle(posList)



        negTen = int(2735/10)
        posTen = int(2735/10)

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








        print "Done Training!"



    def classifyBest(self):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """

        for i in range(1, 11):
            self.dataSet = self.load("dataSet" + str(i) + ".bat")
            self.posD = self.load("posReviews" + str(i) + "Best.bat")
            self.negD = self.load("negReviews" + str(i) + "Best.bat")

            posFinalProb = 0
            negFinalProb = 0

            totalFreq = float(sum(self.posD.itervalues())) + float(len(self.posD))
            negTotalFreq = float(sum(self.negD.itervalues())) + float(len(self.negD))

            TruePositive = 0
            FalseNegative = 0

            TrueNegative = 0
            FalsePositive = 0

            for review in self.dataSet:
                summary = review.summary
                summaryTokenized = self.tokenize(summary)

                for word in summaryTokenized:
                    if word in self.posD:
                        frequency = float(self.posD.get(word)) + 1
                        posFinalProb += math.log(frequency / totalFreq)

                        if word not in self.negD:
                            negFinalProb += math.log(float(1) / negTotalFreq)

                    if word in self.negD:
                        negFrequency = float(self.negD.get(word)) + 1
                        negFinalProb += math.log(negFrequency / negTotalFreq)

                        if word not in self.posD:
                            frequency = float(1)
                            posFinalProb += math.log(frequency / totalFreq)

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

                if posFinalProb > negFinalProb:
                    if review.emotion == "P":
                        TruePositive += 1
                    elif review.emotion == "N":
                        FalsePositive += 1

                elif posFinalProb < negFinalProb:

                    if review.emotion == "P":
                        FalseNegative += 1
                    elif review.emotion == "N":
                        TrueNegative += 1

                posFinalProb = 0  # RESET VALUES FOR NEXT ITERATION
                negFinalProb = 0

            posPrecision = float(TruePositive) / float(TruePositive + FalsePositive)
            posRecall = float(TruePositive) / float(TruePositive + FalseNegative)
            posF1 = float(2 * posPrecision * posRecall) / float(posPrecision + posRecall)

            negPrecision = float(TrueNegative) / float(TrueNegative + FalseNegative)
            negRecall = float(TrueNegative) / float(TrueNegative + FalsePositive)
            negF1 = float(2 * negPrecision * negRecall) / float(negPrecision + negRecall)

            print "Precision is (pos,neg): ", posPrecision, negPrecision
            print "Recall is: (pos,neg)", posRecall, negRecall
            print "F1 Measure is: (pos,neg)", posF1, negF1

            microPrecision = float(posPrecision + negPrecision) / float(2)
            microRecall = float(posRecall + negRecall) / float(2)
            microF1 = float(posF1 + negF1) / float(2)

            self.mPrecision.append(microPrecision)
            self.mRecall.append(microRecall)
            self.mF1.append(microF1)

            print "microAveraged precision is: ", float(posPrecision + negPrecision) / float(2)
            print "microAveraged recall is : ", float(posRecall + negRecall) / float(2)
            print "microAveraged F1 Measure is: ", float(posF1 + negF1) / float(2)
            print ""

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

a.classify()

print "total mPrecision: ", a.mPrecision
print "avg(a.mPrecision): ", float(sum(a.mPrecision))/float(10)

print "total mRecall: ", a.mRecall
print "avg(a.mRecall): ", float(sum(a.mRecall))/float(10)

#print "total mF1: ", a.mF1
#print "avg(a.mF1: ", float(sum(a.mF1))/float(10)
