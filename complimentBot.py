import tweepy
import json
import time
import random
from twitterCredentials import *

auth = tweepy.OAuthHandler(API_KEY,  API_SECRET_KEY)

auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)

api = tweepy.API(auth)
lastMention2 = ""
cumplidos = ["Guaperas", "Hermosura", "❤❤❤❤❤", "😍😍😍😍😍😍😍😍😍", "🥵🥵🥵🥵🥵🥵🥵🥵🥵", "😳😳😳😳😳😳😳", "Bellesón", "No te pongas al sol, quel los bombones se derriten",
             "Vaya, no sabía que había gente tan hermosa en Twitter", "Por ti, mi corazón palpita, como una patata frita", "La verdad que te quedan muy bien los sombreros", "Damn u really hot",
             "🏆 Premio a la persona más guuapa de Twitter", "Eres como una rana: muy bonita", "Yo me haría pirata. No por el oro ni por la plata. Sino por ese tesoro, que tienes entre las patas",
             "Vaya peinado más guay tienes", "Hola, somos de la Agencia Tributaria de Belleza. Venimos a cobrarle el impuesto de las grandes fortunas",
             "Si fuese camionero, te llevaría en mi camión. Pero como no lo soy, te llevo en mi corazón",  "Que tengas un buen día :)",
             "¡Buenas! Soy el bot medidor de las personas guapas. Según mis cálculos ¿usted tiene una belleza del 100%!"]


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
            print("Going to sleep:", e)
            time.sleep(60)
    return followers


while True:
    lastMention = api.mentions_timeline()[0]._json["user"]["screen_name"]

    if lastMention != lastMention2:
        lastMention2 = lastMention
        numFollowers = len(get_followers(lastMention))
        randomFollower = random.randint(0, numFollowers-1)
        followerName = json.dumps(get_followers(lastMention)[randomFollower]._json).split(
            "screen_name")[1].split('"')[2]

        randomCommpliment = cumplidos[random.randint(0, len(cumplidos)-1)]
        api.update_status("@{} {}".format(followerName, randomCommpliment))

    time.sleep(60)
