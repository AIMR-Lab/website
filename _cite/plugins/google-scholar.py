import os
from serpapi import GoogleSearch
from util import *


def main(entry):
    """
    receives single list entry from google-scholar data file
    returns list of sources to cite
    """

    # get api key (serp api key to access google scholar)
    api_key = "e9dbc6276c9333fc24641b295d41b6ebb451073846de103291ea79c6c1aeb700" #VERY FLAWED
    #os.environ.get("GOOGLE_SCHOLAR_API_KEY", "")
    if not api_key:
        raise Exception('No "GOOGLE_SCHOLAR_API_KEY" env var')

    # serp api properties
    params = {
        "engine": "google_scholar_author",
        "api_key": api_key,
        "num": 100,  # max allowed
    }

    # get id from entry
    _id = get_safe(entry, "gsid", "")
    if not _id:
        raise Exception('No "gsid" key')

    # query api
    @log_cache
    @cache.memoize(name=__file__, expire=1 * (60 * 60 * 24))
    def query(_id):
        params["author_id"] = _id
        return get_safe(GoogleSearch(params).get_dict(), "articles", [])

    response = query(_id)

    # list of sources to return
    sources = []

    # go through response and format sources
    # Go through response and format sources
    for work in response:
        year = get_safe(work, "year", "")
        try:
            source = {
                "id": get_safe(work, "citation_id", ""),
                "title": get_safe(work, "title", ""),
                "authors": list(map(str.strip, get_safe(work, "authors", "").split(","))),
                "publisher": get_safe(work, "publication", ""),
                "date": (year + "-01-01") if year else "",
                "link": get_safe(work, "link", ""),
            }

            # Ensure Manubot-citeable id is present
            if not source["id"].startswith(("doi:", "pubmed:", "arxiv:", "pmc:")):
                raise NotImplementedError("Manubot cannot generate a csl_item for this id.")

            # Add source to the list
            sources.append(source)

        except NotImplementedError:
            # Fallback: Generate a simplified citation directly from metadata
            fallback_source = {
                "id": get_safe(work, "citation_id", ""),
                "title": get_safe(work, "title", "Unknown Title"),
                "authors": list(map(str.strip, get_safe(work, "authors", "Unknown Authors").split(","))),
                "publisher": get_safe(work, "publication", "Unknown Publisher"),
                "date": (year + "-01-01") if year else "",
                "link": get_safe(work, "link", ""),
                "description": "This citation was generated directly from Google Scholar metadata.",
            }
            print(f"Using fallback for non-standard citation: {fallback_source['id']}")
            sources.append(fallback_source)

    return sources
