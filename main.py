from functions import search, file_functions, matching_functions
from modules import Person
import credentials
import time
from datetime import datetime
import pickle


if __name__ == '__main__':
    # file_functions.clear_temportary_files('tmp/facebook')
    # file_functions.clear_temportary_files('tmp/instagram')
    # file_functions.clear_temportary_files('tmp/twitter')


    name = input('Type name and surname\n')
    print('START:' + datetime.now().strftime("%H:%M:%S"))
    print('FACEBOOK SEARCHING...')
    facebook_result = search.facebook_search(name, credentials.email, credentials.password)
    # with open('facebook.dump', 'wb') as facebook_dump:
    #     pickle.dump(facebook_result, facebook_dump)

    print('FACEBOOK SEARCHING FINISHED')
    print(datetime.now().strftime("%H:%M:%S"))
    print('SEARCHING INSTAGRAM')
    instagram_result = search.instagram_search(name)
    # with open('instagram.dump', 'wb') as instagram_dump:
    #     pickle.dump(instagram_result, instagram_dump)

    print('SEARCHING INSTAGRAM FINISHED')
    print(datetime.now().strftime("%H:%M:%S"))
    print('SEARCHING TWITTER')
    twitter_result = search.twitter_search(name)
    for twiter in twitter_result:
        search.get_tweets_reports(twiter)
    # with open('twitter.dump', 'wb') as twitter_dump:
    #     pickle.dump(twitter_result, twitter_dump)

    print('TWITTER SEARCHING FINISHED')
    print(datetime.now().strftime("%H:%M:%S"))
    print('PROCESS FINISHED, RESULTS:')
    print(facebook_result)
    print(instagram_result)
    print(twitter_result)

    fb_profiles_used = []
    insta_profiles_used = []
    twitter_profiles_used = []

    new_profiles = []
    print('PROFILES CONNECTING START')
    print(datetime.now().strftime("%H:%M:%S"))
    for fb_res in facebook_result:
        for insta_res in instagram_result:
            if matching_functions.profile_used(fb_profiles_used, fb_res) is False and matching_functions.profile_used(insta_profiles_used, insta_res) is False and matching_functions.match_profiles_by_photos(fb_res, insta_res):
                fb_profiles_used.append(fb_res)
                insta_profiles_used.append(insta_res)
                new_profiles.append(matching_functions.fuse_profiles(fb_res, insta_res))
                print('POŁĄCZONO FB Z INSTA')
        for twit_res in twitter_result:
            if matching_functions.profile_used(twitter_profiles_used, twit_res) is False and matching_functions.profile_used(fb_profiles_used, fb_res) is False and matching_functions.match_profiles_by_photos(fb_res, twit_res):
                fb_profiles_used.append(fb_res)
                twitter_profiles_used.append(twit_res)
                new_profiles.append(matching_functions.fuse_profiles(fb_res, twit_res))
                print('POŁĄCZONO FB Z TWITTEREM')
    for insta_res in instagram_result:
        for fb_res in facebook_result:
            if matching_functions.profile_used(insta_profiles_used, insta_res) is False and matching_functions.profile_used(fb_profiles_used, fb_res) is False and matching_functions.match_profiles_by_photos(insta_res, fb_res):
                fb_profiles_used.append(fb_res)
                insta_profiles_used.append(insta_res)
                new_profiles.append(matching_functions.fuse_profiles(insta_res, fb_res))
                print('POŁĄCZONO INSTA Z FB')
        for twit_res in twitter_result:
            if matching_functions.profile_used(twitter_profiles_used, twit_res) is False and matching_functions.profile_used(insta_profiles_used, insta_res) is False and  matching_functions.match_profiles_by_photos(insta_res, twit_res):
                insta_profiles_used.append(insta_res)
                twitter_profiles_used.append(twit_res)
                new_profiles.append(matching_functions.fuse_profiles(insta_res, twit_res))
                print('POŁĄCZONO INSTA Z TWITTEREM')

    for twit_res in twitter_result:
        for fb_res in facebook_result:
            if matching_functions.profile_used(fb_profiles_used, fb_res) is False and matching_functions.profile_used(twitter_profiles_used, twit_res) is False and matching_functions.match_profiles_by_photos(twit_res, fb_res):
                twitter_profiles_used.append(twit_res)
                fb_profiles_used.append(fb_res)
                new_profiles.append(matching_functions.fuse_profiles(twit_res, fb_res))
                print('POŁĄCZONO TWITTERA Z FB')
        for insta_res in instagram_result:
            if matching_functions.profile_used(twitter_profiles_used, twit_res) is False and matching_functions.profile_used(insta_profiles_used, insta_res) is False and matching_functions.match_profiles_by_photos(twit_res, insta_res):
                twitter_profiles_used.append(twit_res)
                insta_profiles_used.append(insta_res)
                new_profiles.append(matching_functions.fuse_profiles(twit_res, insta_res))
                print('POŁĄCZONO TWITTERA Z INSTA')
    print('SECOND LOOP STARTED')
    print(datetime.now().strftime("%H:%M:%S"))
    new_profile_used = []
    complete_profiles = []
    for new_profile in new_profiles:
        if len(new_profile.twitter) > 0 and len(new_profile.instagram) > 0:
            for fb_res in facebook_result:
                if matching_functions.profile_used(fb_profiles_used, fb_res) is False and matching_functions.profile_used(new_profile_used, new_profile) is False and matching_functions.match_profiles_by_photos(new_profile, fb_res):
                    new_profile_used.append(new_profile)
                    fb_profiles_used.append(fb_res)
                    complete_profiles.append(matching_functions.fuse_profiles(new_profile, fb_res))
        elif len(new_profile.instagram) > 0 and len(new_profile.facebook) > 0:
            for twit_res in twitter_result:
                if matching_functions.profile_used(new_profile_used, new_profile) is False and matching_functions.profile_used(twitter_profiles_used, twit_res) is False and matching_functions.match_profiles_by_photos(new_profile, twit_res):
                    twitter_profiles_used.append(twit_res)
                    new_profile_used.append(new_profile)
                    complete_profiles.append(matching_functions.fuse_profiles(new_profile, twit_res))
        elif len(new_profile.facebook) > 0 and len(new_profile.twitter) > 0:
            for insta_res in instagram_result:
                if matching_functions.profile_used(new_profile_used, new_profile) is False and matching_functions.profile_used(insta_profiles_used, insta_res) is False and matching_functions.match_profiles_by_photos(new_profile, insta_res):
                    new_profile_used.append(new_profile)
                    insta_profiles_used.append(insta_res)
                    complete_profiles.append(matching_functions.fuse_profiles(new_profile, insta_res))

    for n_profile in new_profiles:
        if matching_functions.profile_used(new_profile_used, n_profile) is False:
            complete_profiles.append(n_profile)
            new_profile_used.append(n_profile)
    for f_res in facebook_result:
        if matching_functions.profile_used(fb_profiles_used, f_res) is False:
            fb_profiles_used.append(f_res)
            complete_profiles.append(f_res)
    for i_res in instagram_result:
        if matching_functions.profile_used(insta_profiles_used, i_res) is False:
            insta_profiles_used.append(i_res)
            complete_profiles.append(i_res)
    for t_res in twitter_result:
        if matching_functions.profile_used(twitter_profiles_used, t_res) is False:
            twitter_profiles_used.append(t_res)
            complete_profiles.append(t_res)
    print('FINISH, complete results:')
    print(datetime.now().strftime("%H:%M:%S"))
    print(complete_profiles)






