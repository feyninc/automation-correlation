ME = "c_marisol"


def item(id, channel, kind, at, thread, frm, subject, body, to=None, cc=None, attachments=None, meta=None):
    return {"id": id, "channel": channel, "kind": kind, "at": at, "thread": thread, "from": frm,
            "to": to if to is not None else [ME], "cc": cc or [], "subject": subject, "body": body,
            "attachments": attachments or [], "meta": meta or {}}


def act(id, at, verb, target, content, note, visible=True, **extra):
    a = {"id": id, "at": at, "verb": verb, "target": target, "content": content, "visible_to_model": visible, "note": note}
    a.update(extra)
    return a


def call(id, at, caller, purpose, turns, screen_pop=None):
    c = {"id": id, "at": at, "caller": caller, "purpose": purpose,
         "turns": [{"speaker": s, "text": t, "patience_s": p} for s, t, p in turns]}
    if screen_pop:
        c["screen_pop"] = screen_pop
    return c


C, H = "caller", "human"
