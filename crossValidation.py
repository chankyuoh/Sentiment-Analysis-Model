# Name: Chankyu Oh (con818), Akshat Palnitikar, Shrivant Bhartia sbf324
# Date: 5/19/16
# Description: All group members were present and contributing during all work on this project
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
        self.trainSet = []
        self.mPrecision = []
        self.mRecall = []
        self.mF1 = []


        if not os.path.isfile("posReviewsBest.bat") and not os.path.isfile("negReviewsBest.bat"):
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
                    if self.posD.get(token, False) == False: # if word isn't in the dictionary
                        self.posD[token] = 1  # initialize it with frequency 1
                    else:
                        self.posD[token] += 1  # if already initialized, increment
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

        negList = lFileList[0:2735]  # first 2735 files is negative files
        posList = lFileList[2735:(2735*2)]  # take equal amount of positive files

        random.shuffle(negList)  # shuffle for every iteration
        random.shuffle(posList)  # shuffle for every iteration



        negTen = int(2735/10)  # 10% of negative list
        posTen = int(2735/10)  # 10% of positive list


        # create the data sets, making sure there is no overlap between respective dataSet and trainingSet

        dataSet1 = negList[0:negTen] + posList[0:posTen]

        dataSet2 = negList[negTen:negTen*2] + posList[posTen:posTen*2]

        dataSet3 = negList[negTen*2:negTen*3] + posList[posTen*2:posTen*3]

        dataSet4 = negList[negTen*3:negTen*4] + posList[posTen*3:posTen*4]

        dataSet5 = negList[negTen * 4:negTen * 5] + posList[posTen * 4:posTen * 5]

        dataSet6 = negList[negTen*5:negTen*6] + posList[posTen*5:posTen*6]

        dataSet7 = negList[negTen*6:negTen*7] + posList[posTen*6:posTen*7]

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






        trainSetList = [trainSet1,trainSet2,trainSet3,trainSet4,trainSet5,trainSet6,trainSet7,trainSet8,trainSet9,trainSet10]

        # create each training set
        count = 1
        for trainSet in trainSetList:
            for movie in trainSet:
                if "movies-5" in movie:
                    movieLocation = "movies_reviews/" + movie
                    summary = self.loadFile(movieLocation)
                    tokenSumm = self.tokenize(summary)
                    self.frequencyCalc1(tokenSumm, "positive")
                elif "movies-1" in movie:
                    movieLocation = "movies_reviews/" + movie
                    summary = self.loadFile(movieLocation)
                    tokenSumm = self.tokenize(summary)
                    self.frequencyCalc1(tokenSumm, "negative")

        #  save the dictionaries
            self.save(self.posD, "posReviews"+str(count)+".bat")
            self.save(self.negD, "negReviews"+str(count)+".bat")
            self.negD = {}
            self.posD = {}
            count +=1



        # save the bigram positive and negative dictionaries

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

            self.save(self.posD, "posReviews" + str(count) + "Best.bat")
            self.save(self.negD, "negReviews" + str(count) + "Best.bat")
            self.negD = {}
            self.posD = {}
            count += 1


        # save the dataSets

        dataSetList = [dataSet1,dataSet2,dataSet3,dataSet4,dataSet5,dataSet6,dataSet7,dataSet8,dataSet9,dataSet10]

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

            self.save(self.dataSet,"dataSet"+str(counter)+".bat")
            self.dataSet = []
            counter +=1


    def classify(self):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """




        for i in range(1,11):
            #  iterate through every dataSet+trainSet, and load the appropriate files
            self.dataSet = self.load("dataSet"+str(i)+".bat")
            self.posD = self.load("posReviews"+str(i)+".bat")
            self.negD = self.load("negReviews"+str(i)+".bat")

            #  find total frequency sums
            totalFreq = float(sum(self.posD.itervalues())) + float(len(self.posD))

            negTotalFreq = float(sum(self.negD.itervalues())) + float(len(self.negD))

            posFinalProb = 0
            negFinalProb = 0

            TruePositive = 0
            FalseNegative = 0

            TrueNegative = 0
            FalsePositive = 0

            for review in self.dataSet:
                #  for every review, get the summary, and tokenize it
                summary = review.summary
                summaryTokenized = self.tokenize(summary)

                for word in summaryTokenized:
                    if word in self.posD:
                        frequency = float(self.posD.get(word)) + 1
                        posFinalProb += math.log(frequency / totalFreq)

                        if word not in self.negD:
                            negFrequency = float(1)
                            negFinalProb += math.log(negFrequency / negTotalFreq)

                    if word in self.negD:
                        negFrequency = float(self.negD.get(word)) + 1
                        negFinalProb += math.log(negFrequency / negTotalFreq)

                        if word not in self.posD:
                            frequency = float(1)
                            posFinalProb += math.log(frequency / totalFreq)

                if posFinalProb > negFinalProb:

                    posFinalProb = 0  # RESET VALUES FOR NEXT ITERATION IN FOR LOOP
                    negFinalProb = 0

                    if review.emotion == "P":
                        #  if the review was actually positive and it got classified as positive
                        TruePositive += 1
                    elif review.emotion == "N":
                        #  if the review was actually negative and it got classified as positive
                        FalsePositive += 1

                elif posFinalProb < negFinalProb:
                    posFinalProb = 0
                    negFinalProb = 0
                    if review.emotion == "P":
                        #  if the review was actually positive and it got classified as negative
                        FalseNegative += 1
                    elif review.emotion == "N":
                        #  if the review was actually negative and it got classified as negative
                        TrueNegative += 1

            # calculate precision,recall,F1 values for positive and Negative

            posPrecision = float(TruePositive) / float(TruePositive + FalsePositive)
            posRecall = float(TruePositive) / float(TruePositive + FalseNegative)
            posF1 = float(2 * posPrecision * posRecall) / float(posPrecision + posRecall)

            negPrecision = float(TrueNegative) / float(TrueNegative + FalseNegative)
            negRecall = float(TrueNegative) / float(TrueNegative + FalsePositive)
            negF1 = float(2 * negPrecision * negRecall) / float(negPrecision + negRecall)

            # microaverage the Positive and Negative

            microPrecision = float(posPrecision + negPrecision)/float(2)
            microRecall = float(posRecall + negRecall)/float(2)
            microF1 = float(posF1 + negF1)/float(2)

            # add it to the list of the data

            self.mPrecision.append(microPrecision)
            self.mRecall.append(microRecall)
            self.mF1.append(microF1)

            print "microAveraged precision is: ", float(posPrecision + negPrecision)/float(2)
            print "microAveraged recall is : ", float(posRecall + negRecall)/float(2)
            print "microAveraged F1 Measure is: ", float(posF1 + negF1)/float(2)
            print ""

            # ^ above commented out print will display the average values for the data

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

            #print "Precision is (pos,neg): ", posPrecision, negPrecision
            #print "Recall is: (pos,neg)", posRecall, negRecall
            #print "F1 Measure is: (pos,neg)", posF1, negF1

            microPrecision = float(posPrecision + negPrecision) / float(2)
            microRecall = float(posRecall + negRecall) / float(2)
            microF1 = float(posF1 + negF1) / float(2)

            self.mPrecision.append(microPrecision)
            self.mRecall.append(microRecall)
            self.mF1.append(microF1)

            #print "microAveraged precision is: BIGRAM ", float(posPrecision + negPrecision) / float(2)
            #print "microAveraged recall is : BIGRAM", float(posRecall + negRecall) / float(2)
            #print "microAveraged F1 Measure is: ", float(posF1 + negF1) / float(2)
            #print ""


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

#print "total mPrecision: ", a.mPrecision
print "avg(a.mPrecision) UNIGRAM: ", float(sum(a.mPrecision))/float(10)

#print "total mRecall: ", a.mRecall
print "avg(a.mRecall) UNIGRAM: ", float(sum(a.mRecall))/float(10)

print ""

a.mF1 = []
a.mPrecision = []
a.mRecall = []

a.classifyBest()

#print "total mPrecision: ", a.mPrecision
print "avg(a.mPrecision) BIGRAM: ", float(sum(a.mPrecision))/float(10)

#print "total mRecall: ", a.mRecall
print "avg(a.mRecall) BIGRAM: ", float(sum(a.mRecall))/float(10)


#print "total mF1: ", a.mF1
#print "avg(a.mF1: ", float(sum(a.mF1))/float(10)

