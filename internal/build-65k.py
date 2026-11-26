#!/usr/bin/env python3
"""Train the English tail of the frozen 65,536-token tokenizer.

Runs on the EC2 instance. Indic ids stay on the frozen keep-set.
Indic spans are cut with the BPE scores stored in tokenizer-65k.json.
"""

from __future__ import annotations

import hashlib
import heapq
import json
import os
import re
import sys
import time
import unicodedata
from array import array
from collections import Counter, defaultdict

import pyarrow.fs as pafs
import pyarrow.parquet as pq
import sentencepiece as spm
from tokenizers import Regex, Tokenizer
from tokenizers.models import BPE as TokBPE
from tokenizers.pre_tokenizers import Split

ROOT = os.environ.get("TOK65_ROOT", "/home/ubuntu/tokenizer65k")
MODEL_PATH = os.path.join(ROOT, "tokenizer.model")
BUCKET = "nemotron-training-data-us-east-1"
TARGET_BYTES = int(os.environ.get("TOK65_BYTES", "4000000000"))
EVAL_BYTES = 500_000
VOCAB = 65_536
N_SPECIAL = 32
N_BYTE = 256
TAIL_START_FALLBACK = 40_347

SPECIALS = ["<unk>", "<s>", "</s>", "<pad>", "<eod>"] + [
    f"<reserved_{i:04d}>" for i in range(5, 32)
]
SCISSORS = (
    r"(?:\r\n|\n|\r)[ \t]*"
    r"|\\[A-Za-z]+"
    r"|[0-9]"
    r"|[^\r\n\p{L}\p{N}]?[\p{L}\p{M}]+(?:['\x{2019}][\p{L}\p{M}]+)*"
    r"|[^\s\p{L}\p{M}\p{N}]+"
    r"|[^\S\r\n]+"
    r"|[\s\S]"
)
CMD_RE = re.compile(r"\\[A-Za-z]+")
WORD_RE = re.compile(r"[ \t\n\r]+")
FORCED_COMMANDS = [
    "\\frac",
    "\\partial",
    "\\circ",
    "\\overrightarrow",
    "\\subseteq",
    "\\setminus",
]
BLOCKS = {
    "devanagari": ((0x0900, 0x097F), (0x1CD0, 0x1CFF), (0xA8E0, 0xA8FF)),
    "bengali": ((0x0980, 0x09FF),),
    "gurmukhi": ((0x0A00, 0x0A7F),),
    "gujarati": ((0x0A80, 0x0AFF),),
    "oriya": ((0x0B00, 0x0B7F),),
    "tamil": ((0x0B80, 0x0BFF),),
    "telugu": ((0x0C00, 0x0C7F),),
    "kannada": ((0x0C80, 0x0CFF),),
    "malayalam": ((0x0D00, 0x0D7F),),
}
DROP_SCRIPTS = frozenset({"gurmukhi", "oriya", "malayalam"})
KEEP_SCRIPTS = frozenset({"devanagari", "bengali", "gujarati", "tamil", "telugu", "kannada"})
LANGS = [
    ("Hindi", "hin"),
    ("Marathi", "mar"),
    ("Kannada", "kan"),
    ("Telugu", "tel"),
    ("Tamil", "tam"),
    ("Gujarati", "guj"),
    ("Bengali", "ben"),
]
FIXTURES = {
    "नमस्ते": ["▁नम", "स्ते"],
    "हिन्दी": ["▁ह", "िन्", "दी"],
    "ಕನ್ನಡ": ["▁ಕ", "ನ್ನ", "ಡ"],
}

EN_SOURCES = [
    ("climbmix", "datasets/nemotron-climbmix/karpathy-400b-shuffle/"),
]
CODE_SOURCES = [
    (
        "nemotron-code-concepts",
        "datasets/Nemotron-Pretraining-Specialized-v1.1/Nemotron-Pretraining-Code-Concepts/",
    ),
    (
        "nemotron-scientific-coding",
        "datasets/Nemotron-Pretraining-Specialized-v1/Nemotron-Pretraining-Scientific-Coding/",
    ),
]
MATH_SOURCES = [
    ("nemotron-math-4plus", "datasets/nemotron-cc-math-v1/4plus/"),
    (
        "nemotron-math-textbooks",
        "datasets/Nemotron-Pretraining-Specialized-v1/Nemotron-Pretraining-Math-Textbooks/",
    ),
]
MISSING_SOURCES = [
    "CodeAlchemy is not in the bucket",
    "A dataset named Nemotron Code is not in the bucket. Code share uses Nemotron-Pretraining-Code-Concepts and Nemotron-Pretraining-Scientific-Coding, half and half.",
    "Finemath is not a separate corpus in the bucket",
    "SwallowMath is not in the bucket",
    "Nemotron CC HQ is in the bucket and was not used. ClimbMix is present, so it takes the English share.",
]


def log(msg: str) -> None:
    print(f"{time.strftime('%H:%M:%S')} {msg}", flush=True)


def bytes_to_unicode() -> dict[int, str]:
    bs = (
        list(range(ord("!"), ord("~") + 1))
        + list(range(ord("¡"), ord("¬") + 1))
        + list(range(ord("®"), ord("ÿ") + 1))
    )
    cs = bs[:]
    n = 0
    for b in range(256):
        if b not in bs:
            bs.append(b)
            cs.append(256 + n)
            n += 1
    return dict(zip(bs, [chr(c) for c in cs]))


B2U = bytes_to_unicode()
U2B = {ch: b for b, ch in B2U.items()}
BYTE_CHARS = set(B2U.values())


def script_of(ch: str) -> str | None:
    code = ord(ch)
    for name, ranges in BLOCKS.items():
        for lo, hi in ranges:
            if lo <= code <= hi:
                return name
    return None


LATIN_LETTER_CATEGORIES = {"Lu", "Ll", "Lt", "Lm", "Lo"}


def is_latin_letter(ch: str) -> bool:
    if unicodedata.category(ch) not in LATIN_LETTER_CATEGORIES:
        return False
    return unicodedata.name(ch, "").startswith("LATIN ")


def is_indic_block(ch: str) -> bool:
    name = script_of(ch)
    return name in KEEP_SCRIPTS


def nearest_indic(text: str, idx: int, step: int) -> bool:
    i = idx + step
    n = len(text)
    while 0 <= i < n:
        ch = text[i]
        if ch in ("\u200c", "\u200d"):
            i += step
            continue
        if is_indic_block(ch):
            return True
        if is_latin_letter(ch) or unicodedata.category(ch)[:1] == "L":
            return False
        i += step
    return False


def counts_as_indic(text: str, idx: int) -> bool:
    ch = text[idx]
    if ch in ("\u200c", "\u200d"):
        return nearest_indic(text, idx, -1) or nearest_indic(text, idx, 1)
    return is_indic_block(ch)


# Punctuation folds onto ASCII pieces already in the vocabulary.
# No new piece is added for a curly quote or a unicode dash.
_PUNCT_FOLD = {
    "\u2018": "'",
    "\u2019": "'",
    "\u201A": "'",
    "\u201B": "'",
    "\u201C": '"',
    "\u201D": '"',
    "\u201E": '"',
    "\u201F": '"',
    "\u00AB": '"',
    "\u00BB": '"',
    "\u2032": "'",
    "\u2033": '"',
    "\u2010": "-",
    "\u2011": "-",
    "\u2012": "-",
    "\u2013": "-",
    "\u2014": "-",
    "\u2015": "-",
    "\u2212": "-",
}
# Default-ignorable format characters. ZWJ and ZWNJ stay: they change the word.
_ZERO_WIDTH_STRIP = frozenset(
    {
        "\u200B",  # zero-width space
        "\u200E",  # left-to-right mark
        "\u200F",  # right-to-left mark
        "\uFEFF",  # BOM / zero-width no-break space
        "\u2060",  # word joiner
        "\u2061",
        "\u2062",
        "\u2063",
        "\u2064",
        "\u2066",
        "\u2067",
        "\u2068",
        "\u2069",
        "\u202A",
        "\u202B",
        "\u202C",
        "\u202D",
        "\u202E",
        "\u180E",
    }
)


def normalize_text(text: str) -> str:
    """NFC, whitespace, punctuation, and zero-width characters.

    Space separators (Unicode Zs) become U+0020. Tab, newline, and carriage
    return stay. Curly quotes and unicode dashes fold onto ASCII. Zero-width
    format characters other than U+200C and U+200D are removed. The vocabulary
    does not grow.
    """
    text = unicodedata.normalize("NFC", text)
    out: list[str] = []
    for ch in text:
        if ch in _ZERO_WIDTH_STRIP:
            continue
        folded = _PUNCT_FOLD.get(ch)
        if folded is not None:
            out.append(folded)
            continue
        if ch != " " and unicodedata.category(ch) == "Zs":
            out.append(" ")
            continue
        out.append(ch)
    return "".join(out)


def has_banned_char(text: str) -> bool:
    if "\u2581" in text:
        return True
    for ch in text:
        if ch in ("\u200c", "\u200d"):
            return True
        name = script_of(ch)
        if name in KEEP_SCRIPTS or name in DROP_SCRIPTS:
            return True
    return False


def word_count(text: str) -> int:
    return sum(1 for part in WORD_RE.split(text) if part)


def keep_piece(token: str) -> bool:
    if token.startswith("<<reserved_token_"):
        return False
    if len(token) == 6 and token.startswith("<0x") and token.endswith(">"):
        return True
    if token in ("<unk>", "<s>", "</s>", "<pad>"):
        return False
    scripts: set[str] = set()
    latin = False
    for ch in token:
        if ch == "▁":
            continue
        found = script_of(ch)
        if found:
            scripts.add(found)
        elif is_latin_letter(ch):
            latin = True
    if latin or (scripts & DROP_SCRIPTS) or len(scripts) > 1:
        return False
    if len(scripts) == 1:
        return True
    if token in ("\n", "\r", "\t"):
        return False
    return True


