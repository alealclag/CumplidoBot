# -*- coding: utf-8 -*-
import tweepy
import time
import random

from tweepy.error import TweepError
from botCredentials import *
from cumplidos import *

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)

auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)

api = tweepy.API(auth)
lastMentionsID2 = []


# credit for this function to Thomas Ashish Cherian (https://github.com/PandaWhoCodes)


def get_followers(user_name):
    """
    get a list of all followers of a twitter account
    :param user_name: twitter username without '@' symbol
    :return: list of usernames without '@' symbol
    """
    api = tweepy.API(auth)
    followers = []
    for page in tweepy.Cursor(api.followers, screen_name=user_name, wait_on_rate_limit=True, count=200).pages():
        try:
            followers.extend(page)
        except tweepy.TweepError as e:
            time.sleep(60)
    return followers


def get_friends(user_name):

    api = tweepy.API(auth)
    friends = []
    for page in tweepy.Cursor(api.friends, screen_name=user_name, wait_on_rate_limit=True, count=200).pages():
        try:
            friends.extend(page)
        except tweepy.TweepError as e:
            time.sleep(60)
    return friends

def getMutuals(user):
    followersUsernames=[]
    for follower in get_followers(user):
	followersUsernames.append(follower._json["screen_name"])
    friendsUsernames=[]
    for friend in get_friends(user):
	friendsUsernames.append(friend._json["screen_name"])
    
    return list(set(followersUsernames) & set(friendsUsernames))   


def getRandomMutual(user):
    userMutuals = getMutuals(user);
    randomMutual = random.randint(0, len(userMutuals)-1)
    return userMutuals[randomMutual]


def postCompliment(user):
    complimentPerc = 100*len(cumplidos)/(len(cumplidos)+len(pics))
    rand = random.randint(0, 100)

    if rand <= complimentPerc:
        randomCommpliment = cumplidos[random.randint(
            0, len(cumplidos)-1)]
        try:
            api.update_status(
                "@{} {}".format(user, randomCommpliment));print("Complimented " + user)
        except TweepError:
            pass

    elif rand > complimentPerc:
        randomPic = pics[random.randint(
            0, len(pics)-1)]
        try:
            api.update_with_media(filename=randomPic,
                                  status="@{}".format(user));print("Complimented " + user)
        except TweepError:
            pass
    


for mention in api.mentions_timeline()[:10]:
    mentionID = mention._json["id"]
    lastMentionsID2.append(mentionID)

print("Ready to compliment!")

while True:
    lastMentionsID = []
    lastMentions = api.mentions_timeline()[:10]
    for mention in lastMentions:
        mentionedUsers = []
        userCont = 0

        mentionID = mention._json["id"]

        lastMentionsID.append(mentionID)

        if mentionID not in lastMentionsID2:

            textMentionWords = filter(lambda a: a != '' , mention._json["text"].split(" "))

            for palabra in textMentionWords:
                if palabra[0] == "@" and palabra != "@CumplidoBot":

                    mentionedUsers.append(palabra.replace("@", ""))
                    userCont += 1

            if userCont == 0:
                mutualName = getRandomMutual(
                    mention._json["user"]["screen_name"])

                postCompliment(mutualName)

            elif userCont > 0:
                for user in mentionedUsers:
                    postCompliment(user)

            time.sleep(5)

    lastMentionsID2 = lastMentionsID

    time.sleep(10)
