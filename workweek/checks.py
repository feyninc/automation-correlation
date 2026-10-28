"""The shared check evaluator: does a proposal match a need's or a trap's predicate?

Matching is case-insensitive on word boundaries, with numbers normalized ($, commas, trailing zeros), so "320" does
not match "3,200"; `number_equals` also reads "$50k" and "$11.5M" as 50,000 and 11,500,000 (as well as 50 and 11.5). A proposal matches if any of its drafts does. `number_equals` compares every number in a draft with
the value within `tol`.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .schema import seconds

_DIGITS = r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?"   # 1,234.50 or 1234.5; a comma not followed by 3 digits ends the number
_NUM = re.compile(r"(?<![\w.])[-−]?\$?" + _DIGITS + r"(?:%|\s?(?:[kKM]|thousand|million)\b)?")
_SCALE = {"k": 1e3, "K": 1e3, "thousand": 1e3, "M": 1e6, "million": 1e6}


@dataclass
class Draft:
    text: str
    to: list[str] = field(default_factory=list)     # contact ids
    cc: list[str] = field(default_factory=list)
    subject: str = ""


@dataclass
class Prop:
    t: int                     # simulated seconds
    app: str                   # app of the target ("" for new)
    path: str                  # target path inside the app ("" for new)
    target: str                # thread or document id ("" for new)
    action: str
    drafts: list[Draft]


def numbers(text: str) -> list[float]:
    out = []
    for m in _NUM.findall(text):
        s = m.replace("$", "").replace(",", "").replace("−", "-").rstrip("%")
        unit = re.search(r"\s?([kKM]|thousand|million)$", s)
        try:
            x = float(s[:unit.start()] if unit else s)
        except ValueError:
            continue
        out.append(x)                                   # "$4.82M" is 4.82 (as a figure in millions) and 4,820,000
        if unit:
            out.append(round(x * _SCALE[unit.group(1)], 6))
    return out


def _norm(text: str, strip_commas: bool = True) -> str:
    def fix(m):
        s = m.group(0).replace(",", "") if strip_commas else m.group(0)
        if "." in s:
            s = s.rstrip("0").rstrip(".")
        return s
    return re.sub(_DIGITS if strip_commas else r"\d+(?:\.\d+)?", fix, text.lower())


def _plain(text: str) -> str:
    """Curly quotes as straight ones, every dash as a hyphen, and a hyphen between words as a space ("can’t" is "can't",
    "0–10" is "0-10", "vendor-master" is "vendor master")."""
    text = text.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    text = re.sub("[\u2010\u2011\u2013\u2014]", "-", text)
    return re.sub(r"(?<=[^\W\d_])-(?=[^\W\d_])", " ", text)


def mentions(text: str, term: str) -> bool:
    """Whole-word, case-insensitive; numbers match with or without thousands commas and trailing zeros."""
    text, term = _plain(text), _plain(term)
    for strip in (True, False):
        t, q = _norm(text, strip), _norm(term, strip).strip()
        if q and re.search(r"(?<![\w])" + re.escape(q) + r"(?![\w])", t):
            return True
    return False


def _draft_text(d: Draft) -> str:
    return f"{d.subject}\n{d.text}"


def leaf(key: str, val, p: Prop, d: Draft) -> bool:
    if key == "app":
        return p.app == val
    if key == "path":
        return p.path == val
    if key == "path_prefix":
        return p.path.startswith(val)
    if key == "target":
        return p.target == val or (isinstance(val, list) and p.target in val)
    if key == "action_in":
        return p.action in val
    if key == "to_includes":
        return val in d.to or val in d.cc
    if key == "before":
        return p.t <= seconds(val)
    if key == "after":
        return p.t >= seconds(val)
    if key == "mentions_all":
        return all(mentions(_draft_text(d), v) for v in val)
    if key == "mentions_any":
        return any(mentions(_draft_text(d), v) for v in val)
    if key == "number_equals":
        v, tol = float(val["value"]), float(val.get("tol", 0.005))
        return any(abs(x - v) <= tol for x in numbers(_draft_text(d)))
    raise ValueError(f"unknown predicate {key}")


def _eval(pred: dict, p: Prop, d: Draft) -> bool:
    (k, v), = pred.items()
    if k == "all":
        return all(_eval(q, p, d) for q in v)
    if k == "any":
        return any(_eval(q, p, d) for q in v)
    if k == "not":
        return not _eval(v, p, d)
    return leaf(k, v, p, d)


def matches(pred: dict, p: Prop) -> int | None:
    """Index of the first draft that matches, or None."""
    for i, d in enumerate(p.drafts):
        if _eval(pred, p, d):
            return i
    return None


def leaves(pred: dict):
    (k, v), = pred.items()
    if k in ("all", "any"):
        for q in v:
            yield from leaves(q)
    elif k == "not":
        yield from leaves(v)
    else:
        yield k, v


THREAD_APPS = {"mail", "chat", "tickets", "phone", "news", "reviews"}


def normalize_action(app: str, action: str) -> str:
    """Models name the same act differently: anything that adds to a thread is a reply (a line on a call stays
    "say"); anything that changes a document is an edit."""
    if action in ("flag", "new", "forward", "schedule"):
        return action
    if app == "phone":
        return "say" if action in ("say", "reply") else action
    if app in THREAD_APPS:
        return "reply"
    if app:
        return "edit"
    return action
