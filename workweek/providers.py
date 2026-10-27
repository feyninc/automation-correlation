"""Small patches to Inspect's providers for routes it does not cover.

GLM on Bedrock: Inspect sends reasoning settings to Bedrock only for Claude and Nova. Z.ai's models on Bedrock take
an OpenAI-style `reasoning_effort` in additionalModelRequestFields (only "high" turns thinking on; see
docs/design.md, section 7), so pass it through for `zai.` model ids. Kimi K3 on Bedrock accepts it the same way (it thinks at every setting, as on
Moonshot's own API), so it is passed for `moonshotai.` ids too, keeping the setting on every call.

GLM tool calls in text: GLM-4.7 and GLM-5 on Bedrock sometimes writes a tool call in its native syntax
(`<tool_call>name<arg_key>k</arg_key><arg_value>v</arg_value></tool_call>`) as text instead of a structured call.
`recover_tool_calls` turns that text into tool calls; the engine counts each recovery.
"""
import json
import re
import uuid

from inspect_ai.model._providers import bedrock as _bedrock
from inspect_ai.tool import ToolCall

_CALL = re.compile(r"<tool_call>\s*([\w.-]+)\s*(.*?)</tool_call>", re.S)
_ARG = re.compile(r"<arg_key>(.*?)</arg_key>\s*<arg_value>(.*?)</arg_value>", re.S)

_orig = _bedrock.BedrockAPI.reasoning_config


def _reasoning_config(self, config):
    out = _orig(self, config)
    name = self.model_name.split("/")[-1]
    if re.sub(r"^(global|us)\.", "", name).startswith(("zai.", "moonshotai.")) and config.reasoning_effort:
        out = {**out, "reasoning_effort": config.reasoning_effort}
    return out


_bedrock.BedrockAPI.reasoning_config = _reasoning_config


def recover_tool_calls(text: str, known: set[str]) -> list[ToolCall]:
    """Tool calls written as GLM-syntax text, for tools in `known`."""
    out = []
    for name, body in _CALL.findall(text or ""):
        if name not in known:
            continue
        args = {}
        for k, v in _ARG.findall(body):
            try:
                args[k.strip()] = json.loads(v)
            except ValueError:
                args[k.strip()] = v
        out.append(ToolCall(id=f"recovered-{uuid.uuid4().hex[:12]}", function=name, arguments=args))
    return out