def whitespace_seeds() -> list[str]:
    rows = []
    for n in range(1, 9):
        rows.append((0, "\n" + (" " * n)))
    for n in range(1, 5):
        rows.append((1, "\n" + ("\t" * n)))
    rows.append((2, "  "))
    rows.append((2, "    "))
    rows.append((2, "        "))
    rows.append((3, "\r\n"))
    rows.sort(key=lambda item: (len(item[1]), item[0], item[1]))
    return [text for _, text in rows]


class Tables:
    def __init__(self) -> None:
        self.sp = spm.SentencePieceProcessor()
        self.sp.Load(MODEL_PATH)
        self.pieces: list[str] = [""] * VOCAB
        self.sarvam_of: list[int | None] = [None] * VOCAB
        self.sarvam_piece: list[str | None] = [None] * VOCAB
        self.raw_of: list[bytes | None] = [None] * VOCAB
        self.piece_to_id: dict[str, int] = {}
        self.meaning_owner: dict[str, int] = {}
        self.K = 0
        self.U = 0
        self.tail = 0
        self.tail_start = 0
        self.fingerprint: dict[str, int] = {}
        self.latin = 0
        self.dropped_unnamed: list[str] = []
        self.vowel_mark_pieces = 0
        self.indic_scores: list[int | None] = [None] * VOCAB
        self.indic_normalizer = {
            "form": "NFC",
            "dummy_prefix": True,
            "space_mark": "▁",
        }

    def build(self) -> None:
        n = self.sp.GetPieceSize()
        if n != 68096:
            raise SystemExit(f"vocabulary size is {n}, expected 68096")
        got = self.sp.EncodeAsPieces("नमस्ते")
        if got[:1] == ["<s>"]:
            got = got[1:]
        if got[-1:] == ["</s>"]:
            got = got[:-1]
        if got != ["▁नम", "स्ते"]:
            raise SystemExit(f"नमस्ते pieces are {got}")
        for i, name in enumerate(SPECIALS):
            self.pieces[i] = name
            self.meaning_owner[name] = i
        for b in range(256):
            oid = N_SPECIAL + b
            stored = B2U[b]
            self.pieces[oid] = stored
            self.raw_of[oid] = bytes([b])
            try:
                meaning = bytes([b]).decode("utf-8")
            except UnicodeDecodeError:
                meaning = stored
            self.meaning_owner.setdefault(meaning, oid)
        kept_new: list[tuple[int, str]] = []
        shared = 0
        unnamed_kept = 0
        fp = Counter()
        latin = 0
        dropped_unnamed = []
        for sid in range(n):
            token = self.sp.IdToPiece(sid)
            if token.startswith("<<reserved_token_"):
                continue
            if len(token) == 6 and token.startswith("<0x") and token.endswith(">"):
                fp["byte"] += 1
            elif is_latin_only(token):
                latin += 1
            elif not keep_piece(token) and not token.startswith("<0x") and token not in ("<unk>", "<s>", "</s>", "<pad>") and not token.startswith("<<reserved_token_"):
                if script_bucket(token) == "unnamed" and token in ("\n", "\r", "\t"):
                    dropped_unnamed.append(token)
            if not keep_piece(token):
                continue
            bucket = script_bucket(token)
            if bucket in KEEP_SCRIPTS or bucket == "byte":
                fp[bucket] += 1
            else:
                unnamed_kept += 1
            if token in self.meaning_owner and token in BYTE_CHARS:
                oid = self.meaning_owner[token]
                if self.sarvam_of[oid] is None:
                    self.sarvam_of[oid] = sid
                    self.sarvam_piece[oid] = token
                    self.piece_to_id[token] = oid
                    shared += 1
                continue
            kept_new.append((sid, token))
        self.K = len(kept_new)
        self.U = unnamed_kept
        self.latin = latin
        self.dropped_unnamed = dropped_unnamed
        self.fingerprint = dict(fp)
        self.tail = VOCAB - N_SPECIAL - N_BYTE - self.K
        self.tail_start = N_SPECIAL + N_BYTE + self.K
        if self.K != 40059 or self.U != 435 or self.tail != 25189:
            raise SystemExit(
                f"freeze counts drifted K={self.K} U={self.U} tail={self.tail} shared={shared}"
            )
        if self.tail_start != 40347:
            raise SystemExit(f"tail start {self.tail_start}")
        next_id = N_SPECIAL + N_BYTE
        for sid, token in kept_new:
            if token in self.piece_to_id:
                raise SystemExit(f"duplicate piece {token!r}")
            self.pieces[next_id] = token
            self.sarvam_of[next_id] = sid
            self.sarvam_piece[next_id] = token
            self.piece_to_id[token] = next_id
            self.meaning_owner[token] = next_id
            if starts_with_vowel_mark(token):
                self.vowel_mark_pieces += 1
            next_id += 1
        if next_id != self.tail_start:
            raise SystemExit("id cursor missed the tail")
        for oid, sid in enumerate(self.sarvam_of):
            if sid is None:
                continue
            if (
                self.sp.IsByte(sid)
                or self.sp.IsControl(sid)
                or self.sp.IsUnknown(sid)
                or self.sp.IsUnused(sid)
            ):
                continue
            score = self.sp.GetScore(sid)
            self.indic_scores[oid] = int(score) if score == int(score) else score
        log(
            f"frozen K={self.K} U={self.U} tail={self.tail} "
            f"latin={self.latin} vowel_mark_starts={self.vowel_mark_pieces}"
        )

    def write_frozen(self) -> str:
        kept = []
        for oid in range(VOCAB):
            if self.sarvam_of[oid] is None:
                continue
            kept.append(
                {
                    "id": oid,
                    "piece": self.sarvam_piece[oid],
                }
            )
        payload = {
            "model_sha256": sha_file(MODEL_PATH),
            "K": self.K,
            "U": self.U,
            "english_tail": self.tail,
            "assigned_before_tail": self.tail_start,
            "latin": self.latin,
            "fingerprint": self.fingerprint,
            "dropped_unnamed": self.dropped_unnamed,
            "vowel_mark_starts": self.vowel_mark_pieces,
            "ids": kept,
        }
        path = os.path.join(ROOT, "frozen_indic_ids.json")
        raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode() + b"\n"
        with open(path, "wb") as fh:
            fh.write(raw)
        digest = hashlib.sha256(raw).hexdigest()
        log(f"wrote {path} sha256={digest}")
        return digest


def is_latin_only(token: str) -> bool:
    if token.startswith("<<reserved") or token.startswith("<0x") or token in ("<unk>", "<s>", "</s>", "<pad>"):
        return False
    latin = False
    for ch in token:
        if ch == "▁":
            continue
        if script_of(ch):
            return False
        if is_latin_letter(ch):
            latin = True
    return latin


def script_bucket(token: str) -> str:
    if len(token) == 6 and token.startswith("<0x") and token.endswith(">"):
        return "byte"
    scripts = set()
    for ch in token:
        if ch == "▁":
            continue
        found = script_of(ch)
        if found:
            scripts.add(found)
    if len(scripts) == 1:
        return next(iter(scripts))
    return "unnamed"


def starts_with_vowel_mark(piece: str) -> bool:
    if not piece:
        return False
    name = unicodedata.name(piece[0], "")
    return "VOWEL SIGN" in name or "LENGTH MARK" in name or ("VOCALIC" in name and "SIGN" in name)


def sha_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def split_mixed_word(word: str):
    kinds = []
    for i, ch in enumerate(word):
        if is_latin_letter(ch):
            kinds.append("L")
        elif counts_as_indic(word, i):
            kinds.append("I")
        else:
            kinds.append("O")
    runs = []
    start = 0
    for i in range(1, len(kinds) + 1):
        if i == len(kinds) or kinds[i] != kinds[start]:
            runs.append([kinds[start], start, i])
            start = i
    pieces = []
    i = 0
    while i < len(runs):
        kind, a, b = runs[i]
        if kind == "O":
            if pieces:
                pieces[-1][2] = b
            elif i + 1 < len(runs):
                runs[i + 1][1] = a
            else:
                pieces.append(["L", a, b])
            i += 1
            continue
        pieces.append([kind, a, b])
        i += 1
    merged = []
    for side, a, b in pieces:
        if merged and merged[-1][0] == side and merged[-1][2] == a:
            merged[-1][2] = b
        else:
            merged.append([side, a, b])
    for side, a, b in merged:
        yield ("en" if side == "L" else "ind", word[a:b])


def split_stretch(stretch: str):
    if stretch == "":
        return
    has_lat = False
    has_ind = False
    for i, ch in enumerate(stretch):
        if is_latin_letter(ch):
            has_lat = True
        elif counts_as_indic(stretch, i):
            has_ind = True
    if not has_lat and not has_ind:
        yield ("en", stretch)
        return
    if not has_lat:
        yield ("ind", stretch)
        return
    if not has_ind:
        yield ("en", stretch)
        return
    buf = []
    parts = []
    for ch in stretch:
        if ch == " ":
            if buf:
                parts.append("".join(buf))
                buf = []
            parts.append(" ")
        else:
            buf.append(ch)
    if buf:
        parts.append("".join(buf))
    # A single space belongs to the following word. English शब्द then has one
    # boundary, the same shape as English word, not a space token plus a second
    # cut before the Indic word. A trailing space stays English.
    pending = ""
    words = []
    for part in parts:
        if part == " ":
            pending += part
        else:
            words.append(pending + part)
            pending = ""
    for word in words:
        yield from split_mixed_word(word)
    if pending:
        yield ("en", pending)


def route_cuts(text: str):
    n = len(text)
    i = 0
    while i < n:
        if text[i] in " \t\n\r":
            j = i + 1
            while j < n and text[j] in " \t\n\r":
                j += 1
            run = text[i:j]
            if run != " ":
                yield ("en", run)
                i = j
                continue
        j = i
        while j < n:
            if text[j] in " \t\n\r":
                k = j + 1
                while k < n and text[k] in " \t\n\r":
                    k += 1
                if text[j:k] != " ":
                    break
                j = k
            else:
                j += 1
        yield from split_stretch(text[i:j])
        i = j


