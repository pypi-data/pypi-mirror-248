"""
Tools for microformats production, consumption and analysis.

Microformats are a general way to mark up any HTML document with
classes and propeties. This module uses domain-specific assumptions
about the classes (specifically h-card, h-entry and h-event) to extract
certain interesting properties.

"""

import collections
import datetime
import re
import string
import unicodedata
from urllib.parse import urljoin

import bs4
import easyuri
from mf2py import parse

__all__ = ["parse", "representative_card"]

URL_ATTRIBUTES = {
    "a": ["href"],
    "link": ["href"],
    "img": ["src"],
    "audio": ["src"],
    "video": ["src", "poster"],
    "source": ["src"],
}

# From https://indieweb.org/location#How_to_determine_the_location_of_a_microformat
LOCATION_PROPERTIES = frozenset(
    (
        "street-address",
        "extended-address",
        "post-office-box",
        "locality",
        "region",
        "postal-code",
        "country-name",
        "label",
        "latitude",
        "longitude",
        "altitude",
        "name",
    )
)


def get_url(parsed):
    """Given a property value that may be a list of simple URLs or complex
    h-* dicts (with a url property), extract a list of URLs. This is useful
    when parsing e.g., in-reply-to.

    Args:
      mf (string or dict): URL or h-cite-style dict

    Returns:
      list: a list of URLs
    """

    urls = []
    for item in parsed["items"]:
        if isinstance(item, str):
            urls.append(item)
        elif isinstance(item, dict) and any(
            x.startswith("h-") for x in item.get("type", [])
        ):
            urls.extend(item.get("properties", {}).get("url", []))

    return urls


def find_first_entry(parsed, types):
    """Find the first interesting h-* object in BFS-order

    :param dict parsed: a mf2py parsed dict
    :param list types: target types, e.g. ['h-entry', 'h-event']
    :return: an mf2py item that is one of `types`, or None
    """
    return next(_find_all_entries(parsed, types, False), None)


def find_all_entries(parsed, types, include_properties=False):
    """Find all h-* objects of a given type in BFS-order. Traverses the
    top-level items and their children and descendents. Includes property
    values (e.g. finding all h-cards would not find values of
    "p-author h-card") only if `include_properties` is True.

    :param dict parsed: a mf2py parsed dict
    :param list types: target types, e.g. ['h-entry', 'h-event']
    :param boolean include_properties: include properties in search of entries
    :return: all entries with any of the the target types
    """
    return list(_find_all_entries(parsed, types, include_properties))


def _find_all_entries(parsed, types, include_properties):
    queue = collections.deque(item for item in parsed["items"])
    while queue:
        item = queue.popleft()
        if any(h_class in item.get("type", []) for h_class in types):
            yield item
        queue.extend(item.get("children", []))
        if include_properties:
            queue.extend(
                prop
                for props in item.get("properties", {}).values()
                for prop in props
                if isinstance(prop, dict)
            )


def find_datetimes(parsed):
    """Find published, updated, start, and end dates.

    :param dict parsed: a mf2py parsed dict
    :return: a dictionary from property type to datetime or date
    """
    hentry = find_first_entry(parsed)
    result = {}

    if hentry:
        for prop in ("published", "updated", "start", "end"):
            date_strs = hentry["properties"].get(prop, [])
            result[prop] = parse_dt(" ".join(date_strs))


def parse_dt(s):
    """The definition for microformats2 dt-* properties are fairly
    lenient.  This method converts an mf2 date string into either a
    datetime.date or datetime.datetime object. Datetimes will be naive
    unless a timezone is specified.

    :param str s: a mf2 string representation of a date or datetime
    :return: datetime.date or datetime.datetime
    :raises ValueError: if the string is not recognizable
    """

    if not s:
        return None

    s = re.sub(r"\s+", " ", s)
    date_re = r"(?P<year>\d{4,})-(?P<month>\d{1,2})-(?P<day>\d{1,2})"
    time_re = r"(?P<hour>\d{1,2}):(?P<minute>\d{2})(:(?P<second>\d{2})(\.(?P<microsecond>\d+))?)?"
    tz_re = r"(?P<tzz>Z)|(?P<tzsign>[+-])(?P<tzhour>\d{1,2}):?(?P<tzminute>\d{2})"
    dt_re = f"{date_re}((T| ){time_re} ?({tz_re})?)?$"

    m = re.match(dt_re, s)
    if not m:
        raise ValueError(f"unrecognized datetime {s}")

    year = m.group("year")
    month = m.group("month")
    day = m.group("day")

    hour = m.group("hour")

    if not hour:
        return datetime.date(int(year), int(month), int(day))

    minute = m.group("minute") or "00"
    second = m.group("second") or "00"

    if hour:
        dt = datetime.datetime(
            int(year), int(month), int(day), int(hour), int(minute), int(second)
        )
    if m.group("tzz"):
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    else:
        tzsign = m.group("tzsign")
        tzhour = m.group("tzhour")
        tzminute = m.group("tzminute") or "00"

        if tzsign and tzhour:
            offset = datetime.timedelta(hours=int(tzhour), minutes=int(tzminute))
            if tzsign == "-":
                offset = -offset
            dt = dt.replace(
                tzinfo=datetime.timezone(offset, f"{tzsign}{tzhour}:{tzminute}")
            )

    return dt


