import datetime
import json
import os
from pathlib import Path
from urllib.parse import urlencode

from django.http import (
    Http404,
    HttpResponse,
    HttpResponseBadRequest,
    JsonResponse,
)
from django.shortcuts import redirect, render
from django.utils.safestring import SafeString
from django.views import View
from django.views.generic.base import TemplateView

import dateutil.parser
import requests
from MyCapytain.common.constants import Mimetypes

import yaml

from . import cts
from .conf import settings
from .cts.capitains import default_resolver
from .cts.reference import URN
from .hooks import hookset
from .http import ConditionMixin
from .precomputed import library_view_json
from .search import SearchQuery
from .utils import (
    apify,
    encode_link_header,
    get_pagination_info,
    link_passage,
    normalize_urn,
)


class BaseLibraryView(View):

    format = "html"

    def get(self, request, **kwargs):
        to_response = {"html": self.as_html, "json": self.as_json}.get(
            self.format, "html"
        )
        return to_response()


class LibraryConditionMixin(ConditionMixin):
    def get_last_modified(self, request, *args, **kwargs):
        # @@@ per-URN modification dates will need nautilus-cnd
        # for now, use only deployment creation timestamp.
        last_modified = datetime.datetime.utcnow()
        deployment_timestamp = os.environ.get(settings.DEPLOYMENT_TIMESTAMP_VAR_NAME)
        if deployment_timestamp:
            last_modified = dateutil.parser.parse(deployment_timestamp)
        return last_modified


class LibraryView(LibraryConditionMixin, BaseLibraryView):
    def as_html(self):
        return render(self.request, "library/index.html", {})

    def as_json(self):
        data = library_view_json()
        return JsonResponse(data)


class LibraryInfoView(View):
    def get(self, request, **kwargs):
        payload = {"api_version": settings.LIBRARY_VIEW_API_VERSION}
        return JsonResponse(payload)


class LibraryCollectionView(LibraryConditionMixin, BaseLibraryView):
    def validate_urn(self):
        if not self.kwargs["urn"].startswith("urn:"):
            raise Http404()

    def get_collection(self):
        self.validate_urn()
        try:
            return cts.collection(self.kwargs["urn"])
        except cts.CollectionDoesNotExist:
            raise Http404()

    @property
    def collection_is_version_exemplar(self):
        return len(str(self.collection.urn).rsplit(".")) > 2

    @property
    def should_redirect_to_reader(self):
        if settings.SCAIFE_VIEWER_CORE_REDIRECT_VERSION_LIBRARY_COLLECTION_TO_READER:
            return self.collection_is_version_exemplar and self.format == "html"
        return False

    def get(self, request, **kwargs):
        self.collection = self.get_collection()
        if self.should_redirect_to_reader:
            return library_text_redirect(request, self.kwargs["urn"])
        return super().get(request, **kwargs)

    def as_html(self):
        normalized_urn = normalize_urn(self.kwargs["urn"])
        if normalized_urn != self.kwargs["urn"]:
            return redirect("library_collection", urn=normalized_urn)

        collection = self.collection
        collection_name = collection.__class__.__name__.lower()
        ctx = {collection_name: collection}
        return render(self.request, f"library/cts_{collection_name}.html", ctx)

    def should_toc(self, collection_obj):
        """
        Only invoke TOC when the collection is a Text.
        """
        return isinstance(collection_obj, cts.Text)

    @property
    def json_paylod(self):
        collection = self.collection
        if self.should_toc:
            return apify(collection, with_toc=True)
        return apify(collection)

    def as_json(self):
        try:
            return JsonResponse(self.json_paylod)
        except ValueError as e:
            """
            TODO: good idea to refactor this to send back consistent error
            messages and codes that the client is aware of

            Example 1:

              {
                "error_code": 1,
                "msg": "Malformed XML"
              }

            Example 2:
              {
                "error_code": 2,
                "msg": "Invalid refsDecl"
              }
            """
            return JsonResponse({"error": str(e)}, status=500)


class LibraryCollectionVectorView(LibraryConditionMixin, View):
    def get(self, request, urn):
        entries = request.GET.getlist("e[]")
        try:
            cts.collection(urn)
        except cts.CollectionDoesNotExist:
            raise Http404()
        collections = {}
        for entry in entries:
            collection = cts.collection(f"{urn}.{entry}")
            collections[str(collection.urn)] = apify(collection)
        payload = {"collections": collections}
        return JsonResponse(payload)