def join_indic_runs(spans):
    """Keep one ordinary space between Indic words inside the Sarvam call.

    A space next to a Latin word stays English. A newline, tab, or run of
    two or more spaces stays English and is never joined.
    """
    spans = list(spans)
    i = 0
    n = len(spans)
    while i < n:
        kind, text = spans[i]
        if kind != "ind":
            yield (kind, text)
            i += 1
            continue
        parts = [text]
        j = i
        while True:
            if j + 1 < n and spans[j + 1][0] == "ind":
                parts.append(spans[j + 1][1])
                j += 1
                continue
            if j + 2 < n and spans[j + 1] == ("en", " ") and spans[j + 2][0] == "ind":
                parts.append(" ")
                parts.append(spans[j + 2][1])
                j += 2
                continue
            break
        yield ("ind", "".join(parts))
        i = j + 1


def route(text: str):
    text = normalize_text(text)
    if text == "":
        return
    yield from join_indic_runs(route_cuts(text))


def make_pretokenizer():
    tok = Tokenizer(TokBPE())
    tok.pre_tokenizer = Split(Regex(SCISSORS), behavior="isolated")
    return tok.pre_tokenizer


def check_scissors(pre) -> None:
    samples = [
        ("don't", ["don't"]),
        ("\\frac{1}{2}", ["\\frac", "{", "1", "}{", "2", "}"]),
        ("65", ["6", "5"]),
        ("\n    return", ["\n    ", "return"]),
    ]
    for text, expected in samples:
        got = [piece for piece, _ in pre.pre_tokenize_str(text)]
        if got != expected:
            raise SystemExit(f"scissors mismatch {text!r} got {got!r}")
    log("scissors match the four strings")


class IndicBPE:
    """Score-based BPE over Unicode characters.

    Higher score merges first. Equal scores merge the leftmost pair first.
    Characters are the atoms. A character with no piece is a byte fallback.
    """

    def __init__(self, scores: dict[str, int | float], normalizer: dict) -> None:
        if normalizer.get("form") != "NFC":
            raise RuntimeError(f"indic normalizer form {normalizer.get('form')!r} is not NFC")
        mark = normalizer.get("space_mark")
        if not isinstance(mark, str) or mark == "":
            raise RuntimeError("indic space mark is missing")
        if not normalizer.get("dummy_prefix"):
            raise RuntimeError("indic BPE expects a dummy prefix")
        self.scores = scores
        self.mark = mark
        # A run of space marks is an English piece (ĠĠ, ĠĠĠĠ, …). Merging the
        # dummy prefix into that run splits the following word.
        self.merge_scores: dict[str, int | float] = {}
        for piece, score in scores.items():
            if len(piece) > 1 and set(piece) == {mark}:
                continue
            self.merge_scores[piece] = score
        self.fallback_count = 0

    @staticmethod
    def parallel(pieces: list[str], score_list: list[int | float | None]) -> dict[str, int | float]:
        if len(pieces) != len(score_list):
            raise RuntimeError("indic scores are not aligned with pieces")
        out: dict[str, int | float] = {}
        for piece, score in zip(pieces, score_list):
            if score is None:
                continue
            if piece in out:
                raise RuntimeError(f"duplicate scored piece {piece!r}")
            out[piece] = score
        return out

    def normalize(self, text: str) -> str:
        text = normalize_text(text)
        return self.mark + text.replace(" ", self.mark)

    def encode_pieces(self, text: str) -> list[str]:
        self.fallback_count = 0
        if text == "":
            return []
        norm = self.normalize(text)
        if norm == "":
            return []
        chars = list(norm)
        n = len(chars)
        # prev, next, start, end, alive. Offsets are character indexes.
        sym = [[(i - 1 if i else -1), (i + 1 if i + 1 < n else -1), i, i + 1, True] for i in range(n)]
        heap: list[tuple] = []
        seq = 0

        def consider(left: int, right: int) -> None:
            nonlocal seq
            if left < 0 or right < 0:
                return
            left_sym = sym[left]
            right_sym = sym[right]
            if not (left_sym[4] and right_sym[4] and left_sym[3] == right_sym[2]):
                return
            start = left_sym[2]
            end = right_sym[3]
            piece = "".join(chars[start:end])
            if piece not in self.merge_scores:
                return
            score = self.merge_scores[piece]
            # left is the first character of the pair, so equal scores take the leftmost pair.
            heapq.heappush(heap, (-score, left, seq, right, end - start))
            seq += 1

        for i in range(1, n):
            consider(i - 1, i)
        while heap:
            _neg, left, _seq, right, size = heapq.heappop(heap)
            left_sym = sym[left]
            right_sym = sym[right]
            if not (left_sym[4] and right_sym[4] and left_sym[3] == right_sym[2]):
                continue
            if right_sym[3] - left_sym[2] != size:
                continue
            left_sym[3] = right_sym[3]
            left_sym[1] = right_sym[1]
            if right_sym[1] >= 0:
                sym[right_sym[1]][0] = left
            right_sym[4] = False
            consider(left_sym[0], left)
            consider(left, left_sym[1])
        out: list[str] = []
        index = 0
        while index != -1:
            left_sym = sym[index]
            start = left_sym[2]
            end = left_sym[3]
            piece = "".join(chars[start:end])
            if piece in self.merge_scores:
                out.append(piece)
            else:
                # One uncovered character.
                self.fallback_count += 1
                out.extend(f"<0x{byte:02X}>" for byte in piece.encode("utf-8"))
            index = left_sym[1]
        return out

    def decode_pieces(self, pieces: list[str]) -> str:
        text = ""
        bos_seen = False
        i = 0

        def is_byte(piece: str) -> bool:
            return (
                len(piece) == 6
                and piece.startswith("<0x")
                and piece.endswith(">")
                and all(ch in "0123456789ABCDEF" for ch in piece[3:5])
            )

        def utf8_text(raw: bytes) -> str:
            chars: list[str] = []
            k = 0
            while k < len(raw):
                byte = raw[k]
                if byte < 0x80:
                    need = 1
                elif byte >> 5 == 0b110:
                    need = 2
                elif byte >> 4 == 0b1110:
                    need = 3
                elif byte >> 3 == 0b11110:
                    need = 4
                else:
                    need = 0
                if need and k + need <= len(raw):
                    try:
                        chars.append(raw[k : k + need].decode("utf-8"))
                        k += need
                        continue
                    except UnicodeDecodeError:
                        pass
                chars.append("\ufffd")
                k += 1
            return "".join(chars)

        while i < len(pieces):
            if is_byte(pieces[i]):
                raw = bytearray()
                j = i
                while j < len(pieces) and is_byte(pieces[j]):
                    raw.append(int(pieces[j][3:5], 16))
                    j += 1
                text += utf8_text(bytes(raw))
                i = j
                continue
            is_bos = not (bos_seen or text)
            piece = pieces[i]
            consumed = False
            if is_bos and piece.startswith(self.mark):
                piece = piece[len(self.mark) :]
                consumed = True
            text += piece.replace(self.mark, " ")
            bos_seen = consumed
            i += 1
        return text