def get_plain_text(values, strip=True):
    """Get the first value in a list of values that we expect to be plain-text.
    If it is a dict, then return the value of "value".

    :param list values: a list of values
    :param boolean strip: true if we should strip the plaintext value
    :return: a string or None
    """
    if values:
        v = values[0]
        if isinstance(v, dict):
            v = v.get("value", "")
        if strip:
            v = v.strip()
        return v


def classify_comment(parsed, target_urls):
    """Find and categorize comments that reference any of a collection of
    target URLs. Looks for references of type reply, like, and repost.

    :param dict parsed: a mf2py parsed dict
    :param list target_urls: a collection of urls that represent the
      target post. this can include alternate or shortened URLs.
    :return: a list of applicable comment types ['like', 'reply', 'repost']
    """

    def process_references(objs, reftypes, result):
        for obj in objs:
            if isinstance(obj, dict):
                if any(
                    url in target_urls
                    for url in obj.get("properties", {}).get("url", [])
                ):
                    result += (r for r in reftypes if r not in result)
            elif obj in target_urls:
                result += (r for r in reftypes if r not in result)

    result = []
    hentry = find_first_entry(parsed, ["h-entry"])
    if hentry:
        reply_type = []
        if "rsvp" in hentry["properties"]:
            reply_type.append("rsvp")
        if "invitee" in hentry["properties"]:
            reply_type.append("invite")
        reply_type.append("reply")

        # TODO handle rel=in-reply-to
        for prop in ("in-reply-to", "reply-to", "reply"):
            process_references(hentry["properties"].get(prop, []), reply_type, result)

        for prop in ("like-of", "like"):
            process_references(hentry["properties"].get(prop, []), ("like",), result)

        for prop in ("repost-of", "repost"):
            process_references(hentry["properties"].get(prop, []), ("repost",), result)

    return result


def parse_author(obj):
    """Parse the value of a u-author property, can either be a compound
    h-card or a single name or url.

    :param object obj: the mf2 property value, either a dict or a string
    :result: a dict containing the author's name, photo, and url
    """
    result = {}
    if isinstance(obj, dict):
        names = obj["properties"].get("name")
        photos = obj["properties"].get("photo")
        urls = obj["properties"].get("url")
        if names:
            result["name"] = names[0]
        if photos:
            result["photo"] = photos[0]
        if urls:
            result["url"] = urls[0]
    elif obj:
        if obj.startswith("http://") or obj.startswith("https://"):
            result["url"] = obj
        else:
            result["name"] = obj
    return result


