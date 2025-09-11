import snscrape.modules.twitter as sntwitter

for trend in sntwitter.TwitterTrendsScraper(woeid=1).get_items():
    print(trend.name)
    break
