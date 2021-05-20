from modules import FacebookPublicAccountParser, instagram, twitter2, tweetadvanced, Person, rejestr


def facebook_search(name, email, password):
    fb = FacebookPublicAccountParser.FacebookPublicAccountParser(email, password)
    people = []
    for profile in fb.loggingSearchNew(name):
        person = Person.Person()
        person.facebook = profile['facebook']
        people.append(person)
    return people


def get_hashtag_from_line(line):
    result = ''
    hash_index = 0
    for char_ in range(len(line)):
        if line[char_] == '#':
            hash_index = char_
            break
    space_count = 0
    for index in range(hash_index + 1, len(line)):
        if space_count == 3:
            break
        if line[index] != ' ':
            result = result + line[index]
        else:
            space_count = space_count + 1
    return result


def get_top_hashtags_from_tt_report(path):
    hashtag_list = []
    hashtags_lines_list = []
    with open(path, 'rb') as report_file:
        hashtags_lines = False
        for line in report_file:
            if '[+] Top 10 hashtags' in str(line, encoding='utf-8'):
                hashtags_lines = True
            elif '[+]' in str(line, encoding='utf-8'):
                hashtags_lines = False
            elif hashtags_lines:
                hashtags_lines_list.append(str(line, encoding='utf-8'))
    if len(hashtags_lines_list) > 0:
        for hashtag_line in hashtags_lines_list:
            hashtag_list.append(get_hashtag_from_line(hashtag_line))
    return hashtag_list


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
    person.twitter['report'] = 'tmp/twitter/ ' + person.twitter['nickname'] + '.txt'
    person.twitter['hashtags'] = []



def registries_search(name):
    rs = rejestr.RegistrySearcher()
    rs.searchData(name)
    return rs.peopleFound

