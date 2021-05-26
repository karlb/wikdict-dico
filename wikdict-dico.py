import dico  # type: ignore
from typing import List
import sqlite3

import wikdict_query


def print_result(r):
    print()
    if r["part_of_speech"]:
        pos = f" ({r['part_of_speech']})"
    else:
        pos = ""
    print(
        f"### {r['written_rep']}{pos} {r['match_score']} * {r['translation_score']} * {r['importance']}"
    )

    if r["forms"]:
        print(", ".join(r["forms"]))

    if r["pronuns"]:
        print(", ".join(r["pronuns"]))

    for i, sg in enumerate(r["sense_groups"]):
        print(f"{i+1}.", ", ".join(sg["translations"]), end="")
        if sg["senses"]:
            print(" --", ", ".join(sg["senses"]), end="")
        print()


class DicoResult:
    result: List[dict]

    def __init__(self, *argv):
        self.result = list(argv[0])

    def count(self):
        return len(self.result)

    def output(self, n):
        ...


class DicoDefineResult(DicoResult):
    def output(self, n):
        print_result(self.result[n])


class DicoMatchResult(DicoResult):
    def output(self, n):
        print(self.result[n]['written_rep'], end="")


class DicoModule:
    def __init__(self, from_lang, to_lang, db_filename):
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.db_filename = db_filename

    def open(self, dbname):
        """Open the database."""
        self.dbname = dbname
        self.conn = sqlite3.connect(self.db_filename)

    def close(self):
        """Close the database."""
        self.conn.close()

    def descr(self):
        """Return a short description of the database."""
        return f"WikDict {self.from_lang} -> {self.to_lang} bilingual dictionary"

    def info(self):
        """Return full information about the database."""
        return False

    def lang(self):
        """Optional. Return supported languages (src, dst)."""
        return (self.from_lang, self.to_lang)

    def define_word(self, word):
        """Define a word."""
        results = wikdict_query.define(self.conn, word)
        return DicoDefineResult(results)

    def match_word(self, strat, word):
        """Look up a word in the database."""
        results = wikdict_query.match(self.conn, str(word))
        return DicoMatchResult(results)

    def output(self, rh, n):
        """Output Nth result from the result set."""
        rh.output(n)
        return True

    def result_count(self, rh):
        """Return the number of elements in the result set."""
        return rh.count()

    def result_headers(self, rh, hdr):
        """Optional. Return a dictionary of MIME headers."""
        return hdr

    def db_mime_header(self):
        """Alternative interface to result_headers.
        Return MIME headers as a (multi-line) string. The major difference
        between this method and result_headers is that result_headers is
        called for each result individually, whereas db_mime_header is called
        exactly once, when initializing the database.

        Unless your database implementation supports per-result MIME headers,
        define only db_mime_header.
        """
        return False
