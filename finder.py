import tweepy
import json
import argparse

def parse_args():
    p = argparse.ArgumentParser(description = \
    '''
    Find the Twitter Account most likely matching a name
    ''')
    p.add_argument('--api-key', help='Twitter API Key', required=True)
    p.add_argument('--api-secret', help='Twitter API Secret', required=True)
    p.add_argument('--api-user', help='Twitter API User ID', required=True)
    p.add_argument('--api-user-secret', help='Twitter API User Secret', required=True)
    p.add_argument('--name', help='Name to search for', required=True)
    return p.parse_args()


def main():

    class MyModelParser(tweepy.parsers.ModelParser):
        def parse(self, method, payload):
            result = super(MyModelParser, self).parse(method, payload)
            result._payload = json.loads(payload)
            return result

    args = parse_args()
    auth = tweepy.OAuthHandler(args.api_key, args.api_secret)
    auth.set_access_token(args.api_user, args.api_user_secret)
    api = tweepy.API(auth, parser=MyModelParser())

    print "Auth complete"

#    import ipdb; ipdb.set_trace()
    for user in tweepy.Cursor(api.search_users, args.name, 1).items(20):
        followers = user.followers_count
        name = user.name
        url = user.url
        print "{}: {} {}".format(name, followers, url)

if __name__ == "__main__":
    main()