class Encoder:
    def __init__(self, tables: Tables) -> None:
        self.t = tables
        self.pre = make_pretokenizer()
        self.seed_trie = {}
        self.merge_rank: dict[tuple[int, int], int] = {}
        self.merge_to: dict[tuple[int, int], int] = {}
        self.merges: list[list[str]] = []
        self.seed_strings: list[str] = []
        self.trained = False
        self.indic = IndicBPE(
            IndicBPE.parallel(tables.pieces, tables.indic_scores),
            tables.indic_normalizer,
        )
        self.fallback_count = 0

    def indic_pieces(self, text: str) -> list[str]:
        return self.indic.encode_pieces(text)

    def reference_pieces(self, text: str) -> list[str]:
        pieces = self.t.sp.EncodeAsPieces(text)
        if pieces and pieces[0] == "<s>":
            pieces = pieces[1:]
        if pieces and pieces[-1] == "</s>":
            pieces = pieces[:-1]
        return pieces

    def indic_ids(self, text: str) -> tuple[list[int], list[str]]:
        pieces = self.indic_pieces(text)
        ids = []
        for piece in pieces:
            oid = self.t.piece_to_id.get(piece)
            if oid is None:
                raise RuntimeError(f"kept set missing {piece!r} for {text!r}")
            ids.append(oid)
        return ids, pieces

    def add_seed_string(self, text: str, oid: int) -> None:
        node = self.seed_trie
        for ch in text:
            child = node.get(ch)
            if not isinstance(child, dict):
                child = {}
                node[ch] = child
            node = child
        node[None] = oid

    def match_seed(self, text: str, i: int) -> tuple[int, int] | None:
        node = self.seed_trie
        best = None
        j = i
        n = len(text)
        while j < n and isinstance(node, dict):
            child = node.get(text[j])
            if not isinstance(child, dict):
                break
            node = child
            j += 1
            if None in node:
                best = (node[None], j - i)
        return best

    def bpe(self, chunk: str) -> list[int]:
        raw = chunk.encode("utf-8")
        ids = [N_SPECIAL + b for b in raw]
        if len(ids) < 2 or not self.merge_rank:
            return ids
        while len(ids) >= 2:
            best_i = None
            best_r = None
            for i in range(len(ids) - 1):
                rank = self.merge_rank.get((ids[i], ids[i + 1]))
                if rank is None:
                    continue
                if best_r is None or rank < best_r:
                    best_r = rank
                    best_i = i
            if best_i is None:
                break
            pair = (ids[best_i], ids[best_i + 1])
            ids = ids[:best_i] + [self.merge_to[pair]] + ids[best_i + 2 :]
        return ids

    def encode(self, text: str) -> list[int]:
        out = []
        self.fallback_count = 0
        for kind, span in route(text):
            if kind == "ind":
                ids, _ = self.indic_ids(span)
                self.fallback_count += self.indic.fallback_count
                out.extend(ids)
                continue
            if not self.trained:
                raise RuntimeError("english tail is not trained")
            i = 0
            while i < len(span):
                hit = self.match_seed(span, i)
                if hit is not None:
                    oid, nch = hit
                    out.append(oid)
                    i += nch
                    continue
                rest = span[i:]
                chunk = self.pre.pre_tokenize_str(rest)[0][0]
                out.extend(self.bpe(chunk))
                i += len(chunk)
        return out

    def is_space_keep(self, oid: int) -> bool:
        if self.t.indic_scores[oid] is None:
            return False
        piece = self.t.pieces[oid]
        return piece != "" and set(piece) == {self.indic.mark}

    def is_alias(self, oid: int) -> bool:
        if not (N_SPECIAL <= oid < N_SPECIAL + N_BYTE):
            return False
        return self.t.indic_scores[oid] is not None and not self.is_space_keep(oid)

    def is_slot(self, oid: int) -> bool:
        if self.is_space_keep(oid):
            return False
        return N_SPECIAL + N_BYTE <= oid < self.t.tail_start

    def _indic_mask(self, ids: list[int]) -> list[bool]:
        """Which ids decode with the Indic rules.

        A slot is Indic. A space mark in front of an Indic word is the dummy
        prefix of a span that already starts with a real space, so it joins
        that word and is stripped. Digits and punctuation stay on the English
        side when an English word produced them. They join Indic only when
        they continue a span that is already Indic. That is what keeps
        `pre-शब्द` and `hello123नमस्ते` from gaining a space.
        """
        n = len(ids)
        mask = [False] * n

        def slot(i: int) -> bool:
            return self.is_slot(ids[i])

        def alias(i: int) -> bool:
            return self.is_alias(ids[i])

        def space(i: int) -> bool:
            return self.is_space_keep(ids[i])

        i = 0
        while i < n:
            if slot(i):
                mask[i] = True
                i += 1
                continue
            if space(i):
                j = i
                while j < n and space(j):
                    j += 1
                prev_indic = i > 0 and mask[i - 1]
                k = j
                while k < n and alias(k):
                    k += 1
                next_slot = k < n and slot(k)
                if prev_indic or next_slot:
                    for t in range(i, j):
                        mask[t] = True
                    if next_slot and not prev_indic:
                        for t in range(j, k):
                            mask[t] = True
                i = j
                continue
            if alias(i) and i > 0 and mask[i - 1]:
                mask[i] = True
            i += 1
        return mask

    def decode(self, ids: list[int]) -> str:
        indic = self._indic_mask(ids)
        parts = []
        i = 0
        n = len(ids)
        while i < n:
            if indic[i]:
                j = i + 1
                while j < n and indic[j]:
                    j += 1
                pieces = [self.t.pieces[k] for k in ids[i:j]]
                parts.append(self.indic.decode_pieces(pieces))
                i = j
                continue
            raw = bytearray()
            j = i
            while j < n and not indic[j]:
                blob = self.t.raw_of[ids[j]]
                if blob is None:
                    raise RuntimeError(f"id {ids[j]} has no bytes")
                raw.extend(blob)
                j += 1
            parts.append(bytes(raw).decode("utf-8"))
            i = j
        return "".join(parts)

    def token_text(self, oid: int) -> str:
        if self.is_slot(oid) or self.is_alias(oid):
            return self.indic.decode_pieces([self.t.pieces[oid]])
        if self.t.raw_of[oid] is not None:
            return self.t.raw_of[oid].decode("utf-8")
        if self.is_space_keep(oid):
            return self.indic.decode_pieces([self.t.pieces[oid]])
        return self.t.pieces[oid]


def tokenizer_spec() -> dict:
    """Rules this encoder implements. The file must carry this same object."""
    if LATIN_LETTER_CATEGORIES != {"Lu", "Ll", "Lt", "Lm", "Lo"}:
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    return {
        "indic": {
            "normalization": "NFC",
            "dummy_prefix": True,
            "space_mark": "Ġ",
            "space_mark_codepoint": "U+0120",
            "ordinary_space": "each ordinary space becomes the space mark",
            "merge": "highest indic_score that exists as a piece merges first",
            "equal_scores": "equal scores merge the leftmost pair",
            "unknown_character": "a character with no piece becomes <0xHH> bytes",
            "atoms": "characters",
        },
        "router": {
            "protected_whitespace": "Protected whitespace is a tab, a newline, a carriage return, or two or more spaces. Those runs take the English path and split the text into stretches.",
            "indic_and_no_latin": "Indic letters and no Latin letters: the whole stretch takes the Indic path, including digits, punctuation, and single spaces.",
            "latin_and_no_indic": "Latin letters and no Indic letters: the whole stretch takes the English path.",
            "neither": "No Indic letters and no Latin letters: English.",
            "both_scripts": "Both scripts: a single ordinary space attaches to the following word and is not its own span. English शब्द does not gain a spurious boundary. In a word, a Latin letter is English and an Indic letter is Indic. Digits, punctuation, and other symbols attach to the run on their left. If the word starts with them, they attach to the run on their right. A word made only of them is English. Digits and punctuation encoded on the English side stay English, so they do not turn the Indic dummy prefix into a real space.",
            "latin_letter": "A Latin letter is Unicode category "
            + ", ".join(("Lu", "Ll", "Lt", "Lm"))
            + ', or Lo whose name starts with "LATIN ".',
            "indic_letter": "An Indic letter is a character in the kept Indic blocks already named in the encoder: "
            + ", ".join(sorted(KEEP_SCRIPTS))
            + ".",
            "zwj_zwnj": "U+200D and U+200C count as Indic when the nearest real letter, skipping those two characters, is Indic.",
            "cross_script": "No piece joins two scripts.",
        },
        "normalization": {
            "nfc": "NFC before routing and before the score BPE.",
            "whitespace": "Unicode space separators (category Zs) become U+0020. Tab, newline, and carriage return stay.",
            "punctuation": "Curly quotes and unicode dashes fold onto the ASCII pieces already in the vocabulary. No new piece is added.",
            "zero_width": "U+200B, U+FEFF, bidi marks, and other default-ignorable format characters are removed. U+200C and U+200D stay.",
        },
        "specials": {
            "ids_0_4": SPECIALS[:5],
            "ids_5_31": f"{SPECIALS[5]} through {SPECIALS[31]}",
            "normal_text": "encoding normal text does not emit ids 0-31",
        },
    }


def _require_tokenizer_spec(doc: dict, pieces: list[str]) -> None:
    spec = tokenizer_spec()
    if doc.get("tokenizer_spec") != spec:
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    norm = doc.get("indic_normalizer") or {}
    indic = spec["indic"]
    mark = norm.get("space_mark")
    if norm.get("form") != indic["normalization"] or norm.get("dummy_prefix") is not True:
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    if not isinstance(mark, str) or mark != indic["space_mark"]:
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    if f"U+{ord(mark):04X}" != indic["space_mark_codepoint"]:
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    if pieces[:N_SPECIAL] != SPECIALS or spec["specials"]["ids_0_4"] != SPECIALS[:5]:
        raise RuntimeError("tokenizer_spec disagrees with the encoder")


def _require_spec_behavior(enc: Encoder) -> None:
    """Refuse when the running cut rules no longer match tokenizer_spec."""
    mark = enc.indic.mark
    if enc.indic.normalize("क ख") != f"{mark}क{mark}ख":
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    folded = "\u0930\u093c"
    if enc.indic.normalize(folded) != mark + unicodedata.normalize("NFC", folded):
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    unknown = "\ue000"
    if unknown in enc.t.piece_to_id:
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    got = enc.indic.encode_pieces(unknown)
    expect = [mark] + [f"<0x{byte:02X}>" for byte in unknown.encode("utf-8")]
    if got != expect:
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    routes = {
        "नमस्ते": [("ind", "नमस्ते")],
        "hello": [("en", "hello")],
        "जा रहा": [("ind", "जा रहा")],
        "जा  रहा": [("ind", "जा"), ("en", "  "), ("ind", "रहा")],
        "main जा": [("en", "main"), ("ind", " जा")],
        "English शब्द": [("en", "English"), ("ind", " शब्द")],
        "राम, श्याम": [("ind", "राम, श्याम")],
        "नमस्ते123": [("ind", "नमस्ते123")],
        "hello123": [("en", "hello123")],
        "helloनमस्ते": [("en", "hello"), ("ind", "नमस्ते")],
        "राम\tश्याम": [("ind", "राम"), ("en", "\t"), ("ind", "श्याम")],
        "राम\nश्याम": [("ind", "राम"), ("en", "\n"), ("ind", "श्याम")],
        "राम\rश्याम": [("ind", "राम"), ("en", "\r"), ("ind", "श्याम")],
        "भारत 2026": [("ind", "भारत 2026")],
        "π का मान": [("ind", "π का मान")],
        "भारत-India": [("ind", "भारत-"), ("en", "India")],
        "भारत,India": [("ind", "भारत,"), ("en", "India")],
        "AIमें": [("en", "AI"), ("ind", "में")],
        "C++में": [("en", "C++"), ("ind", "में")],
        "भारत 2026 AI": [("ind", "भारत"), ("en", " 2026"), ("en", " AI")],
    }
    for text, rows in routes.items():
        if list(route(text)) != rows:
            raise RuntimeError("tokenizer_spec disagrees with the encoder")
        if any(oid < N_SPECIAL for oid in enc.encode(text)):
            raise RuntimeError("tokenizer_spec disagrees with the encoder")
    # Sarvam score cuts. Characters are the atoms, so हिन्दी is Ġह | िन् | दी.
    if enc.indic.encode_pieces("का") != [mark + "का"]:
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    if enc.indic.encode_pieces("कार") != [mark + "कार"]:
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    if enc.indic.encode_pieces("नमस्ते") != [mark + "नम", "स्ते"]:
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    if enc.indic.encode_pieces("हिन्दी") != [mark + "ह", "िन्", "दी"]:
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    if enc.indic.encode_pieces("ಕನ್ನಡ") != [mark + "ಕ", "ನ್ನ", "ಡ"]:
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    # A space before an Indic word is inside the Indic span, not a second cut.
    if list(route("English शब्द")) != [("en", "English"), ("ind", " शब्द")]:
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    if enc.decode(enc.encode("English शब्द")) != "English शब्द":
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    if enc.decode(enc.encode("pre-शब्द")) != "pre-शब्द":
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    if enc.decode(enc.encode("hello123नमस्ते")) != "hello123नमस्ते":
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    if enc.decode(enc.encode("C++में")) != "C++में":
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    bare = "\u200b"
    if normalize_text(bare) != "":
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    if normalize_text("a\u00a0b") != "a b":
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    if normalize_text("\u2018quote\u2019") != "'quote'":
        raise RuntimeError("tokenizer_spec disagrees with the encoder")
    if enc.decode(enc.encode("\u2018quote\u2019")) != "'quote'":
        raise RuntimeError("tokenizer_spec disagrees with the encoder")


