[microformats][0] are the simplest way to openly publish contacts, events,
reviews, recipes, and other structured information on the web.

    >>> import mf
    >>> url = "https://alice.example"
    >>> doc = f'''
    ... <p class=h-card><a href={url}>Alice</a></p>
    ... <ul class=h-feed>
    ... <li class=h-entry>foo
    ... <li class=h-entry>bar
    ... </ul>
    ... '''
    >>> page = mf.parse(doc=doc, url=url)

    # TODO >>> dict(page)
    # TODO >>> page.json

    >>> card = page["items"][0]
    >>> card["type"]
    ['h-card']
    >>> card["properties"]
    {'name': ['Alice'], 'url': ['https://alice.example']}
    >>> feed = page["items"][1]
    >>> feed["children"][0]["properties"]["name"]
    ['foo']

    >>> mf.util.representative_card(page, url)
    {'name': ['Alice'], 'url': ['https://alice.example']}
    >>> mf.util.representative_feed(page, url)["items"][0]["name"]
    ['foo']

    # TODO >>> page.representative_card
    # TODO {'name': ['Alice'], 'url': ['https://alice.example']}
    # TODO >>> page.representative_feed["items"][0]["name"]
    # TODO ['foo']

Based upon [`mf2util`][1].

[0]: https://microformats.org/wiki/microformats
[1]: https://github.com/kylewm/mf2util
