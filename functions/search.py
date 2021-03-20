from modules import FacebookPublicAccountParser, instagram, twitter2, tweetadvanced, Person


def facebook_search(name, email, password):
    fb = FacebookPublicAccountParser.FacebookPublicAccountParser(email, password)
    return fb.loggingSearchNew(name)


def instagram_search(name):
    insta = instagram.InstagramSearcher()
    insta.search(name)
    return insta.peopleFound


def twitter_search(name):
    twitter = twitter2.TwitterSearch()
    twitter.search(name)
    return twitter.found


def get_tweets_reports(person):
    tweetadvanced.get_report(person.twitter['nickname'])
    person.twitter['report'] = person.twitter['nickname'] + '.txt'