def load_runtime(path: str) -> Encoder:
    """Read tokenizer-65k.json. Does not open tokenizer.model.

    Our id is the index in pieces. Piece strings are unique, so the space
    mark resolves to the scored Ġ id.
    """
    with open(path) as fh:
        doc = json.load(fh)
    if doc.get("indic_model") != "BPE":
        raise RuntimeError(f"indic model type is {doc.get('indic_model')!r}")
    if "sarvam_id" in doc:
        raise RuntimeError("tokenizer file still has sarvam_id")
    pieces = doc["pieces"]
    scores = doc["indic_scores"]
    if len(pieces) != VOCAB or len(scores) != VOCAB:
        raise RuntimeError("tokenizer file is not 65,536 ids")
    _require_tokenizer_spec(doc, pieces)
    if len(set(pieces)) != VOCAB:
        raise RuntimeError("piece texts are not unique")
    tables = Tables.__new__(Tables)
    tables.sp = None
    tables.pieces = pieces
    tables.sarvam_of = [None] * VOCAB
    tables.indic_scores = scores
    tables.indic_normalizer = doc["indic_normalizer"]
    tables.sarvam_piece = [None] * VOCAB
    tables.raw_of = [None] * VOCAB
    tables.K = doc["K"]
    tables.tail_start = N_SPECIAL + N_BYTE + doc["K"]
    grouped: dict[str, list[int]] = defaultdict(list)
    for oid, piece in enumerate(pieces):
        grouped[piece].append(oid)
    tables.piece_to_id = {}
    for piece, ids in grouped.items():
        if len(ids) == 1:
            tables.piece_to_id[piece] = ids[0]
            continue
        raise RuntimeError(f"ambiguous piece {piece!r}: ids {ids}")
    mark = doc["indic_normalizer"]["space_mark"]
    mark_id = tables.piece_to_id.get(mark)
    if mark_id is None or scores[mark_id] is None:
        raise RuntimeError("space mark is not the scored piece")
    for oid, piece in enumerate(pieces):
        if N_SPECIAL <= oid < N_SPECIAL + N_BYTE:
            tables.raw_of[oid] = bytes([oid - N_SPECIAL])
        elif oid >= tables.tail_start:
            tables.raw_of[oid] = bytes(U2B[ch] for ch in piece)
    enc = Encoder(tables)
    tail_start = N_SPECIAL + N_BYTE + doc["K"]
    merges = doc["english_merges"]
    if tail_start + len(merges) != VOCAB:
        raise RuntimeError("english merges do not fill the tail")
    for n, pair in enumerate(merges):
        left, right = pair
        aid = tables.piece_to_id[left]
        bid = tables.piece_to_id[right]
        nid = tail_start + n
        if pieces[nid] != left + right:
            raise RuntimeError(f"english merge {n} does not match its piece")
        enc.merge_rank[(aid, bid)] = n
        enc.merge_to[(aid, bid)] = nid
    enc.merges = merges
    for text in doc["english_seeds"]:
        stored = "".join(B2U[b] for b in text.encode("utf-8"))
        oid = tables.piece_to_id.get(stored)
        if oid is None:
            raise RuntimeError(f"english seed missing {text!r}")
        enc.add_seed_string(text, oid)
    enc.seed_strings = list(doc["english_seeds"])
    enc.trained = True
    _require_spec_behavior(enc)
    return enc


def check_router() -> None:
    def kinds(text):
        return [(k, s) for k, s in route(text)]

    expect = {
        "नमस्ते": [("ind", "नमस्ते")],
        "राम, श्याम": [("ind", "राम, श्याम")],
        "main जा रहा hoon": [
            ("en", "main"),
            ("ind", " जा रहा"),
            ("en", " hoon"),
        ],
        "English शब्द": [
            ("en", "English"),
            ("ind", " शब्द"),
        ],
        "अमेरिकी राष्ट्रपति चुनाव US": [
            ("ind", "अमेरिकी राष्ट्रपति चुनाव"),
            ("en", " US"),
        ],
        "hello जा  रहा": [
            ("en", "hello"),
            ("ind", " जा"),
            ("en", "  "),
            ("ind", "रहा"),
        ],
        "नमस्ते\nदुनिया": [
            ("ind", "नमस्ते"),
            ("en", "\n"),
            ("ind", "दुनिया"),
        ],
        "helloनमस्ते": [("en", "hello"), ("ind", "नमस्ते")],
        "नमस्ते123": [("ind", "नमस्ते123")],
        "123नमस्ते": [("ind", "123नमस्ते")],
        "वर्ष 2024 में": [("ind", "वर्ष 2024 में")],
        "hello123नमस्ते": [("en", "hello123"), ("ind", "नमस्ते")],
        "नमस्ते123hello": [("ind", "नमस्ते123"), ("en", "hello")],
    }
    for text, rows in expect.items():
        got = kinds(text)
        if got != rows:
            raise SystemExit(f"router {text!r}\n got {got}\n want {rows}")
    code = "\n    return"
    got = kinds(code)
    if got != [("en", "\n    "), ("en", "return")]:
        raise SystemExit(f"router indent {got}")
    log("router fixtures match")


def s3_client():
    import boto3

    return boto3.client("s3", region_name="us-east-1")


def list_parquet(prefix: str) -> list[str]:
    client = s3_client()
    keys = []
    token = None
    while True:
        kw = {"Bucket": BUCKET, "Prefix": prefix, "MaxKeys": 1000}
        if token:
            kw["ContinuationToken"] = token
        try:
            resp = client.list_objects_v2(**kw)
        except Exception as exc:
            raise SystemExit(f"S3 list failed for {prefix}: {type(exc).__name__}: {exc}")
        for row in resp.get("Contents", []):
            if row["Key"].endswith(".parquet"):
                keys.append(row["Key"])
        if not resp.get("IsTruncated"):
            break
        token = resp["NextContinuationToken"]
    keys.sort()
    if not keys:
        raise SystemExit(f"S3 prefix has no parquet: s3://{BUCKET}/{prefix}")
    return keys


def iter_docs(name: str, keys: list[str]):
    filesystem = pafs.S3FileSystem(region="us-east-1")
    for key in keys:
        path = f"{BUCKET}/{key}"
        try:
            pf = pq.ParquetFile(path, filesystem=filesystem)
        except Exception as exc:
            raise SystemExit(f"S3 read failed for {path}: {type(exc).__name__}: {exc}")
        row = 0
        try:
            batches = pf.iter_batches(batch_size=32, columns=["text"])
        except Exception as exc:
            raise SystemExit(f"S3 read failed for {path}: {type(exc).__name__}: {exc}")
        for batch in batches:
            col = batch.column(0)
            for i in range(len(col)):
                text = col[i].as_py()
                doc_id = f"{name}::{key}#{row}"
                row += 1
                if isinstance(text, str) and text:
                    yield doc_id, text


class SourceCursor:
    def __init__(self, name: str, prefix: str) -> None:
        self.name = name
        self.keys = list_parquet(prefix)
        self.it = iter_docs(name, self.keys)
        self.done = False
        log(f"source {name} files={len(self.keys)}")

    def next(self):
        if self.done:
            return None
        try:
            return next(self.it)
        except StopIteration:
            self.done = True
            return None
        except SystemExit:
            raise
        except Exception as exc:
            raise SystemExit(f"S3 read failed in {self.name}: {type(exc).__name__}: {exc}")


def carve_corpus() -> dict:
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    groups = {
        "en": [SourceCursor(n, p) for n, p in EN_SOURCES],
        "code": [SourceCursor(n, p) for n, p in CODE_SOURCES],
        "math": [SourceCursor(n, p) for n, p in MATH_SOURCES],
    }
    shares = {"en": 33, "code": 12, "math": 7}
    eval_f = {k: open(os.path.join(ROOT, "data", f"eval-{k}.jsonl"), "w") for k in groups}
    train_f = {k: open(os.path.join(ROOT, "data", f"train-{k}.jsonl"), "w") for k in groups}
    eval_ids = set()
    stats = {
        k: {"eval_bytes": 0, "eval_docs": 0, "train_bytes": 0, "train_docs": 0, "train_words": 0}
        for k in groups
    }
    cmd_train = Counter()
    cmd_eval = Counter()
    rr = {k: 0 for k in groups}

    def pull(bucket: str, train: bool):
        sources = groups[bucket]
        for _ in range(len(sources)):
            src = sources[rr[bucket] % len(sources)]
            rr[bucket] += 1
            if src.done:
                continue
            row = src.next()
            if row is None:
                continue
            return row
        return None

    try:
        for bucket in groups:
            while stats[bucket]["eval_bytes"] < EVAL_BYTES:
                row = pull(bucket, False)
                if row is None:
                    raise SystemExit(f"ran out of {bucket} text before the eval carve")
                doc_id, text = row
                eval_ids.add(doc_id)
                blob = json.dumps({"id": doc_id, "text": text}, ensure_ascii=False)
                eval_f[bucket].write(blob + "\n")
                stats[bucket]["eval_bytes"] += len(text.encode("utf-8"))
                stats[bucket]["eval_docs"] += 1
                if bucket == "math":
                    cmd_eval.update(CMD_RE.findall(text))
            log(f"eval {bucket} docs={stats[bucket]['eval_docs']} bytes={stats[bucket]['eval_bytes']}")

        total = 0
        while total < TARGET_BYTES:
            alive = [k for k in groups if any(not s.done for s in groups[k])]
            if not alive:
                raise SystemExit(
                    f"text ran out at {total} bytes. stats={json.dumps(stats)}"
                )
            bucket = min(alive, key=lambda k: stats[k]["train_words"] / shares[k])
            row = pull(bucket, True)
            if row is None:
                continue
            doc_id, text = row
            if doc_id in eval_ids:
                continue
            text = unicodedata.normalize("NFC", text)
            if len(text) > 4000:
                text = text[:4000]
            if not text:
                continue
            raw = text.encode("utf-8")
            train_f[bucket].write(json.dumps({"id": doc_id, "text": text}, ensure_ascii=False) + "\n")
            stats[bucket]["train_bytes"] += len(raw)
            stats[bucket]["train_docs"] += 1
            stats[bucket]["train_words"] += word_count(text)
            total += len(raw)
            if bucket == "math":
                cmd_train.update(CMD_RE.findall(text))
            if stats[bucket]["train_docs"] % 20000 == 0:
                log(f"train bytes={total} { {k: stats[k]['train_words'] for k in stats} }")
    finally:
        for fh in list(eval_f.values()) + list(train_f.values()):
            fh.close()
    words = {k: stats[k]["train_words"] for k in stats}
    log(f"corpus bytes={total} words={words}")
    meta = {
        "stats": stats,
        "missing": MISSING_SOURCES,
        "cmd_train": cmd_train.most_common(),
        "cmd_eval": cmd_eval.most_common(),
        "target_bytes": total,
    }
    with open(os.path.join(ROOT, "data", "corpus_meta.json"), "w") as fh:
        json.dump(meta, fh)
    return meta


