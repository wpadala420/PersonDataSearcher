from functions import search
import credentials


if __name__ == '__main__':
    name = input('Type name and surname\n')
    # print('FACEBOOK SEARCHING...')
    # facebook_result = search.facebook_search(name, credentials.email, credentials.password)
    # print('FACEBOOK SEARCHING FINISHED')
    # print('SEARCHING INSTAGRAM')
    # instagram_result = search.instagram_search(name)
    # print('SEARCHING INSTAGRAM FINISHED')
    print('SEARCHING TWITTER')
    twitter_result = search.twitter_search(name)
    for twiter in twitter_result:
        search.get_tweets_reports(twiter)
    print('TWITTER SEARCHING FINISHED')
    print('PROCESS FINISHED, RESULTS:')
    print(facebook_result)
    print(instagram_result)
    print(twitter_result)