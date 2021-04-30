import tweepy
import time
import random

from tweepy.error import TweepError
from botCredentials import *

auth = tweepy.OAuthHandler(API_KEY,  API_SECRET_KEY)

auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)

api = tweepy.API(auth)
lastMentionsID2 = []
cumplidos = ["Guaperas", "Hermosura", "❤❤❤❤❤", "😍😍😍😍😍😍😍😍😍", "🥵🥵🥵🥵🥵🥵🥵🥵🥵", "😳😳😳😳😳😳😳", "Bellesón", "No te pongas al sol, quel los bombones se derriten",
             "Vaya, no sabía que había gente tan hermosa en Twitter", "Por ti, mi corazón palpita, como una patata frita", "La verdad que te quedan muy bien los sombreros", "Damn u really hot",
             "🏆 Premio a la persona más guuapa de Twitter", "Eres como una rana: muy bonita", "Yo me haría pirata. No por el oro ni por la plata. Sino por ese tesoro, que tienes entre las patas",
             "Vaya peinado más guay tienes", "Hola, somos de la Agencia Tributaria de Belleza. Venimos a cobrarle el impuesto de las grandes fortunas",
             "Si fuese camionero, te llevaría en mi camión. Pero como no lo soy, te llevo en mi corazón",  "Que tengas un buen día :)",
             "¡Buenas! Soy el bot medidor de las personas guapas. Según mis cálculos ¿usted tiene una belleza del 100%!"]

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


def getRandomFriend(user):
    numFriends = len(get_friends(user))
    randomFriend = random.randint(0, numFriends-1)
    return get_friends(user)[
        randomFriend]._json["screen_name"]


lastMentionsID2 = api.mentions_timeline()[:5]

while True:
    lastMentionsID = []
    lastMentions = api.mentions_timeline()[:5]
    for mention in lastMentions:
        mentionedUsers = []
        userCont = 0

        mentionID = mention._json["id"]

        lastMentionsID.append(mentionID)

        if mentionID not in lastMentionsID2:

            textMentionWords = mention._json["text"].split(" ")

            for palabra in textMentionWords:
                if palabra[0] == "@" and palabra != "@CumplidoBot":
                    mentionedUsers.append(palabra)
                    userCont += 1

            if userCont == 0:
                friendName = getRandomFriend(
                    mention._json["user"]["screen_name"])
                randomCommpliment = cumplidos[random.randint(
                    0, len(cumplidos)-1)]

                try:
                    api.update_status(
                        "@{} {}".format(friendName, randomCommpliment))
                except TweepError:
                    pass

            elif userCont > 0:
                for user in mentionedUsers:
                    randomCommpliment = cumplidos[random.randint(
                        0, len(cumplidos)-1)]

                    try:
                        api.update_status("{} {}".format(
                            user, randomCommpliment))
                    except TweepError:
                        pass
            time.sleep(5)

    lastMentionsID2 = lastMentionsID

    time.sleep(60)