class LibraryPassageView(LibraryConditionMixin, View):

    format = "json"

    def get(self, request, **kwargs):
        try:
            passage, healed = self.get_passage()
        except cts.InvalidPassageReference as e:
            return HttpResponse(
                json.dumps({"reason": str(e)}),
                status=400,
                content_type="application/json",
            )
        except cts.InvalidURN as e:
            return HttpResponse(
                json.dumps({"reason": str(e)}),
                status=404,
                content_type="application/json",
            )
        if healed:
            key = {"json": "json_url", "text": "text_url"}.get(self.format, "json")
            redirect = HttpResponse(status=303)
            redirect["Location"] = link_passage(str(passage.urn))[key]
            return redirect
        self.passage = passage
        to_response = {
            "json": self.as_json,
            "text": self.as_text,
            "xml": self.as_xml,
        }.get(self.format, "json")
        return to_response()

    def get_passage(self):
        urn = self.kwargs["urn"]
        try:
            return cts.passage_heal(urn)
        except cts.PassageDoesNotExist:
            raise Http404()

    def as_json(self):
        lo = {}
        prev, nxt = self.passage.prev(), self.passage.next()
        if prev:
            lo["prev"] = {
                "target": link_passage(str(prev.urn))["url"],
                "urn": str(prev.urn),
            }
        if nxt:
            lo["next"] = {
                "target": link_passage(str(nxt.urn))["url"],
                "urn": str(nxt.urn),
            }
        response = JsonResponse(apify(self.passage))
        if lo:
            response["Link"] = encode_link_header(lo)
        return response

    def as_text(self):
        return HttpResponse(
            f"{self.passage.content}\n", content_type="text/plain; charset=utf-8"
        )

    def as_xml(self):
        return HttpResponse(f"{self.passage.xml}", content_type="application/xml")


class Reader(TemplateView):

    template_name = "reader/reader.html"

    def get(self, request, *args, **kwargs):
        self.urn = cts.URN(self.kwargs["urn"])
        if not self.urn.reference:
            return redirect("library_text_redirect", urn=self.kwargs["urn"])
        return super().get(request, *args, **kwargs)

    def get_text(self):
        try:
            text = cts.collection(self.urn.upTo(cts.URN.NO_PASSAGE))
        except cts.CollectionDoesNotExist:
            raise Http404()
        return text

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["text"] = self.get_text()
        return context


def library_text_redirect(request, urn):
    """
    Given a text URN redirect to the first chunk. Required to prevent
    TOCing on the top-level library page.
    """
    urn = normalize_urn(urn)

    try:
        text = cts.collection(urn)
    except cts.CollectionDoesNotExist:
        raise Http404()
    if not isinstance(text, cts.Text):
        return redirect("library_collection", urn=urn)
    passage = text.first_passage()
    if not passage:
        raise Http404()
    return redirect("reader", urn=passage.urn)


def search(request):
    return render(request, "search.html")