def find_author(parsed, source_url=None, hentry=None, fetch_mf2_func=None):
    """Use the authorship discovery algorithm
    https://indiewebcamp.com/authorship to determine an h-entry's
    author.

    :param dict parsed: an mf2py parsed dict.
    :param str source_url: the source of the parsed document.
    :param hentry dict: optional, the h-entry we're examining, if omitted,
        we'll just use the first one
    :param fetch_mf2_func callable: optional function that takes a URL
        and returns parsed mf2
    :return: a dict containing the author's name, photo, and url
    """

    def find_hentry_author(hentry):
        for obj in hentry["properties"].get("author", []):
            return parse_author(obj)

    def find_parent_hfeed_author(hentry):
        for hfeed in _find_all_entries(parsed, ["h-feed"], False):
            # find the h-entry's parent h-feed
            if hentry in hfeed.get("children", []):
                for obj in hfeed["properties"].get("author", []):
                    return parse_author(obj)

    if not hentry:
        hentry = find_first_entry(parsed, ["h-entry"])
        if not hentry:
            return None

    author_page = None

    # 3. if the h-entry has an author property, use that
    author = find_hentry_author(hentry)

    # 4. otherwise if the h-entry has a parent h-feed with author property,
    #    use that
    if not author:
        author = find_parent_hfeed_author(hentry)

    # 5. if an author property was found
    if author:
        # 5.2 otherwise if author property is an http(s) URL, let the
        #     author-page have that URL
        if list(author.keys()) == ["url"]:
            author_page = author["url"]
        # 5.1 if it has an h-card, use it, exit.
        # 5.3 otherwise use the author property as the author name,
        #     exit.
        else:
            return author

    # 6. if there is no author-page and the h-entry's page is a permalink page
    if not author_page:
        # 6.1 if the page has a rel-author link, let the author-page's
        #     URL be the href of the rel-author link
        rel_authors = parsed.get("rels", {}).get("author", [])
        if rel_authors:
            author_page = rel_authors[0]

    # 7. if there is an author-page URL
    if author_page:
        if not fetch_mf2_func:
            return {"url": author_page}

        # 7.1 get the author-page from that URL and parse it for microformats2
        parsed = fetch_mf2_func(author_page)
        hcards = find_all_entries(parsed, ["h-card"])

        # 7.2 if author-page has 1+ h-card with url == uid ==
        #     author-page's URL, then use first such h-card, exit.
        for hcard in hcards:
            hcard_url = get_plain_text(hcard["properties"].get("url"))
            hcard_uid = get_plain_text(hcard["properties"].get("uid"))
            if (
                hcard_url
                and hcard_uid
                and hcard_url == hcard_uid
                and hcard_url == author_page
            ):
                return parse_author(hcard)

        # 7.3 else if author-page has 1+ h-card with url property
        #     which matches the href of a rel-me link on the author-page
        #     (perhaps the same hyperlink element as the u-url, though not
        #     required to be), use first such h-card, exit.
        rel_mes = parsed.get("rels", {}).get("me", [])
        for hcard in hcards:
            hcard_url = get_plain_text(hcard["properties"].get("url"))
            if hcard_url and hcard_url in rel_mes:
                return parse_author(hcard)

        # 7.4 if the h-entry's page has 1+ h-card with url ==
        #     author-page URL, use first such h-card, exit.
        for hcard in hcards:
            hcard_url = get_plain_text(hcard["properties"].get("url"))
            if hcard_url and hcard_url == author_page:
                return parse_author(hcard)

        # 8. otherwise no deterministic author can be found.
        return None


def representative_hcard(parsed, source_url):
    """Find the representative h-card for a URL

    http://microformats.org/wiki/representative-h-card-parsing

    :param dict parsed: an mf2 parsed dict
    :param str source_url: the source of the parsed document.
    :return: the representative h-card if one is found
    """
    hcards = find_all_entries(parsed, ["h-card"], include_properties=True)
    # uid and url both match source_url
    for hcard in hcards:
        if source_url in hcard["properties"].get("uid", []) and source_url in hcard[
            "properties"
        ].get("url", []):
            return hcard
    # url that is also a rel=me
    for hcard in hcards:
        if any(
            url in parsed.get("rels", {}).get("me", [])
            for url in hcard["properties"].get("url", [])
        ):
            return hcard
    # single hcard with matching url
    found = None
    count = 0
    for hcard in hcards:
        if source_url in hcard["properties"].get("url", []):
            found = hcard
            count += 1
    if count == 1:
        return found


def convert_relative_paths_to_absolute(source_url, base_href, html):
    """Attempt to convert relative paths in foreign content
    to absolute based on the source url of the document. Useful for
    displaying images or links in reply contexts and comments.

    Gets list of tags/attributes from `URL_ATTRIBUTES`. Note that this
    function uses a regular expression to avoid adding a library
    dependency on a proper parser.

    :param str source_url: the source of the parsed document.
    :param str html: the text of the source document
    :return: the document with relative urls replaced with absolute ones
    """

    def do_convert(match):
        base_url = urljoin(source_url, base_href) if base_href else source_url
        return (
            match.string[match.start(0) : match.start(1)]
            + urljoin(base_url, match.group(1))
            + match.string[match.end(1) : match.end(0)]
        )

    if source_url:
        for tagname, attributes in URL_ATTRIBUTES.items():
            for attribute in attributes:
                pattern = re.compile(
                    rf"<{tagname}[^>]*?{attribute}\s*=\s*['\"](.*?)['\"]",
                    flags=re.DOTALL | re.MULTILINE | re.IGNORECASE,
                )
                html = pattern.sub(do_convert, html)

    return html


def is_name_a_title(name, content):
    """Determine whether the name property represents an explicit title.

    Typically when parsing an h-entry, we check whether p-name ==
    e-content (value). If they are non-equal, then p-name likely
    represents a title.

    However, occasionally we come across an h-entry that does not
    provide an explicit p-name. In this case, the name is
    automatically generated by converting the entire h-entry content
    to plain text. This definitely does not represent a title, and
    looks very bad when displayed as such.

    To handle this case, we broaden the equality check to see if
    content is a subset of name. We also strip out non-alphanumeric
    characters just to make the check a little more forgiving.

    :param str name: the p-name property that may represent a title
    :param str content: the plain-text version of an e-content property
    :return: True if the name likely represents a separate, explicit title
    """

    def normalize(s):
        if not isinstance(s, str):
            s = s.decode("utf-8")
        s = unicodedata.normalize("NFKD", s)
        s = s.lower()
        s = re.sub("[" + string.whitespace + string.punctuation + "]", "", s)
        return s

    if not content:
        return True
    if not name:
        return False
    return normalize(content) not in normalize(name)