def choose_commands(meta: dict) -> list[str]:
    train = Counter(dict(meta["cmd_train"]))
    eval_rows = meta["cmd_eval"]
    eval_total = sum(n for _, n in eval_rows)
    top90 = []
    if eval_total:
        running = 0
        for cmd, n in eval_rows:
            top90.append(cmd)
            running += n
            if running / eval_total >= 0.90:
                break
    frequent = [cmd for cmd, n in train.most_common() if n >= 50]
    required = []
    for cmd in FORCED_COMMANDS + top90:
        if cmd not in required:
            required.append(cmd)
    chosen = list(required)
    for cmd in frequent:
        if cmd in chosen:
            continue
        if len(chosen) >= 512:
            break
        chosen.append(cmd)
    chosen.sort(key=lambda cmd: (len(cmd), cmd))
    log(f"latex seeds={len(chosen)} required={len(required)} train>=50={sum(1 for c in frequent)}")
    return chosen


class Tok:
    __slots__ = ("raw", "text", "stored")

    def __init__(self, raw: bytes, stored: str) -> None:
        self.raw = raw
        self.stored = stored
        try:
            self.text = raw.decode("utf-8")
        except UnicodeDecodeError:
            self.text = None


def train_tail(tables: Tables, commands: list[str]) -> Encoder:
    enc = Encoder(tables)
    check_scissors(enc.pre)
    log("counting chunks")
    counts: Counter[str] = Counter()
    files = 0
    for name in ("en", "code", "math"):
        path = os.path.join(ROOT, "data", f"train-{name}.jsonl")
        with open(path) as fh:
            for line in fh:
                text = json.loads(line)["text"]
                for piece, _ in enc.pre.pre_tokenize_str(text):
                    counts[piece] += 1
                files += 1
                if files % 200000 == 0:
                    log(f"pretoken docs={files} types={len(counts)}")
    log(f"pretoken types={len(counts)}")
    seqs: list[array] = []
    weights: list[int] = []
    for chunk, cnt in counts.items():
        raw = chunk.encode("utf-8")
        if len(raw) < 2:
            continue
        seqs.append(array("I", list(raw)))
        weights.append(cnt)
    del counts
    log(f"sequences={len(seqs)}")
    toks: list[Tok] = []
    for b in range(256):
        toks.append(Tok(bytes([b]), B2U[b]))
    meaning = dict(tables.meaning_owner)
    pair_count: dict[tuple[int, int], int] = defaultdict(int)
    where: dict[tuple[int, int], set[int]] = defaultdict(set)

    def local_pairs(seq: array) -> dict[tuple[int, int], int]:
        local: dict[tuple[int, int], int] = {}
        for i in range(len(seq) - 1):
            pair = (seq[i], seq[i + 1])
            local[pair] = local.get(pair, 0) + 1
        return local

    for wi, seq in enumerate(seqs):
        weight = weights[wi]
        for pair, mult in local_pairs(seq).items():
            pair_count[pair] += mult * weight
            where[pair].add(wi)
    log(f"initial pairs={len(pair_count)}")

    merges: list[tuple[int, int]] = []
    rejected: set[tuple[int, int]] = set()
    raw_index: dict[bytes, int] = {tok.raw: i for i, tok in enumerate(toks)}

    def text_of(raw: bytes) -> str | None:
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            return None

    def accept(left: int, right: int) -> int | None:
        if len(toks) - N_BYTE >= tables.tail:
            return None
        raw = toks[left].raw + toks[right].raw
        if raw in raw_index:
            return None
        text = text_of(raw)
        stored = toks[left].stored + toks[right].stored
        if text is not None and (has_banned_char(text) or text in meaning):
            return None
        if text is None and stored in meaning:
            return None
        nid = len(toks)
        tok = Tok(raw, stored)
        toks.append(tok)
        raw_index[raw] = nid
        if text is not None:
            meaning[text] = nid
        meaning[stored] = nid
        merges.append((left, right))
        touched = list(where.get((left, right), ()))
        fresh: set[tuple[int, int]] = set()
        for wi in touched:
            seq = seqs[wi]
            if len(seq) < 2:
                continue
            old = local_pairs(seq)
            out = array("I")
            i = 0
            n = len(seq)
            changed = False
            while i < n:
                if i + 1 < n and seq[i] == left and seq[i + 1] == right:
                    out.append(nid)
                    i += 2
                    changed = True
                else:
                    out.append(seq[i])
                    i += 1
            if not changed:
                continue
            weight = weights[wi]
            new = local_pairs(out)
            for pair in set(old) | set(new):
                delta = (new.get(pair, 0) - old.get(pair, 0)) * weight
                if delta:
                    pair_count[pair] = pair_count.get(pair, 0) + delta
                if new.get(pair, 0):
                    where[pair].add(wi)
                    fresh.add(pair)
                elif wi in where.get(pair, ()):
                    where[pair].discard(wi)
            seqs[wi] = out
        accept.fresh = fresh
        return nid

    accept.fresh = set()

    def add_seed_text(text: str) -> None:
        raw = text.encode("utf-8")
        if raw in raw_index:
            return
        if text in meaning:
            raise SystemExit(f"seed {text!r} collides with an existing piece")
        guard = 0
        while raw not in raw_index:
            guard += 1
            if guard > 80:
                raise SystemExit(f"seed did not resolve {text!r}")
            split_at = None
            for cut in range(len(raw) - 1, 0, -1):
                li = raw_index.get(raw[:cut])
                ri = raw_index.get(raw[cut:])
                if li is not None and ri is not None:
                    split_at = (li, ri)
                    break
            if split_at is None:
                li = None
                pref = 0
                for cut in range(len(raw) - 1, 0, -1):
                    found = raw_index.get(raw[:cut])
                    if found is not None:
                        li = found
                        pref = cut
                        break
                if li is None:
                    raise SystemExit(f"no prefix for seed {text!r}")
                split_at = (li, raw[pref])
            nid = accept(split_at[0], split_at[1])
            if nid is None:
                raise SystemExit(f"seed merge rejected {text!r} pieces={split_at}")

    seed_notes = []
    for text in whitespace_seeds():
        before = len(toks)
        add_seed_text(text)
        seed_notes.append(text)
        log(f"seed {text!r} new={len(toks) - before}")
    for cmd in commands:
        before = len(toks)
        add_seed_text(cmd)
        seed_notes.append(cmd)
        if len(toks) != before:
            log(f"seed {cmd} new_tokens={len(toks) - before}")
    enc.seed_strings = list(seed_notes)
    log(f"after seeds tail_used={len(toks) - N_BYTE}/{tables.tail}")

    heap = [(-cnt, a, b) for (a, b), cnt in pair_count.items() if cnt > 0]
    heapq.heapify(heap)
    last = time.time()
    merge_cap = int(os.environ.get("TOK65_MERGE_CAP", "0"))
    limit = tables.tail if merge_cap <= 0 else min(tables.tail, merge_cap)
    while len(toks) - N_BYTE < limit:
        if not heap:
            if merge_cap > 0:
                break
            raise SystemExit(
                f"pair heap empty at tail {len(toks) - N_BYTE}/{tables.tail}. Add more text."
            )
        neg, left, right = heapq.heappop(heap)
        cnt = pair_count.get((left, right), 0)
        if cnt <= 0 or cnt != -neg:
            if cnt > 0:
                heapq.heappush(heap, (-cnt, left, right))
            continue
        if (left, right) in rejected:
            continue
        nid = accept(left, right)
        if nid is None:
            rejected.add((left, right))
            continue
        for pair in accept.fresh:
            fresh_count = pair_count.get(pair, 0)
            if fresh_count > 0:
                heapq.heappush(heap, (-fresh_count, pair[0], pair[1]))
        used = len(toks) - N_BYTE
        if used % 500 == 0 or used == tables.tail:
            now = time.time()
            log(f"merge {used}/{tables.tail} dt={now - last:.1f}s heap={len(heap)}")
            last = now
    if merge_cap <= 0 and len(toks) - N_BYTE != tables.tail:
        raise SystemExit(f"tail size {len(toks) - N_BYTE}")
    if merge_cap > 0:
        log(f"smoke stop at {len(toks) - N_BYTE}")

    # Publish onto the shared tables.
    for n, (left, right) in enumerate(merges):
        oid = tables.tail_start + n
        tok = toks[N_BYTE + n]
        tables.pieces[oid] = tok.stored
        tables.raw_of[oid] = tok.raw
        enc.merges.append([toks[left].stored, toks[right].stored])
        # internal ids to our ids
    def our_id(internal: int) -> int:
        if internal < N_BYTE:
            return N_SPECIAL + internal
        return tables.tail_start + (internal - N_BYTE)

    enc.merges = []
    enc.merge_rank = {}
    enc.merge_to = {}
    for n, (left, right) in enumerate(merges):
        a = our_id(left)
        b = our_id(right)
        nid = our_id(N_BYTE + n)
        enc.merges.append([tables.pieces[a], tables.pieces[b]])
        enc.merge_rank[(a, b)] = n
        enc.merge_to[(a, b)] = nid
        if tables.raw_of[nid] is None:
            tables.raw_of[nid] = tables.raw_of[a] + tables.raw_of[b]
            tables.pieces[nid] = tables.pieces[a] + tables.pieces[b]
    # Seed trie uses final seed strings that exist as whole tokens.
    for text in seed_notes:
        raw = text.encode("utf-8")
        found = None
        for oid in range(N_SPECIAL, VOCAB):
            if tables.raw_of[oid] == raw and tables.sarvam_piece[oid] is None:
                found = oid
                break
            if tables.raw_of[oid] == raw and text in (".",):
                found = oid
        if found is None:
            # A byte-sized seed should not happen except newline, which is a byte.
            for oid in range(N_SPECIAL, N_SPECIAL + N_BYTE):
                if tables.raw_of[oid] == raw:
                    found = oid
                    break
        if found is None:
            raise SystemExit(f"seed text missing from vocab {text!r}")
        enc.add_seed_string(text, found)
    enc.trained = True
    enc.seed_strings = seed_notes
    log(f"trained merges={len(enc.merges)}")
    return enc


