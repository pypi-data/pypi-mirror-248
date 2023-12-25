import logging
import math

from django.urls import reverse

from . import cts
from .conf import settings


logger = logging.getLogger(__name__)


def link_collection(urn) -> dict:
    return {
        "url": reverse("library_collection", kwargs={"urn": urn}),
        "json_url": reverse("api:library_collection", kwargs={"urn": urn}),
        "text_url": reverse("api:library_passage_text", kwargs={"urn": urn}),
    }


def link_passage(urn) -> dict:
    return {
        "url": reverse("reader", kwargs={"urn": urn}),
        "json_url": reverse("api:library_passage", kwargs={"urn": urn}),
        "text_url": reverse("api:library_passage_text", kwargs={"urn": urn}),
    }


def apify(obj, **kwargs):
    remaining = obj.as_json(**kwargs)
    rels = {}
    if isinstance(obj, cts.TextGroup):
        works = remaining.pop("works")
        rels = {
            "works": [
                {
                    **link_collection(work["urn"]),
                    **work,
                    "texts": [
                        {**link_collection(text["urn"]), **text}
                        for text in work["texts"]
                    ],
                }
                for work in works
            ]
        }
    if isinstance(obj, cts.Work):
        texts = remaining.pop("texts")
        rels = {"texts": [{**link_collection(text["urn"]), **text} for text in texts]}
    if isinstance(obj, cts.Text):
        if kwargs.get("with_toc", False):
            first_passage = remaining.pop("first_passage")
            ancestors = remaining.pop("ancestors")
            toc = remaining.pop("toc")
            rels = {
                "first_passage": {
                    **link_passage(first_passage["urn"]),
                    **first_passage,
                },
                "ancestors": [
                    {**link_collection(ancestor["urn"]), **ancestor}
                    for ancestor in ancestors
                ],
                "toc": [{**link_passage(entry["urn"]), **entry} for entry in toc],
            }
        else:
            rels = {}
    if isinstance(obj, cts.Collection):
        links = link_collection(str(obj.urn))
        if isinstance(obj, cts.Text):
            links.update(
                {
                    "reader_url": reverse(
                        "library_text_redirect", kwargs={"urn": obj.urn}
                    )
                }
            )
    if isinstance(obj, cts.Passage):
        links = link_passage(str(obj.urn))
        text = remaining.pop("text")
        text_ancestors = text.pop("ancestors")
        rels = {
            "text": {
                **link_collection(text["urn"]),
                "ancestors": [
                    {**link_collection(ancestor["urn"]), **ancestor}
                    for ancestor in text_ancestors
                ],
                **text,
            }
        }
    return {**links, **rels, **remaining}


def encode_link_header(lo: dict):
    links = []
    for rel, attrs in lo.items():
        link = []
        link.append(f"<{attrs.pop('target')}>")
        for k, v in {"rel": rel, **attrs}.items():
            link.append(f'{k}="{v}"')
        links.append("; ".join(link))
    return ", ".join(links)


def get_pagination_info(total_count, page_num):
    num_pages = int(math.ceil(total_count / 10))
    has_previous = False
    if page_num > 1:
        has_previous = True
    has_next = False
    if page_num < num_pages:
        has_next = True
    end_index = page_num * 10
    if page_num == num_pages:
        end_index = total_count
    return {
        "number": page_num,
        "start_index": (page_num * 10) - 9,
        "end_index": end_index,
        "has_previous": has_previous,
        "has_next": has_next,
        "num_pages": num_pages,
    }


def normalize_urn(urn):
    if not settings.SCAIFE_VIEWER_CORE_ALLOW_TRAILING_COLON and urn.endswith(":"):
        new_urn = urn[:-1]
        msg = f'Normalized "{urn}" to "{new_urn}"'
        logger.info(msg)
        return new_urn
    return urn
