import feedparser

from pprint import pprint

feed = feedparser.parse('https://www.legis.state.pa.us/WU01/LI/RSS/SenateMembers.xml')
print(len(feed.entries))
pprint(feed.entries[0].keys())