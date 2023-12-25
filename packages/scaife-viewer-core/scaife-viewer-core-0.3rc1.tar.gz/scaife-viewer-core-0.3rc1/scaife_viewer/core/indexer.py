import csv
import json
import logging
import multiprocessing
import os
from collections import Counter, deque
from functools import lru_cache
from itertools import zip_longest
from operator import attrgetter
from pathlib import Path
from typing import Iterable, List, NamedTuple

from django.conf import settings

import dask.bag
import elasticsearch
import elasticsearch.helpers
from anytree.iterators import PreOrderIter

from . import cts
from .morphology import Morphology
from .search import default_es_client_config


logger = logging.getLogger(__name__)
morphology = None
DASK_CONFIG_NUM_WORKERS = int(
    os.environ.get("DASK_CONFIG_NUM_WORKERS", multiprocessing.cpu_count() - 1)
)
DASK_PARTITIONS = int(os.environ.get("DASK_PARTITIONS", "100"))
LEMMA_CONTENT = bool(int(os.environ.get("LEMMA_CONTENT", 0)))

NO_LEMMA = "�"
TOKEN_ANNOTATIONS_PATH = os.environ.get("TOKEN_ANNOTATIONS_PATH")


def compute_kwargs(**params):
    max_workers = params.get("max_workers", DASK_CONFIG_NUM_WORKERS)
    kwargs = {"num_workers": max_workers}
    kwargs.update(params)
    return kwargs


class SortedPassage(NamedTuple):

    urn: str
    sort_idx: int


