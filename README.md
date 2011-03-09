## Feed-o-mizer ##

### Convert feeds to valid Atom format ###


The application converting [RSS feeds](http://www.whatisrss.com/) from different formats (RSS 1.0, RSS 2.0 etc.) to [valid Atom 1.0 format](http://validator.w3.org/feed/), using great [Universal Feed Parser](http://www.feedparser.org/) python library.

You can consume the feed on URL (In the moment the application is [deployed on Google AppEngine](http://feedomizer.appspot.com/)):

    http://feedomizer.appspot.com/atom?uri=[Your original feed URL]

*Example*: [HackerNews Atom Feed](http://feedomizer.appspot.com/atom?uri=http://news.ycombinator.com/rss)

The application also providing additional service for converting RSS feeds to [JSON format](http://json.org/) on URL:

    http://feedomizer.appspot.com/json?uri=[Your original feed URL]

*Example*: [HackerNews JSON](http://feedomizer.appspot.com/json?uri=http://news.ycombinator.com/rss)
