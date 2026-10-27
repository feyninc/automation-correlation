"""Small patches to Inspect's providers for routes it does not cover.

GLM on Bedrock: Inspect sends reasoning settings to Bedrock only for Claude and Nova. Z.ai's models on Bedrock take
an OpenAI-style `reasoning_effort` in additionalModelRequestFields (only "high" turns thinking on; see
docs/reasoning.md), so pass it through for `zai.` model ids.
"""
from inspect_ai.model._providers import bedrock as _bedrock

_orig = _bedrock.BedrockAPI.reasoning_config


def _reasoning_config(self, config):
    out = _orig(self, config)
    name = self.model_name.split("/")[-1]
    if name.startswith(("zai.", "global.zai.", "us.zai.")) and config.reasoning_effort:
        out = {**out, "reasoning_effort": config.reasoning_effort}
    return out


_bedrock.BedrockAPI.reasoning_config = _reasoning_config