class Indexer:
    def __init__(
        self,
        pusher,
        morphology_path,
        urn_prefix=None,
        chunk_size=100,
        limit=None,
        dry_run=False,
        max_workers=None,
    ):
        self.pusher = pusher
        self.urn_prefix = urn_prefix
        self.chunk_size = chunk_size
        self.limit = limit
        self.dry_run = dry_run
        self.max_workers = max_workers
        self.load_morphology(morphology_path)

    def load_morphology(self, path):
        global morphology
        if path and morphology is None:
            morphology = Morphology.load(path)
            print("Morphology loaded")

    def get_urn_obj(self):
        if not self.urn_prefix:
            return None
        return cts.URN(self.urn_prefix)

    def get_urn_prefix_filter(self, urn_obj):
        if not urn_obj:
            return None
        if urn_obj.reference:
            up_to = cts.URN.NO_PASSAGE
        elif urn_obj.version:
            up_to = cts.URN.VERSION
        elif urn_obj.work:
            up_to = cts.URN.WORK
        elif urn_obj.textgroup:
            up_to = cts.URN.TEXTGROUP
        elif urn_obj.namespace:
            up_to = cts.URN.NAMESPACE
        else:
            raise ValueError(f'Could not derive prefix filter from "{urn_obj}"')

        value = urn_obj.upTo(up_to)
        print(f"Applying URN prefix filter: {value}")
        return value

    def prepare_passages(self, urn_prefix=None):
        if urn_prefix is not None:
            raise NotImplementedError("URN prefix is not currently supported")

        texts = dask.bag.from_sequence(
            self.texts(urn_prefix.upTo(cts.URN.NO_PASSAGE) if urn_prefix else None)
        )

        passages = []
        for text in texts:
            passages.extend(self.passages_from_text(text))
        if self.limit is not None:
            passages = passages[0 : self.limit]
        return passages

    @staticmethod
    # TODO: Make maxsize configurable; this really exists
    # so we can use a threadlocal within each process
    @lru_cache(maxsize=1)
    def get_lemma_lookup(version_urn):
        workparts = str(version_urn).rsplit(":", maxsplit=1)[1]
        tg, work, _ = workparts.split(".")
        inf = Path(TOKEN_ANNOTATIONS_PATH, f"{tg}/{work}/{workparts}.tsv")
        if not inf.exists():
            print(f"{inf.name} not found")
            return None

        # TODO: Experiment with loading this lookup
        # in a similar fashion as the `morphology` global, or via
        # Pandas or via SQLite
        lemma_lookup = {}
        for row in csv.DictReader(inf.open(), delimiter="\t"):
            lemma_lookup[row["subref"]] = row["lemma"]
        return lemma_lookup

    def index(self):
        cts.TextInventory.load()
        print("Text inventory loaded")
        urn_obj = self.get_urn_obj()
        prefix_filter = self.get_urn_prefix_filter(urn_obj)

        passages = self.prepare_passages(urn_prefix=prefix_filter)

        print(f"Indexing {len(passages)} passages")
        process_lemmas = LEMMA_CONTENT

        if process_lemmas:
            print(f"Processing lemmas")
            # FIXME: Refactor without globals;
            # may cause an issue with lru_cache and our staticmethod
            global TOKEN_ANNOTATIONS_PATH
            if TOKEN_ANNOTATIONS_PATH:
                TOKEN_ANNOTATIONS_PATH = Path(TOKEN_ANNOTATIONS_PATH)
                print(f"Will load annotations from {TOKEN_ANNOTATIONS_PATH}")
            elif bool(morphology):
                print(f"Will load annotations from `morphology` global")
            else:
                # Nothing to populate lemmas with
                process_lemmas = False
                print(
                    "`morphology` and `TOKEN_ANNOTATIONS_PATH` are falsey; aborting lemma processing"
                )

        indexer_kwargs = dict(lemma_content=process_lemmas)
        word_counts = (
            dask.bag.from_sequence(passages, npartitions=DASK_PARTITIONS)
            .map_partitions(self.indexer, **indexer_kwargs)
            .compute(**compute_kwargs(max_workers=self.max_workers))
        )
        total_word_counts = Counter()
        for (lang, count) in word_counts:
            total_word_counts[lang] += count
        word_count_line = [
            f"{lang}={count}" for lang, count in total_word_counts.items()
        ]
        print("Word Count Summary: {0}".format(", ".join(word_count_line)))

    def texts(self, urn_prefix):
        ti = cts.text_inventory()
        for text_group in ti.text_groups():
            for work in text_group.works():
                for text in work.texts():
                    # skip these URNs because they cause MemoryError due to their
                    # massive token size when doing morphology alignment
                    # @@@ proper exclude functionality
                    exclude = {
                        "urn:cts:greekLit:tlg2371.tlg001.opp-grc1",
                        "urn:cts:greekLit:tlg4013.tlg001.opp-grc1",
                        "urn:cts:greekLit:tlg4013.tlg003.opp-grc1",
                        "urn:cts:greekLit:tlg4013.tlg004.opp-grc1",
                        "urn:cts:greekLit:tlg4013.tlg005.opp-grc1",
                        "urn:cts:greekLit:tlg4015.tlg001.opp-grc1",
                        "urn:cts:greekLit:tlg4015.tlg002.opp-grc1",
                        "urn:cts:greekLit:tlg4015.tlg004.opp-grc1",
                        "urn:cts:greekLit:tlg4015.tlg005.opp-grc1",
                        "urn:cts:greekLit:tlg4015.tlg006.opp-grc1",
                        "urn:cts:greekLit:tlg4015.tlg007.opp-grc1",
                        "urn:cts:greekLit:tlg4015.tlg008.opp-grc1",
                        "urn:cts:greekLit:tlg4015.tlg009.opp-grc1",
                        "urn:cts:greekLit:tlg4016.tlg003.opp-grc2",
                    }
                    if str(text.urn) in exclude:
                        continue
                    if urn_prefix and not str(text.urn).startswith(urn_prefix):
                        continue
                    yield text

    def passages_from_text(self, text) -> List[SortedPassage]:
        passages = []
        try:
            toc = text.toc()
        except Exception as e:
            print(f"toc error: {e} [urn={text.urn}]")
        else:
            leaves = PreOrderIter(toc.root, filter_=attrgetter("is_leaf"))
            for i, node in enumerate(leaves):
                passages.append(
                    SortedPassage(urn=f"{text.urn}:{node.reference}", sort_idx=i,)
                )
        return passages

    def indexer(self, chunk: Iterable[SortedPassage], lemma_content=True):
        from raven.contrib.django.raven_compat.models import client as sentry

        words = []
        result = None
        for p in chunk:
            urn = p.urn
            try:
                passage = cts.passage(urn)
            except cts.PassageDoesNotExist:
                print(f"Passage does not exist [urn={urn}]")
                continue
            except Exception as e:
                print(f"Error {e} [urn={urn}]")
                continue
            try:
                # tokenized once and passed around as an optimization
                tokens = passage.tokenize(whitespace=False)
                stats = (str(passage.text.lang), self.count_words(tokens))
                words.append(stats)
                doc = self.passage_to_doc(
                    passage, p.sort_idx, tokens, stats, lemma_content
                )
            except MemoryError:
                return words
            except Exception:
                sentry.captureException()
                raise
            if not self.dry_run:
                result = self.pusher.push(doc)

        self.pusher.finalize(result, self.dry_run)

        return words

    def count_words(self, tokens) -> int:
        n = 0
        for token in tokens:
            if token["t"] == "w":
                n += 1
        return n

    def lemma_content(self, passage, tokens) -> str:
        if TOKEN_ANNOTATIONS_PATH:
            urn = str(passage.urn)
            version_urn, ref = str(urn).rsplit(":", maxsplit=1)

            lemma_lookup = self.get_lemma_lookup(version_urn)
            if not lemma_lookup:
                return None

            lemma_tokens = []
            for svt in tokens:
                token = svt["w"]
                subref_count = svt["i"]
                subref = f"{ref}@{token}"
                if subref_count != 1:
                    subref = f"{subref}[{subref_count}]"
                lt = lemma_lookup.get(subref) or NO_LEMMA
                lemma_tokens.append(lt)
            return " ".join(lemma_tokens)

        if morphology is None:
            return ""
        short_key = morphology.short_keys.get(str(passage.text.urn))
        if short_key is None:
            return ""

        token_limit = 50000
        limit_exceeded = len(tokens) > token_limit
        if limit_exceeded:
            print(
                f"more than {token_limit} tokens detected [urn={passage.urn}] [count={len(tokens)}]"
            )

        thibault = [token["w"] for token in tokens]
        giuseppe = []
        text = morphology.text.get((short_key, str(passage.reference)))
        if text is None:
            return ""
        for form_keys in text.values():
            form_key = form_keys[0]
            form = morphology.forms[int(form_key) - 1]
            giuseppe.append((form.form, form.lemma))
        missing = chr(0xFFFD)
        content = " ".join(
            [{None: missing}.get(w, w) for w in align_text(thibault, giuseppe)]
        )
        if limit_exceeded:
            print(f"lemma content generated [urn={passage.urn}]")

        return content

    def passage_to_doc(self, passage, sort_idx, tokens, word_stats, lemma_content):
        urn = str(passage.urn)
        language, word_count = word_stats

        lc = None
        # TODO: Support lemmas in other languages
        if language == "grc" and lemma_content:
            lc = self.lemma_content(passage, tokens)

        return {
            "urn": urn,
            "text_group": str(passage.text.urn.upTo(cts.URN.TEXTGROUP)),
            "work": str(passage.text.urn.upTo(cts.URN.WORK)),
            "text": {
                "urn": str(passage.text.urn),
                "label": passage.text.label,
                "description": passage.text.description,
            },
            "reference": str(passage.reference),
            "sort_idx": sort_idx,
            "content": " ".join([token["w"] for token in tokens]),
            "raw_content": passage.content,
            "lemma_content": lc,
            "language": language,
            "word_count": word_count,
        }


