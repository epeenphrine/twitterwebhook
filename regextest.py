
import re

text = 'Donald J. TrumpRetweetedThe White House‏Verified account@WhiteHouseApr 15MoreCopy link to TweetEmbed TweetWe are using every available authority to accelerate the development, study, and delivery of therapies.pic.twitter.com/GKbkUd0nxd3,301 replies8,906 retweets37,938 likesReplyRetweetRetweetedLikeLiked'

tweeted_today = re.findalll(r'')
tweeted_not_today = re.findall(r'\w\w\w \d\d|\w\w\w \d', text)

print(search)