def post_type_discovery(hentry):
    """Implementation of the post-type discovery algorithm
    defined here https://indiewebcamp.com/post-type-discovery#Algorithm

    :param dict hentry: mf2 item representing the entry to test

    :return: string, one of: 'org', 'person', 'event', 'rsvp',
                     'invite', 'reply', 'repost', 'like', 'photo',
                     'article', 'note', 'follow'

    """
    props = hentry.get("properties", {})
    if "h-card" in hentry.get("type", []):
        name = get_plain_text(props.get("name"))
        org = get_plain_text(props.get("org"))
        if name and org and name == org:
            return "org"
        return "person"

    if "h-event" in hentry.get("type", []):
        return "event"

    for prop, implied_type in [
        ("rsvp", "rsvp"),
        ("invitee", "invite"),
        ("in-reply-to", "reply"),
        ("repost-of", "repost"),
        ("like-of", "like"),
        ("follow-of", "follow"),
        ("photo", "photo"),
    ]:
        if props.get(prop) is not None:
            return implied_type
    # check name ~= content
    name = get_plain_text(props.get("name"))
    content = get_plain_text(props.get("content"))
    if not content:
        content = get_plain_text(props.get("summary"))
    if content and name and is_name_a_title(name, content):
        return "article"
    return "note"


def _interpret_common_properties(
    parsed,
    source_url,
    base_href,
    hentry,
    use_rel_syndication,
    want_json,
    fetch_mf2_func,
):
    result = {}
    props = hentry["properties"]

    for prop in ("url", "uid", "photo", "featured" "logo"):
        value = get_plain_text(props.get(prop))
        if value:
            result[prop] = value

    for prop in ("start", "end", "published", "updated", "deleted"):
        date_str = get_plain_text(props.get(prop))
        if date_str:
            if want_json:
                result[prop] = date_str
            else:
                result[prop + "-str"] = date_str
                try:
                    date = parse_dt(date_str)
                    if date:
                        result[prop] = date
                except ValueError:
                    raise ValueError(f"Failed to parse datetime {date_str}")

    author = find_author(parsed, source_url, hentry, fetch_mf2_func)
    if author:
        result["author"] = author

    content_prop = props.get("content")
    content_value = None
    if content_prop:
        if isinstance(content_prop[0], dict):
            content_html = content_prop[0].get("html", "").strip()
            content_value = content_prop[0].get("value", "").strip()
        else:
            content_value = content_html = content_prop[0]
        result["content"] = convert_relative_paths_to_absolute(
            source_url, base_href, content_html
        )
        result["content-plain"] = content_value

    summary_prop = props.get("summary")
    if summary_prop:
        if isinstance(summary_prop[0], dict):
            result["summary"] = summary_prop[0]["value"]
        else:
            result["summary"] = summary_prop[0]

    # Collect location objects, then follow this algorithm to consolidate their
    # properties:
    # https://indieweb.org/location#How_to_determine_the_location_of_a_microformat
    location_stack = [props]

    for prop in "location", "adr":
        vals = props.get(prop)
        if vals:
            if isinstance(vals[0], str):
                location_stack.append({"name": vals})
            else:
                location_stack.append(vals[0].get("properties", {}))

    geo = props.get("geo")
    if geo:
        if isinstance(geo[0], dict):
            location_stack.append(geo[0].get("properties", {}))
        else:
            if geo[0].startswith("geo:"):
                # a geo: URL. try to parse it. https://tools.ietf.org/html/rfc5870
                parts = geo[0][len("geo:") :].split(";")[0].split(",")
                if len(parts) >= 2:
                    location_stack.append(
                        {
                            "latitude": [parts[0]],
                            "longitude": [parts[1]],
                            "altitude": [parts[2]] if len(parts) >= 3 else [],
                        }
                    )

    for prop in LOCATION_PROPERTIES:
        for obj in location_stack:
            if obj and obj.get(prop) and not (obj == props and prop == "name"):
                result.setdefault("location", {})[prop] = obj[prop][0]

    if use_rel_syndication:
        result["syndication"] = list(
            set(
                parsed.get("rels", {}).get("syndication", [])
                + hentry["properties"].get("syndication", [])
            )
        )
    else:
        result["syndication"] = hentry["properties"].get("syndication", [])

    return result


