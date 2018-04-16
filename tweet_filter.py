"""
    Author: Charles Carlson 2018
    This script was written for CS:4440 Web Mining Homework 2  

    The purpose of this script is to parse .txt files of tweets,
    rate their relevance to the user's life, and generate new files
    of reformatted tweets. In the form: userID|tweetID|relevance
"""

import sys
import os
import string

"""
    This function takes as input a file, reads
    the lines of the file and places each line
    into an array. This array represents a list
    of tweets
"""
def generateListOfTweets(file):
    tweet_file = open(file,"r", encoding="utf-8")
    tweetList = []
    for line in tweet_file.readlines():
        tweetList.append(line)
    return tweetList

"""
    "Content" is referring to the text part of a tweet.
    The content is passed to this function and determined
    to be either relevant (1) or irrelevant (0)
"""

"""
    
    "myX": "my" and "life" or "me" or "im" or "i'm" or "i am",
    "day": "best" or "worst" and "day",
    "iQuality": "i feel" or "i m feeling" or "im feeling" or "feeling" or "i m having" or "im having",
    "iAm": "im " or "i'm " or "i am "

"""

def relevant(content):
    if isRt(content):
        return 0
    if relevantByKeyPhrases(content):
        return 1
    if relevantByKeyWords(content):
        return 1
    else: 
        return 0

def relevantByKeyWords(content):
    for word in keyWords:
        if word in content:
            return True

def relevantByKeyPhrases(content):
    for phrase in keyPhrases:
        if keyPhrases[phrase] in content:
            return True

def isRt(content):
    if content[0:2] == "rt":
        return True

keyPhrases = {
    "loveX": "i love" or "i hate" "i like" and ("me" or "myself" or "my" or "life"),
    "haveX": "i have" and ("friend" or "friends" or "mother" or "mom" or "father" or "dad" or "life")
}

keyWords = [
    "im", "i'm", "i am", "life", "my", "i feel", "im feeling", "i'm feeling", "feels",
    "im having", "i'm having", "im having", "i have"
]


"""
    This function is given a list of formatted tweets
    i.e userID|tweetID|relevance, and a name for the 
    file they are to be written into. It creates the 
    file with the specified name and writes the tweets 
    into that file.
"""
def writeFile(tweets, fs):
    if not os.path.isdir("Part2_filtered/"):
        os.mkdir("Part2_filtered/")
    txt_file = open(fs, "w", encoding="utf-8")
    for tweet in tweets:
        txt_file.write(tweet + "\n")

"""
    This function's job is to parse the tweets in their
    original format, locate the important pieces: userID,
    tweetID, content, and return a new list of reformatted 
    tweets. i.e in the format userID|tweetID|relevance
"""
def getRelevantTweets(tweetList):
    currentString = ""
    iterCount = 0
    tweets = []
    for tweet in tweetList:
        try:
            for char in tweet:
                if iterCount == 0:
                    currentString += char
                    if char == "|":
                        userId = currentString
                        currentString = ""
                        iterCount += 1
                elif iterCount == 1:
                    currentString += char
                    if char == "|":
                        tweetId = currentString
                        currentString = ""
                        iterCount += 1
                elif iterCount == 2:
                    if char == "|":
                        content = currentString
                        content = content.lower()
                        relevance = relevant(content) 
                        iterCount = 0
                        currentString = ""
                        break
                    else:
                        currentString += char
                else:
                    continue
            tweet = "%s%s%s" % (userId, tweetId, relevance)
            tweets.append(tweet)
            tweet = ""
        except UnboundLocalError as e:
            pass
    return tweets

def main():
    """
        path represents the path to the original tweet .txt files
        newPath represents where filtered files will be placed
    """
    path = "Part2/"
    newPath = "Part2_filtered/"

    """
        Console paramter -test is only used for testing purposes
    """
    if sys.argv[1] == "-test":
        file = "Part2/test.txt"
        tweets = generateListOfTweets(file)
        r = getRelevantTweets(tweets)
        fs = "test.txt"
        writeFile(r,fs) 

    """
        Use parameter -m if you're doing a non-test run of the 
        program
    """
    if sys.argv[1] == "-m":
        for text_file in os.listdir(path):
            tweetList = generateListOfTweets(path + text_file)
            tweets = getRelevantTweets(tweetList)
            filteredFileName = str(text_file[0:-4] + "_filtered_carlson.txt")
            filteredFileName = newPath + filteredFileName 
            writeFile(tweets,filteredFileName)    

if __name__ == "__main__": 
    main()

