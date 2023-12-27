from promptmodel import init
from promptmodel import PromptModel, ChatModel
from promptmodel.types.response import PromptModelConfig
from datetime import datetime

init(use_cache=True)

text = "hello, world!"

res = PromptModel("summarize").run({"text": text})
print(res.raw_output)

print(res.pm_detail)


deployed_version_config: PromptModelConfig = PromptModel(
    "summarize", version="deploy"
).get_config()

print("DEPLOYED PROMPT")
print(deployed_version_config)


version_2_config: PromptModelConfig = PromptModel("summarize", version=2).get_config()

print("VERSION 2 PROMPT")
print(version_2_config)


latest_version_config: PromptModelConfig = PromptModel(
    "summarize", version="latest"
).get_config()

print("LATEST VERSION PROMPT")
print(latest_version_config)


import asyncio

log_uuid = asyncio.run(
    PromptModel("summarize").log(
        latest_version_config.version_uuid,
        res.api_response,
        inputs={"text": text},
        metadata={"time": datetime.now().isoformat()},
    )
)

asyncio.run(
    PromptModel("summarize").log_score(
        "d9ed8b03-faf3-44a2-a4e2-5316b57ee9af",
        score={"bleu": 2},
    )
)