def interpret_event(
    parsed,
    source_url,
    base_href=None,
    hevent=None,
    use_rel_syndication=True,
    want_json=False,
    fetch_mf2_func=None,
):
    """Given a document containing an h-event, return a dictionary::

        {
         'type': 'event',
         'url': the permalink url of the document (may be different than source_url),
         'start': datetime or date,
         'end': datetime or date,
         'name': plain-text event name,
         'content': body of event description (contains HTML)
        }

    :param dict parsed: the result of parsing a document containing mf2 markup
    :param str source_url: the URL of the parsed document, not currently used
    :param str base_href: (optional) the href value of the base tag
    :param dict hevent: (optional) the item in the above document representing
      the h-event. if provided, we can avoid a redundant call to
      find_first_entry
    :param boolean use_rel_syndication: (optional, default True) Whether
      to include rel=syndication in the list of syndication sources. Sometimes
      useful to set this to False when parsing h-feeds that erroneously include
      rel=syndication on each entry.
    :param boolean want_json: (optional, default false) if true, the result
      will be pure json with datetimes as strings instead of python objects
    :param callable fetch_mf2_func: (optional) function to fetch mf2 parsed
      output for a given URL.
    :return: a dict with some or all of the described properties
    """
    # find the h-event if it wasn't provided
    if not hevent:
        hevent = find_first_entry(parsed, ["h-event"])
        if not hevent:
            return {}

    result = _interpret_common_properties(
        parsed,
        source_url,
        base_href,
        hevent,
        use_rel_syndication,
        want_json,
        fetch_mf2_func,
    )
    result["type"] = "event"
    name_value = get_plain_text(hevent["properties"].get("name"))
    if name_value:
        result["name"] = name_value
    return result


def interpret_entry(
    parsed,
    source_url,
    base_href=None,
    hentry=None,
    use_rel_syndication=True,
    want_json=False,
    fetch_mf2_func=None,
):
    """Given a document containing an h-entry, return a dictionary::

        {
         'type': 'entry',
         'url': the permalink url of the document (may be different than source_url),
         'published': datetime or date,
         'updated': datetime or date,
         'name': title of the entry,
         'content': body of entry (contains HTML),
         'author': {
          'name': author name,
          'url': author url,
          'photo': author photo
         },
         'syndication': [
           'syndication url',
           ...
         ],
         'in-reply-to': [...],
         'like-of': [...],
         'repost-of': [...],
        }

    :param dict parsed: the result of parsing a document containing mf2 markup
    :param str source_url: the URL of the parsed document, used by the
      authorship algorithm
    :param str base_href: (optional) the href value of the base tag
    :param dict hentry: (optional) the item in the above document
      representing the h-entry. if provided, we can avoid a redundant
      call to find_first_entry
    :param boolean use_rel_syndication: (optional, default True) Whether
      to include rel=syndication in the list of syndication sources. Sometimes
      useful to set this to False when parsing h-feeds that erroneously include
      rel=syndication on each entry.
    :param boolean want_json: (optional, default False) if true, the result
      will be pure json with datetimes as strings instead of python objects
    :param callable fetch_mf2_func: (optional) function to fetch mf2 parsed
      output for a given URL.
    :return: a dict with some or all of the described properties
    """

    # find the h-entry if it wasn't provided
    if not hentry:
        hentry = find_first_entry(parsed, ["h-entry"])
        if not hentry:
            return {}

    result = _interpret_common_properties(
        parsed,
        source_url,
        base_href,
        hentry,
        use_rel_syndication,
        want_json,
        fetch_mf2_func,
    )
    if "h-cite" in hentry.get("type", []):
        result["type"] = "cite"
    else:
        result["type"] = "entry"

    title = get_plain_text(hentry["properties"].get("name"))
    if title and is_name_a_title(title, result.get("content-plain")):
        result["name"] = title

    for prop in (
        "in-reply-to",
        "like-of",
        "repost-of",
        "bookmark-of",
        "comment",
        "like",
        "repost",
    ):
        for url_val in hentry["properties"].get(prop, []):
            if isinstance(url_val, dict):
                result.setdefault(prop, []).append(
                    interpret(
                        parsed,
                        source_url,
                        base_href,
                        url_val,
                        use_rel_syndication=False,
                        want_json=want_json,
                        fetch_mf2_func=fetch_mf2_func,
                    )
                )
            else:
                result.setdefault(prop, []).append(
                    {
                        "url": url_val,
                    }
                )

    return result


