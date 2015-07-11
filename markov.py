import sys
from random import choice
import os
import twitter

class MarkovMachine(object):

    def read_files(self, filenames):
        """Given a list of files, make chains from them."""

        body = ""

        for filename in filenames:
            text_file = open(filename)
            body = body + text_file.read()
            text_file.close()

        self.make_chains(body)

    def make_chains(self, corpus):
        """Takes input text as string; returns dictionary of markov chains."""

        self.chains = {}

        words = corpus.split()

        for i in range(len(words) - 2):
            key = (words[i], words[i + 1])
            value = words[i + 2]

            if key not in self.chains:
                self.chains[key] = []

            self.chains[key].append(value)

    def make_text(self):
        """Takes dictionary of markov chains; returns random text."""

        key = choice(self.chains.keys())
        words = [key[0], key[1]]

        while key in self.chains:
            # Keep looping until we have a key that isn't in the chains
            # (which would mean it was the end of our original text)
            #
            # Note that for long texts (like a full book), this might mean
            # it would run for a very long time.

            word = choice(self.chains[key])
            words.append(word)
            key = (key[1], word)

        text = " ".join(words)

        # This is the clumsiest way to make sure it's never longer than
        # 140 characters; can you think of better ways?
        return text[:140]


if __name__ == "__main__":
    filenames = sys.argv[1:]

    generator = MarkovMachine()
    generator.read_files(filenames)
    print generator.make_text()
    output = generator.make_text()


# Use Python os.environ to get at environmental variables
#
# Note: you must run `source secrets.sh` before running this file
# to make sure these environmental variables are set.

api = twitter.Api(
    consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
    access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

# This will print info about credentials to make sure they're correct
print api.VerifyCredentials()

# Send a tweet
# status = api.PostUpdate('tweet body here')
# print status.text


while True:
    status = api.PostUpdate(output) # post a tweet
    print status.text # print what was posted
    tweet_again = raw_input("Enter to tweet again [q to quit] >")
    if tweet_again == "q":
        break

