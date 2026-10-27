"""Apps: how each service's threads and documents render into files in the sandbox.

An app is a class registered by name. Thread apps render each thread to one file of exchanges; document apps render
each document's latest visible version. Adding a service means adding a class here.
"""
from __future__ import annotations

import csv
import io
from dataclasses import dataclass

from .schema import Document, Episode, Exchange, Thread, fmt, seconds

REGISTRY: dict[str, "App"] = {}


def register(cls):
    REGISTRY[cls.name] = cls()
    return cls


class App:
    name: str = ""
    kind: str = "thread"        # or "document"
    root: str = ""              # sandbox folder
    ext: str = ".md"
    label: str = ""             # how the feed names one of its items

    def file_for(self, path: str) -> str:
        return f"/world/{self.root}/{path}{self.ext}"


def _who(ep: Episode, pid: str) -> str:
    if pid == "worker":
        return f"{ep.worker.name} <{ep.worker.email}>"
    c = next((c for c in ep.contacts if c.id == pid), None)
    if not c:
        return pid
    return f"{c.name} <{c.email}>" if c.email else f"{c.name} ({c.role}, {c.org})"


def _attach(ep: Episode, x: Exchange) -> str:
    if not x.attachments:
        return ""
    paths = []
    for a in x.attachments:
        d = next(d for d in ep.documents if d.id == a)
        paths.append(document_file(d))
    return "\nAttachments: " + ", ".join(paths)


class ThreadApp(App):
    kind = "thread"

    def render(self, ep: Episode, t: Thread, upto: int) -> str:
        xs = [x for x in t.exchanges if seconds(x.at) <= upto]
        head = f"# {t.title}\n"
        state = t.state_at(upto)
        if state:
            head += "State: " + ", ".join(f"{k}={v}" for k, v in state.items()) + "\n"
        return head + "\n".join(self.exchange(ep, x) for x in xs) + "\n"

    def exchange(self, ep: Episode, x: Exchange) -> str:
        return f"\n## {fmt(seconds(x.at))} {_who(ep, x.author)}\n{x.body}{_attach(ep, x)}\n"


@register
class Mail(ThreadApp):
    name, root, label = "mail", "mail", "email"

    def exchange(self, ep, x):
        lines = [f"\n---\nFrom: {_who(ep, x.author)}"]
        if x.to:
            lines.append("To: " + ", ".join(_who(ep, p) for p in x.to))
        if x.cc:
            lines.append("Cc: " + ", ".join(_who(ep, p) for p in x.cc))
        lines.append(f"Date: {fmt(seconds(x.at))}")
        if x.subject:
            lines.append(f"Subject: {x.subject}")
        return "\n".join(lines) + f"\n\n{x.body}{_attach(ep, x)}\n"


@register
class Chat(ThreadApp):
    name, root, label = "chat", "chat", "chat"


@register
class Tickets(ThreadApp):
    name, root, label = "tickets", "tickets", "ticket"


@register
class Phone(ThreadApp):
    name, root, label = "phone", "phone", "call"

    def exchange(self, ep, x):
        if x.meta.get("case_note"):
            return f"\n## {fmt(seconds(x.at))} Case note ({_who(ep, x.author)})\n{x.body}\n"
        return super().exchange(ep, x)


@register
class News(ThreadApp):
    name, root, label = "news", "news", "news item"


@register
class Reviews(ThreadApp):
    name, root, label = "reviews", "repo/.reviews", "pull request"


class DocumentApp(App):
    kind = "document"


def document_file(d: Document) -> str:
    app = REGISTRY[d.app]
    ext = "" if "." in d.path.rsplit("/", 1)[-1] else "." + d.format
    return f"/world/{app.root}/{d.path}{ext}"


@register
class Docs(DocumentApp):
    name, root, label = "docs", "docs", "document"


@register
class Calendar(DocumentApp):
    name, root, label = "calendar", "calendar", "calendar entry"


@register
class Records(DocumentApp):
    name, root, label = "records", "records", "record"


@register
class Policies(DocumentApp):
    name, root, label = "policies", "policies", "policy"


@register
class Contacts(DocumentApp):
    name, root, label = "contacts", "contacts", "contact list"


@register
class Repo(DocumentApp):
    name, root, label = "repo", "repo", "file"


def latest(d: Document, upto: int):
    vs = [v for v in d.versions if seconds(v.at) <= upto]
    return vs[-1] if vs else None


def xlsx_bytes(csv_text: str) -> bytes:
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    for row in csv.reader(io.StringIO(csv_text)):
        out = []
        for cell in row:
            try:
                out.append(float(cell.replace(",", "")) if cell and cell.replace(",", "").replace(".", "", 1).lstrip("-").isdigit() else cell)
            except ValueError:
                out.append(cell)
        ws.append(out)
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


@dataclass
class FileOut:
    path: str
    data: bytes


def thread_file(t: Thread) -> str:
    return REGISTRY[t.app].file_for(t.path)


def render_world(ep: Episode, upto: int) -> dict[str, FileOut]:
    """Every file the assistant can see at simulated second `upto`."""
    out: dict[str, FileOut] = {}
    for t in ep.threads:
        if any(seconds(x.at) <= upto for x in t.exchanges):
            p = thread_file(t)
            out[p] = FileOut(p, REGISTRY[t.app].render(ep, t, upto).encode())
    for d in ep.documents:
        v = latest(d, upto)
        if v is None:
            continue
        p = document_file(d)
        data = xlsx_bytes(v.content) if d.format == "xlsx" else v.content.encode()
        out[p] = FileOut(p, data)
    people = io.StringIO()
    w = csv.writer(people)
    w.writerow(["id", "name", "role", "org", "email", "phone", "relation"])
    w.writerow(["worker", ep.worker.name, ep.worker.title, ep.employer.name, ep.worker.email, "", "you assist this person"])
    for c in ep.contacts:
        w.writerow([c.id, c.name, c.role, c.org, c.email or "", c.phone or "", c.relation])
    out["/world/contacts.csv"] = FileOut("/world/contacts.csv", people.getvalue().encode())
    return out