def search_json(request):

    # get params from query string
    search_type = request.GET.get("type")
    q = request.GET.get("q", "")
    kind = request.GET.get("kind", "form")
    size = int(request.GET.get("size", "10"))
    text_group_urn = request.GET.get("text_group")
    work_urn = request.GET.get("work")

    # validate params
    if not search_type:
        return JsonResponse(
            {"error": "Provide a search type - 'library' or 'reader'."}, status=400
        )
    if not q:
        return JsonResponse({"error": "Provide a search query."}, status=400)

    scope = {}
    data = {"results": []}

    # conduct search
    if search_type == "library":

        page_num = int(request.GET.get("page_num"))
        aggregate_fields = {
            "filtered_text_group": {"terms": {"field": "text_group", "size": 300}}
        }

        data.update({"q": q, "kind": kind, "page_num": page_num, "type": search_type})

        if text_group_urn:
            scope["text_group"] = text_group_urn
            aggregate_fields["filtered_work"] = {
                "terms": {"field": "work", "size": 300}
            }

        if work_urn:
            scope = {}
            scope["work"] = work_urn

        kwargs = {
            "search_type": search_type,
            "scope": scope,
            "aggregate_fields": aggregate_fields,
            "kind": kind,
            "offset": (page_num - 1) * 10,
        }
        try:
            sq = SearchQuery(q, **kwargs)
        except Exception:
            return JsonResponse({"error": "Something went wrong."}, status=500)
        total_count = sq.count()
        page = get_pagination_info(total_count, page_num)
        results = sq.search_window(size=size, offset=((page_num - 1) * 10))

        for result in results:
            r = {"passage": apify(result["passage"], with_content=False)}
            if kind == "form":
                r["content"] = result["raw_content"]
            else:
                r["content"] = result["content"]
            data["results"].append(r)

        data.update(
            {
                "text_groups": results.filtered_aggs("filtered_text_group"),
                "works": results.filtered_aggs("filtered_work")
                if text_group_urn
                else None,
                "total_count": total_count,
                "page": page,
            }
        )

    else:

        offset = int(request.GET.get("offset", "0"))
        pivot = request.GET.get("pivot")
        work_urn = request.GET.get("work")
        text_urn = request.GET.get("text")
        passage_urn = request.GET.get("passage")

        if text_group_urn:
            scope["text_group"] = text_group_urn
        elif work_urn:
            scope["work"] = work_urn
        elif text_urn:
            scope["text.urn"] = text_urn
        elif passage_urn:
            scope["urn"] = passage_urn

        query_kwargs = {
            "search_type": search_type,
            "scope": scope,
            "sort_by": "document",
            "kind": kind,
        }
        sq = SearchQuery(q, **query_kwargs)

        if "text.urn" in scope and pivot:
            urn = cts.URN(pivot)
            urn_start = f"{urn.upTo(cts.URN.NO_PASSAGE)}:{urn.reference.start}"
            for doc_offset, doc in enumerate(sq.scan()):
                if doc["_id"] == urn_start:
                    start_offset = max(0, doc_offset - (size // 2))
                    data["pivot"] = {
                        "offset": doc_offset,
                        "start_offset": start_offset,
                        "end_offset": start_offset + size - 1,
                    }
                    offset = start_offset
                    break

        data["total_count"] = sq.count()
        fields = set(request.GET.get("fields", "content,highlights").split(","))

        for result in sq.search_window(size=size, offset=offset):
            r = {"passage": apify(result["passage"], with_content=False)}
            if "content" in fields:
                r["content"] = result["content"]
            if "highlights" in fields:
                r["highlights"] = [dict(w=w, i=i) for w, i in result["highlights"]]
            data["results"].append(r)

    return JsonResponse(data)


def morpheus(request):
    if ("word" not in request.GET) or ("lang" not in request.GET):
        return HttpResponseBadRequest(
            content='Error when processing morpheus request: "word" and "lang" parameters are required'
        )
    word = request.GET["word"]
    lang = request.GET["lang"]
    allowed_langs = ["grc", "lat"]
    if lang not in allowed_langs:
        return HttpResponseBadRequest(
            content='Error when processing morpheus request: "lang" parameter must be one of: {}'.format(
                ", ".join(allowed_langs)
            )
        )
    params = {"word": word, "lang": lang, "engine": f"morpheus{lang}"}
    qs = urlencode(params)
    url = f"http://services.perseids.org/bsp/morphologyservice/analysis/word?{qs}"
    headers = {"Accept": "application/json"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    body = r.json().get("RDF", {}).get("Annotation", {}).get("Body", [])
    if not isinstance(body, list):
        body = [body]
    data_body = []
    for item in body:
        entry = {
            "uri": item["rest"]["entry"]["uri"],
            # "dict": item["rest"]["entry"]["dict"],
            "hdwd": item["rest"]["entry"]["dict"]["hdwd"]["$"],
            "pofs": item["rest"]["entry"]["dict"]["pofs"]["$"],
        }
        if "decl" in item["rest"]["entry"]["dict"]:
            entry["decl"] = item["rest"]["entry"]["dict"]["decl"]["$"]
        infl_body = item["rest"]["entry"]["infl"]
        if not isinstance(infl_body, list):
            infl_body = [infl_body]
        infl_list = []
        for infl_item in infl_body:
            infl_entry = {
                # "raw": infl_item,
            }
            infl_entry["stem"] = infl_item["term"]["stem"]["$"]
            if "suff" in infl_item["term"]:
                infl_entry["suff"] = infl_item["term"]["suff"].get("$", "")
            infl_entry["pofs"] = infl_item["pofs"]["$"]
            if "case" in infl_item:
                infl_entry["case"] = infl_item["case"]["$"]
            if "mood" in infl_item:
                infl_entry["mood"] = infl_item["mood"]["$"]
            if "tense" in infl_item:
                infl_entry["tense"] = infl_item["tense"]["$"]
            if "voice" in infl_item:
                infl_entry["voice"] = infl_item["voice"]["$"]
            if "gend" in infl_item:
                infl_entry["gend"] = infl_item["gend"]["$"]
            if "num" in infl_item:
                infl_entry["num"] = infl_item["num"]["$"]
            if "pers" in infl_item:
                infl_entry["pers"] = infl_item["pers"]["$"]
            if "comp" in infl_item:
                infl_entry["comp"] = infl_item["comp"]["$"]
            if "dial" in infl_item:
                infl_entry["dial"] = infl_item["dial"]["$"]
            infl_entry["stemtype"] = infl_item["stemtype"]["$"]
            if "derivtype" in infl_item:
                infl_entry["derivtype"] = infl_item["derivtype"]["$"]
            if "morph" in infl_item:
                infl_entry["morph"] = infl_item["morph"]["$"]
            infl_list.append(infl_entry)
        entry["infl"] = infl_list
        data_body.append(entry)
    data = {"Body": data_body}
    return JsonResponse(data)


class CTSApiGetPassageView(LibraryConditionMixin, View):
    """
    Mirrors the output of the Nautilus `GetPassage` endpoint.
    """

    def get_version(self, urn):
        try:
            cts_obj = cts.collection(urn)
        except cts.CollectionDoesNotExist:
            raise Http404()

        if not isinstance(cts_obj, cts.Text):
            raise cts.InvalidURN(
                f'This endpoint only supports passage or version-level URNs [urn="{cts_obj.urn}"]'
            )
        return cts_obj

    def resolve_urn_to_obj(self, urn):
        if not urn.reference:
            return self.get_version(str(urn))
        else:
            return cts.passage(str(urn))

    def get_textual_node(self, cts_obj):
        if isinstance(cts_obj, cts.Text):
            return default_resolver().getTextualNode(
                textId=cts_obj.urn.upTo(URN.NO_PASSAGE)
            )
        return cts_obj.textual_node()

    def get(self, request, **kwargs):
        urn = normalize_urn(self.kwargs["urn"])
        urn_obj = cts.URN(urn)
        try:
            cts_obj = self.resolve_urn_to_obj(urn_obj)
        except cts.InvalidURN as e:
            return HttpResponse(
                json.dumps({"reason": str(e)}),
                status=404,
                content_type="application/json",
            )
        node = self.get_textual_node(cts_obj)
        ctx = {
            "request_urn": urn,
            # TODO: simplify this, as it appears to always be
            #  the same as request_urn
            "full_urn": urn,
            "passage": SafeString(node.export(Mimetypes.XML.TEI)),
        }
        return render(
            self.request, "cts_api/get_passage.xml", ctx, content_type="application/xml"
        )


class CTSApiGetValidReffView(LibraryConditionMixin, View):
    """
    Mirrors the output of the Nautilus `GetValidReff` endpoint
    """

    def get(self, request, **kwargs):
        urn = normalize_urn(self.kwargs["urn"])
        urn = URN(urn)
        subreference = None
        textId = urn.upTo(URN.NO_PASSAGE)
        if urn.reference is not None:
            subreference = str(urn.reference)

        level = int(request.GET.get("level", 1))
        reffs = default_resolver().getReffs(
            textId=textId, subreference=subreference, level=level
        )
        ctx = {
            "reffs": reffs,
            "urn": textId,
            "level": level,
            "request_urn": str(urn),
        }
        return render(
            request,
            "cts_api/get_valid_reffs.xml",
            ctx,
            content_type="application/xml",
        )


class CorporaReposView(View):
    """
    Backport of `/repos` route from scaife-cts-api.
    """

    def get(self, request, **kwargs):
        manifest = hookset.content_manifest_path
        with manifest.open("rb") as f:
            data = yaml.safe_load(f)
            return JsonResponse(data)


class CorpusMetadata(View):
    """
    Backport of `/corpus-metadata` route from scaife-cts-api.
    """

    def get(self, request, **kwargs):
        cts_data_path = Path(settings.CTS_LOCAL_DATA_PATH)
        metadata = cts_data_path / ".scaife-viewer.json"
        with open(metadata, "rb") as f:
            data = json.load(f)
            return JsonResponse(data, safe=False)