def eligible_line(text: str) -> bool:
    if "\t" in text or "\n" in text or "\r" in text or "  " in text:
        return False
    has_ind = False
    for i, ch in enumerate(text):
        if is_latin_letter(ch):
            return False
        if counts_as_indic(text, i):
            has_ind = True
    return has_ind and len(text) >= 8


def load_gate1_sentences(enc: Encoder) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    filesystem = pafs.S3FileSystem(region="us-east-1")
    for lang, code in LANGS:
        prefix = f"datasets/sangraha/verified/{code}/"
        keys = list_parquet(prefix)[:2]
        got = []
        rewritten = 0
        scanned = 0
        for key in keys:
            path = f"{BUCKET}/{key}"
            try:
                pf = pq.ParquetFile(path, filesystem=filesystem)
                batches = pf.iter_batches(batch_size=16, columns=["text"])
            except Exception as exc:
                raise SystemExit(f"S3 read failed for {path}: {type(exc).__name__}: {exc}")
            for batch in batches:
                for i in range(len(batch.column(0))):
                    text = batch.column(0)[i].as_py()
                    if not isinstance(text, str):
                        continue
                    for line in re.split(r"[\n।॥]+", text):
                        line = line.strip(" \t")
                        if not eligible_line(line):
                            continue
                        if len(line) > 400:
                            line = line[:400]
                            if not eligible_line(line):
                                continue
                        scanned += 1
                        pieces = enc.reference_pieces(line)
                        back = enc.t.sp.DecodePieces(pieces)
                        if back != line:
                            rewritten += 1
                            continue
                        got.append(line)
                        if len(got) >= 120:
                            break
                    if len(got) >= 120:
                        break
                if len(got) >= 120:
                    break
            if len(got) >= 120:
                break
        log(f"gate1 pool {lang} usable={len(got)} sarvam_rewrites_skipped={rewritten} scanned={scanned}")
        if len(got) < 20:
            raise SystemExit(f"{lang} has {len(got)} round-tripping sentences")
        out[lang] = got[:100] if len(got) >= 100 else got
    return out


def run_gate1(enc: Encoder, sentences: dict[str, list[str]]) -> dict:
    report = {"languages": {}, "fixtures": {}}
    for word, expect in FIXTURES.items():
        ids, pieces = enc.indic_ids(word)
        if pieces != expect:
            raise SystemExit(f"fixture {word} pieces {pieces} != {expect}")
        if enc.decode(ids) != word:
            raise SystemExit(f"fixture {word} did not round-trip")
        report["fixtures"][word] = pieces
    for lang, rows in sentences.items():
        for sent in rows:
            ids, pieces = enc.indic_ids(sent)
            orig = enc.reference_pieces(sent)
            if pieces != orig:
                raise SystemExit(f"{lang} piece mismatch {sent!r} {pieces!r} {orig!r}")
            if enc.decode(ids) != enc.t.sp.DecodePieces(orig):
                raise SystemExit(f"{lang} decode mismatch {sent!r}")
        report["languages"][lang] = len(rows)
    path = os.path.join(ROOT, "gate1.json")
    with open(path, "w") as fh:
        json.dump({"sentences": sentences, "report": report}, fh, ensure_ascii=False)
    log(f"gate 1 passed {report['languages']}")
    return report


def token_texts(enc: Encoder, text: str) -> list[str]:
    return [enc.token_text(i) for i in enc.encode(text)]


def run_gates(enc: Encoder, meta: dict, digest: str) -> dict:
    sentences = json.load(open(os.path.join(ROOT, "gate1.json")))["sentences"]
    # Gate 2
    indent_cases = {
        "\n": "\n",
        "\n  ": "\n  ",
        "\n    ": "\n    ",
        "\n\t": "\n\t",
    }
    g2 = {}
    for text, want in indent_cases.items():
        ids = enc.encode(text)
        texts = [enc.token_text(i) for i in ids]
        if texts != [want]:
            raise SystemExit(f"gate 2 indent {text!r} -> {texts!r}")
        if "▁" in texts[0]:
            raise SystemExit("gate 2 indent contains the space mark")
        g2[repr(text)] = texts
    ids = enc.encode("\n    return")
    texts = [enc.token_text(i) for i in ids]
    if not texts or texts[0] != "\n    " or "▁" in texts[0] or "".join(texts) != "\n    return":
        raise SystemExit(f"gate 2 return line {texts!r}")
    g2["newline-four-spaces-return"] = texts
    # Recompute the top-90 command list for the gate report.
    eval_rows = meta["cmd_eval"]
    total = sum(n for _, n in eval_rows) or 1
    running = 0
    top90 = []
    for cmd, n in eval_rows:
        top90.append(cmd)
        running += n
        if running / total >= 0.90:
            break
    must = []
    for cmd in FORCED_COMMANDS + top90:
        if cmd not in must:
            must.append(cmd)
    for cmd in must:
        ids = enc.encode(cmd)
        texts = [enc.token_text(i) for i in ids]
        if texts != [cmd]:
            raise SystemExit(f"gate 2 command {cmd} -> {texts!r}")
    g2["commands_one_token"] = must
    log(f"gate 2 passed commands={len(must)}")

    # Gate 3
    g3 = {}
    for name in ("en", "code", "math"):
        path = os.path.join(ROOT, "data", f"eval-{name}.jsonl")
        ours = sar = words = 0
        with open(path) as fh:
            for line in fh:
                text = json.loads(line)["text"]
                words += word_count(text)
                ours += len(enc.encode(text))
                pieces = enc.reference_pieces(text)
                sar += len(pieces)
        if words == 0:
            raise SystemExit(f"gate 3 empty {name}")
        row = {
            "words": words,
            "ours": ours,
            "sarvam": sar,
            "ours_per_word": ours / words,
            "sarvam_per_word": sar / words,
        }
        if not (ours / words < sar / words):
            raise SystemExit(f"gate 3 failed {name} {row}")
        g3[name] = row
        log(f"gate 3 {name} ours={row['ours_per_word']:.4f} sarvam={row['sarvam_per_word']:.4f}")

    # Gate 4
    broken = 0
    for lang, rows in sentences.items():
        for sent in rows:
            ids = enc.encode(sent)
            orig = set(enc.reference_pieces(sent))
            for oid in ids:
                if enc.t.sarvam_piece[oid] is None:
                    text = enc.token_text(oid)
                    if any(counts_as_indic(text, i) for i, _ch in enumerate(text)):
                        raise SystemExit(f"gate 4 english token has Indic {text!r}")
                    try:
                        text.encode("utf-8").decode("utf-8")
                    except UnicodeError:
                        broken += 1
                else:
                    if enc.t.sarvam_piece[oid] not in orig:
                        raise SystemExit("gate 4 sarvam token was not in the original pieces")
    if broken:
        raise SystemExit(f"gate 4 broken utf-8 {broken}")
    log(f"gate 4 passed vowel_mark_starts={enc.t.vowel_mark_pieces}")

    # Gate 5
    mismatches = 0
    fixtures = [
        "नमस्ते",
        "राम, श्याम",
        "main जा रहा hoon",
        "helloनमस्ते",
        "नमस्ते123",
        "123नमस्ते",
        "वर्ष 2024 में",
        "\n    return",
        "\\frac{1}{2}",
        "def f():\n    return 1\n",
    ]
    for text in fixtures:
        back = enc.decode(enc.encode(text))
        if back != text:
            raise SystemExit(f"gate 5 fixture mismatch {text!r} -> {back!r}")
    py = "def f():\n    return 1\n"
    py_texts = token_texts(enc, py)
    if "\n    " not in py_texts:
        raise SystemExit(f"gate 5 python indent missing {py_texts!r}")
    for lang, rows in sentences.items():
        for sent in rows:
            if enc.decode(enc.encode(sent)) != sent:
                mismatches += 1
    for name in ("code", "math", "en"):
        path = os.path.join(ROOT, "data", f"eval-{name}.jsonl")
        with open(path) as fh:
            for line in fh:
                text = json.loads(line)["text"]
                if enc.decode(enc.encode(text)) != text:
                    mismatches += 1
                    if mismatches > 5:
                        raise SystemExit("gate 5 too many mismatches")
    if mismatches:
        raise SystemExit(f"gate 5 mismatches {mismatches}")
    log("gate 5 passed")

    # Gate 6
    if sum(1 for p in enc.t.pieces if p != "") != VOCAB:
        # tail and specials and bytes and kept should fill every slot
        empty = [i for i, p in enumerate(enc.t.pieces) if p == ""]
        raise SystemExit(f"gate 6 empty ids {empty[:8]} count={len(empty)}")
    meanings = []
    seen = set()
    for oid, piece in enumerate(enc.t.pieces):
        if enc.t.raw_of[oid] is not None:
            try:
                meaning = enc.t.raw_of[oid].decode("utf-8")
            except UnicodeDecodeError:
                meaning = piece
        else:
            meaning = piece
        if meaning in seen:
            raise SystemExit(f"gate 6 duplicate text {meaning!r} id {oid}")
        seen.add(meaning)
        meanings.append(meaning)
    unk = 0
    for name in ("en", "code", "math"):
        path = os.path.join(ROOT, "data", f"eval-{name}.jsonl")
        with open(path) as fh:
            for line in fh:
                text = json.loads(line)["text"]
                unk += enc.encode(text).count(0)
    if unk:
        raise SystemExit(f"gate 6 unk count {unk}")
    log("gate 6 passed")

    # Gate 7
    cross = 0
    fp = Counter()
    for oid in range(N_SPECIAL + N_BYTE, VOCAB):
        if enc.t.sarvam_piece[oid] is not None:
            text = enc.t.sarvam_piece[oid]
        elif enc.t.raw_of[oid] is not None:
            try:
                text = enc.t.raw_of[oid].decode("utf-8")
            except UnicodeDecodeError:
                continue
        else:
            text = enc.t.pieces[oid]
        fams = set()
        for ch in text:
            if ch == "▁" or ch.isspace():
                continue
            cat = unicodedata.category(ch)
            if cat[:1] in {"N", "P", "S", "Z", "C"}:
                continue
            if is_latin_letter(ch):
                fams.add("latin")
                continue
            name = script_of(ch)
            if name:
                fams.add(name)
        if len(fams) > 1 or (fams & DROP_SCRIPTS):
            cross += 1
        if len(fams) == 1 and enc.t.sarvam_piece[oid] is not None:
            fp[next(iter(fams))] += 1
    if cross:
        raise SystemExit(f"gate 7 cross-script {cross}")
    for name, expect in (
        ("devanagari", 12126),
        ("telugu", 5916),
        ("kannada", 5693),
        ("bengali", 5299),
        ("gujarati", 5274),
        ("tamil", 5100),
    ):
        if enc.t.fingerprint.get(name) != expect:
            raise SystemExit(f"gate 7 fingerprint {name} {enc.t.fingerprint.get(name)}")
    log("gate 7 passed")
    return {
        "gate2": g2,
        "gate3": g3,
        "gate4": {"broken_utf8": 0, "vowel_mark_starts": enc.t.vowel_mark_pieces},
        "gate5": {"mismatches": 0},
        "gate7": {"cross_script": 0, "fingerprint": enc.t.fingerprint},
        "commands": must,
        "frozen_sha256": digest,
    }


