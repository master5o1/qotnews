import logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)

if __name__ == '__main__':
    import sys
    sys.path.insert(0,'.')

import praw
from praw.exceptions import PRAWException
from praw.models import MoreComments
from prawcore.exceptions import PrawcoreException

from utils import render_md, clean

SUBREDDITS = 'Economics+AcademicPhilosophy+DepthHub+Foodforthought+HistoryofIdeas+LaymanJournals+PhilosophyofScience+PoliticsPDFs+Scholar+StateOfTheUnion+TheAgora+TrueFilm+TrueReddit+UniversityofReddit+culturalstudies+hardscience+indepthsports+indepthstories+ludology+neurophilosophy+resilientcommunities+worldevents'

SITE_LINK = lambda x : 'https://old.reddit.com{}'.format(x)
SITE_AUTHOR_LINK = lambda x : 'https://old.reddit.com/u/{}'.format(x)

reddit = praw.Reddit('bot')

def feed():
    try:
        return [x.id for x in reddit.subreddit(SUBREDDITS).hot()]
    except KeyboardInterrupt:
        raise
    except PRAWException as e:
        logging.error('Problem hitting reddit API: {}'.format(str(e)))
        return []
    except PrawcoreException as e:
        logging.error('Problem hitting reddit API: {}'.format(str(e)))
        return []

def comment(i):
    if isinstance(i, MoreComments):
        return False
    if '[removed]' in i.body or '[deleted]' in i.body:
        return False
    if i.author and i.author.name == 'AutoModerator':
        return False

    c = {}
    c['author'] = i.author.name if i.author else '[Deleted]'
    c['score'] = i.score
    c['date'] = i.created_utc
    c['text'] = render_md(clean(i.body))
    c['comments'] = [comment(j) for j in i.replies]
    c['comments'] = list(filter(bool, c['comments']))
    return c

def story(ref):
    try:
        r = reddit.submission(ref)
        if not r: return False

        s = {}
        s['author'] = r.author.name if r.author else '[Deleted]'
        s['author_link'] = SITE_AUTHOR_LINK(r.author)
        s['score'] = r.score
        s['date'] = r.created_utc
        s['title'] = r.title
        s['link'] = SITE_LINK(r.permalink)
        s['url'] = r.url
        s['comments'] = [comment(i) for i in r.comments]
        s['comments'] = list(filter(bool, s['comments']))
        s['num_comments'] = r.num_comments

        if s['score'] < 25 and s['num_comments'] < 10:
            return False

        if r.selftext:
            s['text'] = render_md(clean(r.selftext))

        return s

    except KeyboardInterrupt:
        raise
    except PRAWException as e:
        logging.error('Problem hitting reddit API: {}'.format(str(e)))
        return False
    except PrawcoreException as e:
        logging.error('Problem hitting reddit API: {}'.format(str(e)))
        return False

# scratchpad so I can quickly develop the parser
if __name__ == '__main__':
    #print(feed())
    #print(reddit.submission(feed()[0]).permalink)
    #print()
    print(story('e4asnp'))