def consume(it):
    deque(it, maxlen=0)


def chunker(iterable, n):
    args = [iter(iterable)] * n
    for chunk in zip_longest(*args, fillvalue=None):
        yield [item for item in chunk if item is not None]


class DirectPusher:
    def __init__(self, chunk_size=500, index_name=None):
        self.chunk_size = chunk_size
        if index_name is None:
            index_name = settings.ELASTICSEARCH_INDEX_NAME
        self.index_name = index_name
        self.es.indices.create(index=self.index_name, ignore=400)

    @property
    def es(self):
        if not hasattr(self, "_es"):
            self._es = elasticsearch.Elasticsearch(**default_es_client_config())
        return self._es

    @property
    def docs(self):
        if not hasattr(self, "_docs"):
            self._docs = deque(maxlen=self.chunk_size)
        return self._docs

    def push(self, doc):
        self.docs.append(doc)
        if len(self.docs) == self.chunk_size:
            self.commit_docs()

    def commit_docs(self):
        msg = f"Committing {len(self.docs)} doc(s) to {self.index_name}"
        # FIXME: Prefer logger, but am not seeing messages locally
        print(msg)
        # logger.info(msg)

        metadata = {"_op_type": "index", "_index": self.index_name}
        docs = ({"_id": doc["urn"], **metadata, **doc} for doc in self.docs)
        elasticsearch.helpers.bulk(self.es, docs)
        self.docs.clear()

    def finalize(self, result, dry_run):
        if dry_run:
            return

        # we need to ensure the deque is cleared if less than
        # `chunk_size`
        self.commit_docs()

    def __getstate__(self):
        s = self.__dict__.copy()
        if "_es" in s:
            del s["_es"]
        if "_docs" in s:
            del s["_docs"]
        return s


