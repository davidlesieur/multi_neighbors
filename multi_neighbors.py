""" Multi-neighbor articles plugin for Pelican.

This plugin adds ``next_articles`` (newer) and ``prev_articles`` (older)
variables to every article's context.
"""

from collections import deque
from pelican import signals


def neighbors(generator):
    # Populate prev_articles.
    prevs = deque([], generator.settings.get('MULTI_NEIGHBORS', 5))
    for article in reversed(generator.articles):
        if not hasattr(article, 'prev_articles'):
            article.prev_articles = []
        if prevs:
            article.prev_articles.extend(prevs)
            if len(prevs) == prevs.maxlen:
                prevs.pop()
        prevs.appendleft(article)

    # Populate next_articles.
    nexts = deque([], generator.settings.get('MULTI_NEIGHBORS', 5))
    for article in generator.articles:
        if not hasattr(article, 'next_articles'):
            article.next_articles = []
        if nexts:
            article.next_articles.extend(nexts)
            if len(nexts) == nexts.maxlen:
                nexts.pop()
        nexts.appendleft(article)


def register():
    signals.article_generator_finalized.connect(neighbors)
