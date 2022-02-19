from TikTokApi import TikTokApi
import csv
from feedgen.feed import FeedGenerator
from datetime import datetime, timezone


# Normal GitHub Pages URL
ghPagesURL = "https://james-wilson-21.github.io/tiktok-rss-flat/"

# Custom Domain
# ghPagesURL = "https://james-wilson-21.github.io/tiktok-rss-flat/"

api = TikTokApi()

count = 10

with open('subscriptions.csv') as f:
    cf = csv.DictReader(f, fieldnames=['username'])
    for row in cf:
        user = row['username']

        print(f'Running for user \'{user}\'')

        fg = FeedGenerator()
        fg.id('https://www.tiktok.com/@' + user)
        fg.title('@' + user + ' TikTok')
        fg.author( {'name':'James Wilson','email':'support@maorilandinfo.co.nz'} )
        fg.link( href='http://tiktok.com', rel='alternate' )
        fg.logo(ghPagesURL + 'tiktok-rss.png')
        fg.subtitle('Latest TikToks from ' + user)
        fg.link( href=ghPagesURL + 'rss/' + user + '.xml', rel='self' )
        fg.language('en')

        # Set the last modification time for the feed to be the most recent post, else now.
        updated=None

        for tiktok in api.user(username=user).videos(count=count):
            fe = fg.add_entry().insert(0)
            link = "https://tiktok.com/@" + user + "/video/" + tiktok.id
            fe.id(link)
            ts = datetime.fromtimestamp(tiktok.as_dict['createTime'], timezone.utc)
            fe.published(ts)
            fe.updated(ts)
            updated = max(ts, updated) if updated else ts
            fe.title(tiktok.as_dict['desc'])
            fe.link(href=link)
            fe.description("<img src='" + tiktok.as_dict['video']['cover'] + "' />")

        fg.updated(updated)
        newFile = 'rss/' + user + '.xml'

        fg.atom_file(newFile, pretty=True) # Write the RSS feed to a file