class PubSubPusher:
    def __init__(self, project, topic):
        self.topic_path = f"projects/{project}/topics/{topic}"

    @property
    def publisher(self):
        if not hasattr(self, "_publisher"):
            # import happens here because module-level kicks off the
            # thread to handle publishing (which breaks multiprocessing)
            import google.cloud.pubsub

            self._publisher = google.cloud.pubsub.PublisherClient()
        return self._publisher

    def push(self, doc):
        """
        Returns a Future

        https://github.com/googleapis/google-cloud-python/blob/master/pubsub/docs/publisher/index.rst#futures
        """
        return self.publisher.publish(self.topic_path, json.dumps(doc).encode("utf-8"))

    def finalize(self, future, dry_run):
        if dry_run:
            return

        if future and not future.done():
            print("Publishing messages to PubSub")
            # Block until the last message has been published
            # https://github.com/googleapis/google-cloud-python/blob/69ec9fea1026c00642ca55ca18110b7ef5a09675/pubsub/docs/publisher/index.rst#futures
            future.result()

    def __getstate__(self):
        s = self.__dict__.copy()
        if "_publisher" in s:
            del s["_publisher"]
        return s


def nw_align(a, b, replace_func=lambda x, y: -1 if x != y else 0, insert=-1, delete=-1):
    ZERO, LEFT, UP, DIAGONAL = 0, 1, 2, 3
    len_a, len_b = len(a), len(b)
    matrix = [[(0, ZERO) for x in range(len_b + 1)] for y in range(len_a + 1)]
    for i in range(len_a + 1):
        matrix[i][0] = (insert * i, UP)
    for j in range(len_b + 1):
        matrix[0][j] = (delete * j, LEFT)
    for i in range(1, len_a + 1):
        for j in range(1, len_b + 1):
            replace = replace_func(a[i - 1], b[j - 1])
            matrix[i][j] = max(
                [
                    (matrix[i - 1][j - 1][0] + replace, DIAGONAL),
                    (matrix[i][j - 1][0] + insert, LEFT),
                    (matrix[i - 1][j][0] + delete, UP),
                ]
            )
    i, j = len_a, len_b
    alignment = []
    while (i, j) != (0, 0):
        if matrix[i][j][1] == DIAGONAL:
            alignment.insert(0, (a[i - 1], b[j - 1]))
            i -= 1
            j -= 1
        elif matrix[i][j][1] == LEFT:
            alignment.insert(0, (None, b[j - 1]))
            j -= 1
        else:  # UP
            alignment.insert(0, (a[i - 1], None))
            i -= 1
    return alignment


def replace_func(a, b):
    if a == b[0]:
        return 0
    else:
        return -1


def align_text(a, b):
    result = nw_align(a, b, replace_func=replace_func)
    for x, y in result:
        if y is None:
            yield None
        elif x:
            yield y[1]