def interpret_feed(
    parsed, source_url, base_href=None, hfeed=None, want_json=False, fetch_mf2_func=None
):
    """Interpret a source page as an h-feed or as an top-level collection
    of h-entries.

    :param dict parsed: the result of parsing a mf2 document
    :param str source_url: the URL of the source document (used for authorship
        discovery)
    :param str base_href: (optional) the href value of the base tag
    :param dict hfedd: (optional) the h-feed to be parsed. If provided,
        this will be used instead of the first h-feed on the page.
    :param callable fetch_mf2_func: (optional) function to fetch mf2 parsed
      output for a given URL.
    :return: a dict containing 'entries', a list of entries, and possibly other
        feed properties (like 'name').
    """
    result = {}
    # find the first feed if it wasn't provided
    if not hfeed:
        hfeed = find_first_entry(parsed, ["h-feed"])

    if hfeed:
        names = hfeed["properties"].get("name")
        if names:
            result["name"] = names[0]
        children = hfeed.get("children", [])
    # just use the top level 'items' as the feed children
    else:
        children = parsed.get("items", [])

    entries = []
    for child in children:
        entry = interpret(
            parsed,
            source_url,
            base_href,
            item=child,
            use_rel_syndication=False,
            want_json=want_json,
            fetch_mf2_func=fetch_mf2_func,
        )
        if entry:
            entries.append(entry)
    result["entries"] = entries
    return result


def interpret(
    parsed,
    source_url,
    base_href=None,
    item=None,
    use_rel_syndication=True,
    want_json=False,
    fetch_mf2_func=None,
):
    """Interpret a permalink of unknown type. Finds the first interesting
    h-* element, and delegates to :func:`interpret_entry` if it is an
    h-entry or :func:`interpret_event` for an h-event

    :param dict parsed: the result of parsing a mf2 document
    :param str source_url: the URL of the source document (used for authorship
      discovery)
    :param str base_href: (optional) the href value of the base tag
    :param dict item: (optional) the item to be parsed. If provided,
      this will be used instead of the first element on the page.
    :param boolean use_rel_syndication: (optional, default True) Whether
      to include rel=syndication in the list of syndication sources. Sometimes
      useful to set this to False when parsing h-feeds that erroneously include
      rel=syndication on each entry.
    :param boolean want_json: (optional, default False) If true, the result
      will be pure json with datetimes as strings instead of python objects
    :param callable fetch_mf2_func: (optional) function to fetch mf2 parsed
      output for a given URL.
    :return: a dict as described by interpret_entry or interpret_event, or None
    """
    if not item:
        item = find_first_entry(parsed, ["h-entry", "h-event"])

    if item:
        types = item.get("type", [])
        if "h-event" in types:
            return interpret_event(
                parsed,
                source_url,
                base_href=base_href,
                hevent=item,
                use_rel_syndication=use_rel_syndication,
                want_json=want_json,
                fetch_mf2_func=fetch_mf2_func,
            )
        elif "h-entry" in types or "h-cite" in types:
            return interpret_entry(
                parsed,
                source_url,
                base_href=base_href,
                hentry=item,
                use_rel_syndication=use_rel_syndication,
                want_json=want_json,
                fetch_mf2_func=fetch_mf2_func,
            )


def interpret_comment(
    parsed,
    source_url,
    target_urls,
    base_href=None,
    want_json=False,
    fetch_mf2_func=None,
):
    """Interpret received webmentions, and classify as like, reply, or
    repost (or a combination thereof). Returns a dict as described
    in :func:`interpret_entry`, with the additional fields::

        {
         'comment_type': a list of strings, zero or more of
                         'like', 'reply', or 'repost'
         'rsvp': a string containing the rsvp response (optional)
        }

    :param dict parsed: a parsed mf2 parsed document
    :param str source_url: the URL of the source document
    :param list target_urls: a collection containing the URL of the target\
      document, and any alternate URLs (e.g., shortened links) that should\
      be considered equivalent when looking for references
    :param str base_href: (optional) the href value of the base tag
    :param boolean want_json: (optional, default False) If true, the result
      will be pure json with datetimes as strings instead of python objects
    :param callable fetch_mf2_func: (optional) function to fetch mf2 parsed
      output for a given URL.
    :return: a dict as described above, or None
    """
    item = find_first_entry(parsed, ["h-entry"])
    if item:
        result = interpret_entry(
            parsed,
            source_url,
            base_href=base_href,
            hentry=item,
            want_json=want_json,
            fetch_mf2_func=fetch_mf2_func,
        )
        if result:
            result["comment_type"] = classify_comment(parsed, target_urls)
            rsvp = get_plain_text(item["properties"].get("rsvp"))
            if rsvp:
                result["rsvp"] = rsvp.lower()

            invitees = item["properties"].get("invitee")
            if invitees:
                result["invitees"] = [parse_author(inv) for inv in invitees]

        return result


# ===========================================================================