def write_artifacts(enc: Encoder, meta: dict, gates: dict, digest: str) -> None:
    payload = {
        "vocab_size": VOCAB,
        "license_notice": "Licensed by Sarvam AI under the Sarvam AI Research License. This file is a modified derivative: Indic piece strings are unchanged. Indic cuts are the BPE scores in this file. It is not an official Sarvam product.",
        "K": enc.t.K,
        "U": enc.t.U,
        "english_tail": enc.t.tail,
        "pieces": enc.t.pieces,
        "indic_model": "BPE",
        "indic_normalizer": enc.t.indic_normalizer,
        "tokenizer_spec": tokenizer_spec(),
        "indic_scores": enc.t.indic_scores,
        "bytes_to_unicode": [B2U[b] for b in range(256)],
        "english_merges": enc.merges,
        "english_scissors": SCISSORS,
        "english_seeds": enc.seed_strings,
    }
    path = os.path.join(ROOT, "tokenizer-65k.json")
    with open(path, "w") as fh:
        json.dump(payload, fh, ensure_ascii=False)
    file_sha = sha_file(path)
    model_sha = sha_file(MODEL_PATH)
    g1 = json.load(open(os.path.join(ROOT, "gate1.json")))["report"]
    g3 = gates["gate3"]
    lines = [
        "# Tokenizer 65,536 freeze",
        "",
        "Licensed by Sarvam AI under the Sarvam AI Research License. Indic piece strings were not rewritten. Indic cuts now come from BPE scores inside `tokenizer-65k.json`. This is not an official Sarvam product.",
        "",
        f"- sha256 of the original Sarvam `tokenizer.model`: `{model_sha}`",
        f"- sha256 of `tokenizer-65k.json`: `{file_sha}`",
        f"- sha256 of `frozen_indic_ids.json`: `{digest}`",
        f"- K = {enc.t.K}. U = {enc.t.U}. English tail = {enc.t.tail}. That is 65,536 − 32 − 256 − {enc.t.K}.",
        "",
        "## Gate 1",
        "",
        "Piece strings match original Sarvam on every round-tripping sentence, ignoring a leading `<s>` and a trailing `</s>` on Sarvam’s side only.",
        "",
    ]
    for lang, n in g1["languages"].items():
        lines.append(f"- {lang}: {n} sentences")
    lines.append("")
    for word, pieces in g1["fixtures"].items():
        lines.append(f"- `{word}` → {' + '.join(pieces)}")
    lines += ["", "## Gate 2", ""]
    for key, texts in gates["gate2"].items():
        if key == "commands_one_token":
            continue
        lines.append(f"- {key}: {' | '.join(repr(t) for t in texts)}")
    lines.append("- Each of these is one token: " + ", ".join(f"`{c}`" for c in gates["commands"]))
    lines += ["", "## Gate 3", "", "Tokens per word on the held-out files.", ""]
    for name in ("en", "code", "math"):
        row = g3[name]
        lines.append(
            f"- {name}: ours {row['ours_per_word']:.4f} ({row['ours']} tokens / {row['words']} words), "
            f"original Sarvam {row['sarvam_per_word']:.4f} ({row['sarvam']} tokens / {row['words']} words)"
        )
    lines += [
        "",
        "## Gate 4",
        "",
        f"- Broken UTF-8 tokens: {gates['gate4']['broken_utf8']}",
        f"- Frozen Sarvam pieces that start with a dependent vowel mark: {gates['gate4']['vowel_mark_starts']}",
        "",
        "## Gate 5",
        "",
        f"- Round-trip mismatches: {gates['gate5']['mismatches']}",
        "",
        "## Gate 7",
        "",
        f"- Cross-script pieces: {gates['gate7']['cross_script']}",
        "",
        "## Training text",
        "",
    ]
    for note in MISSING_SOURCES:
        lines.append(f"- {note}")
    st = meta["stats"]
    for name in ("en", "code", "math"):
        lines.append(
            f"- {name}: train {st[name]['train_bytes']} UTF-8 bytes, {st[name]['train_words']} words, "
            f"{st[name]['train_docs']} documents; eval {st[name]['eval_bytes']} bytes"
        )
    note_path = os.path.join(ROOT, "tokenizer-65k-freeze.md")
    with open(note_path, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    log(f"wrote {path} sha256={file_sha}")
    log(f"wrote {note_path}")


def load_meta_commands() -> dict:
    with open(os.path.join(ROOT, "data", "corpus_meta.json")) as fh:
        meta = json.load(fh)
    meta["cmd_train"] = meta["cmd_train"]
    meta["cmd_eval"] = meta["cmd_eval"]
    return meta


def main() -> None:
    os.makedirs(ROOT, exist_ok=True)
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    check_router()
    if not os.path.exists(MODEL_PATH):
        raise SystemExit(f"missing {MODEL_PATH}")
    model_sha = sha_file(MODEL_PATH)
    if model_sha != "4cd33409a577e8b416247587b0f5bd7a3eec245a1f18d4ec7793ff299ad3fbe2":
        raise SystemExit(f"tokenizer.model sha256 is {model_sha}")
    tables = Tables()
    tables.build()
    digest = tables.write_frozen()
    enc = Encoder(tables)
    check_scissors(enc.pre)
    if stage == "freeze":
        return
    sentences_path = os.path.join(ROOT, "gate1.json")
    if stage in {"all", "gate1"} and not os.path.exists(sentences_path):
        sentences = load_gate1_sentences(enc)
        run_gate1(enc, sentences)
    elif os.path.exists(sentences_path):
        log("gate 1 checkpoint present")
    if stage == "gate1":
        return
    meta_path = os.path.join(ROOT, "data", "corpus_meta.json")
    if stage in {"all", "data"} and not os.path.exists(meta_path):
        carve_corpus()
    if stage == "data":
        return
    if stage == "smoke":
        os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
        samples = {
            "en": "The quick brown fox jumps over the lazy dog.\n" * 50,
            "code": "def f():\n    return 1\n\n" * 40,
            "math": "The value is \\frac{1}{2} and \\partial x plus \\circ and \\subseteq and \\setminus.\n" * 40,
        }
        for name, text in samples.items():
            with open(os.path.join(ROOT, "data", f"train-{name}.jsonl"), "w") as fh:
                fh.write(json.dumps({"id": name, "text": text}) + "\n")
        meta = {
            "stats": {},
            "cmd_train": [["\\frac", 40], ["\\partial", 40], ["\\circ", 40], ["\\subseteq", 40], ["\\setminus", 40]],
            "cmd_eval": [["\\frac", 10], ["\\partial", 10]],
        }
        enc = train_tail(tables, choose_commands(meta))
        sample = "\n    return \\frac{1}{2}"
        ids = enc.encode(sample)
        back = enc.decode(ids)
        log(f"smoke encode {enc.token_text(ids[0])!r} round {back == sample}")
        if back != sample or enc.token_text(ids[0]) != "\n    ":
            raise SystemExit(f"smoke failed { [enc.token_text(i) for i in ids] !r} {back!r}")
        return
    meta = load_meta_commands()
    commands = choose_commands(meta)
    if stage in {"all", "train"}:
        enc = train_tail(tables, commands)
        # stash encoder state by running gates immediately
        gates = run_gates(enc, meta, digest)
        write_artifacts(enc, meta, gates, digest)
    log("done")


if __name__ == "__main__":
    main()