stable = {
    "adr": [
        "p-street-address",
        "p-extended-address",
        "p-post-office-box",
        "p-locality",
        "p-region",
        "p-postal-code",
        "p-country-name",
        "p-label",
        "p/u-geo",
        "p-latitude",
        "p-longitude",
        "p-altitude",
    ],
    "card": [
        "p-name",
        "p-honorific-prefix",
        "p-given-name",
        "p-additional-name",
        "p-family-name",
        "p-sort-string",
        "p-honorific-suffix",
        "p-nickname",
        "u-email",
        "u-logo",
        "u-photo",
        "u-url",
        "u-uid",
        "p-category",
        "p/h-adr",
        "p-post-office-box",
        "p-extended-address",
        "p-street-address",
        "p-locality",
        "p-region",
        "p-postal-code",
        "p-country-name",
        "p-label",
        "p/u/h-geo",
        "p-latitude",
        "p-longitude",
        "p-altitude",
        "p-tel",
        "p-note",
        "dt-bday",
        "u-key",
        "p-org",
        "p-job-title",
        "p-role",
        "u-impp",
        "p-sex",
        "p-gender-identity",
        "dt-anniversary",
    ],
    "entry": [
        "p-name",
        "p-summary",
        "e-content",
        "dt-published",
        "dt-updated",
        "p-author",
        "p-category",
        "u-url",
        "u-uid",
        "p-location",
        "u-syndication",
        "u-in-reply-to",
        "p-rsvp",
        "u-like-of",
        "u-repost-of",
    ],
    "event": [
        "p-name",
        "p-summary",
        "dt-start",
        "dt-end",
        "dt-duration",
        "e-content",
        "u-url",
        "p-category",
        "p-location(card/adr/geo)",
        "[p-attendee]",
    ],
    "feed": ["p-name", "p-author(card)", "u-url", "u-photo"],
    "geo": ["p-latitude", "p-longitude", "p-altitude"],
    "item": ["p-name", "u-url", "u-photo"],
    "product": [
        "p-name",
        "u-photo",
        "p-brand(card)",
        "p-category",
        "e-content",
        "u-url",
        "u-identifier",
        "p-review(review)",
        "p-price",
    ],
    "recipe": [
        "p-name",
        "p-ingredient",
        "p-yield",
        "e-instructions",
        "dt-duration",
        "u-photo",
        "p-summary",
        "p-author(card)",
        "dt-published",
        "p-nutrition",
        "p-category",
    ],
    "resume": [
        "p-name",
        "p-summary",
        "p-contact",
        "p-education(event+card)",
        "p-experience(event+card)",
        "p-skill",
        "p-affiliation",
    ],
    "review": [
        "p-name ",
        "p-item(card/event/adr/geo/product/item)",
        "p-author(card)",
        "dt-published",
        "p-rating",
        "p-best",
        "p-worst",
        "e-content",
        "p-category",
        "u-url",
    ],
    "review-aggregate": [
        "p-item(card/event/adr/geo/product/item)",
        "p-average",
        "p-best",
        "p-worst",
        "p-count",
        "p-votes",
        "p-name",
    ],
}
draft = {"app": ["p-name", "u-url", "u-logo", "u-photo"]}


def representative_card(mf2json: dict, source_url: str) -> dict:
    """
    Return the representative card for given parsed document.

    http://microformats.org/wiki/representative-h-card-parsing

    """
    source = easyuri.parse(source_url).minimized
    cards = [
        card
        for card in _get_all_items(mf2json, ["h-card"], include_props=True)
        if (
            card["properties"].get("name", [""])[0]
            or card["properties"].get("nickname", [""])[0]
        )
    ]
    if match := _check_uid_and_url_match_source_url(cards, source):
        return match
    if match := _check_url_matches_rel_me(cards, mf2json):
        return match
    if match := _check_url_matches_source_url(cards, source):
        return match
    return {}


def _check_uid_and_url_match_source_url(cards, source_url):  # FIXME same as below?
    """"""
    for card in cards:
        if source_url in _get_normalized_urls(
            card, "uid"
        ) and source_url in _get_normalized_urls(card, "url"):
            return card["properties"]


def _check_url_matches_rel_me(cards, parsed):
    """"""
    for card in cards:
        rel_mes = set()
        for rel_me in parsed.get("rels", {}).get("me", []):
            try:
                rel_me = easyuri.parse(rel_me)
            except ValueError:
                continue
            if isinstance(rel_me, (easyuri.HTTPURI, easyuri.HTTPSURI)):
                rel_mes.add(rel_me.minimized)
        if any(url in rel_mes for url in _get_normalized_urls(card, "url")):
            return card["properties"]


def _check_url_matches_source_url(cards, source_url):  # FIXME same as above?
    """"""
    found = []
    count = 0
    for card in cards:
        # if source_url in card['properties'].get('url', []):
        for card_url in _get_normalized_urls(card, "url"):
            if card_url.rstrip("/") == source_url:
                found.append(card)
                count += 1
    if count:
        return found[0]["properties"]


def representative_feed(mf2json: dict, source_url: str, source_dom=None):
    """
    Return the representative feed for given parsed document.

    https://indieweb.org/feed#How_To_Consume
    https://microformats.org/wiki/h-feed#Discovery

    """
    feed = {}
    try:
        feed["name"] = source_dom.select("title")[0].text
    except (AttributeError, IndexError):
        pass
    if author := representative_card(mf2json, source_url):
        feed["author"] = author
    items = []
    if first_feed := _get_first_item(mf2json, ["h-feed"]):
        if name := first_feed["properties"].get("name"):
            feed["name"] = [name]
        if authors := first_feed["properties"].get("author"):
            feed["author"] = []
            for author in authors:
                author["properties"]["type"] = author["type"]
                feed["author"].append(author["properties"])
        if children := first_feed["children"]:
            items = children
    else:
        items = _get_all_items(mf2json, ["h-entry", "h-event"])
    feed["items"] = []
    for item in items:
        if item.get("source") == "metaformats":
            continue
        item["properties"]["type"] = item["type"]
        feed["items"].append(item["properties"])
    if rel_next := mf2json["rels"].get("next"):
        feed["next"] = rel_next[0]
    if rel_prev := mf2json["rels"].get("prev"):
        feed["prev"] = rel_prev[0]
    return feed


def discover_post_type(properties):
    """
    Return the discovered post type.

    http://ptd.spec.indieweb.org/#x5-post-type-algorithm

    """
    type_specific_properties = {
        "rsvp": "rsvp",
        "repost-of": "repost",  # aka share
        "like-of": "like",  # aka favorite
        "in-reply-to": "reply",
        "listen-of": "listen",
        "bookmark-of": "bookmark",
        "checkin": "check-in",
        "video": "video",
        "audio": "audio",
        "photo": "photo",
        # TODO "checkin": "checkin",
        # TODO "bookmark-of": "bookmark",
        # TODO "follow-of": "follow",
        # TODO "weight": "weight",
    }
    for type_specific_property, post_type in type_specific_properties.items():
        if type_specific_property in properties:
            if (
                post_type in ("video", "audio", "photo")
                and "quotation-of" in properties
            ):
                return f"{post_type}/clip"
            return post_type
    content = ""
    try:
        content = _get_first_non_empty(properties["content"])
    except KeyError:
        try:
            content = _get_first_non_empty(properties["summary"])
        except KeyError:
            return "note"
    name = ""
    try:
        name = _get_first_non_empty(properties["name"])
    except KeyError:
        return "note"
    if name:
        try:
            content = dict(content)
        except ValueError:
            text_content = content
        else:
            text_content = bs4.BeautifulSoup(content["html"].strip()).text
        if not text_content.startswith(name):
            return "article"
    return "note"


def _get_first_item(mf2json: dict, item_type: set):
    """Return the first object(s) of given item_type(s) (eg. h-entry, h-event)."""
    return next(_yield_all_items(mf2json, item_type, False), None)


def _get_all_items(mf2json: dict, item_type: set, include_props=False):
    """Return all object(s) of given item_type(s) (eg. h-entry, h-event)."""
    return list(_yield_all_items(mf2json, item_type, include_props))


def _yield_all_items(mf2json: dict, item_type: set, include_props: bool):
    """
    Yield objects(s) of given item_type(s) in breadth first search.

    Traverses the top-level items and their children and descendents.
    Includes property values (e.g. finding all h-cards would not find
    values of "p-author h-card") only if `include_props` is True.

    """
    queue = collections.deque(item for item in mf2json["items"])
    while queue:
        item = queue.popleft()
        if any(h_class in item.get("type", []) for h_class in item_type):
            yield item
        queue.extend(item.get("children", []))
        if include_props:
            queue.extend(
                prop
                for props in item.get("properties", {}).values()
                for prop in props
                if isinstance(prop, dict)
            )


def _get_normalized_urls(card, prop):
    """Return a list of normalized URLs for an card's prop (uid/url)."""
    urls = []
    for url in card["properties"].get(prop, []):
        try:
            urls.append(easyuri.parse(url).minimized)
        except ValueError:
            pass
    return urls


def _get_first_non_empty(propval):
    """
    Return the first non-empty value in `propval`.

    If `propval` is not a list and non-empty, return it.

    """
    if not isinstance(propval, list):
        propval = [propval]
    for content in propval:
        if content:
            return content
