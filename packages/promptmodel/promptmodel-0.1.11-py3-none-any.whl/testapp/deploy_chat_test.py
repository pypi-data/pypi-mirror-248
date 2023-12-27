from promptmodel import init
from promptmodel import ChatModel
from promptmodel.types.response import PromptModelConfig, ChatModelConfig
from datetime import datetime

init(use_cache=False)

chat = ChatModel("weather_bot")
chat.add_messages([{"role": "user", "content": "hello"}])
res = chat.run(stream=False)
# for r in res:
#     print(r)
print(res)

deployed_version_config: ChatModelConfig = ChatModel(
    "weather_bot", version="deploy"
).get_config()

print("DEPLOYED PROMPT")
print(deployed_version_config.system_prompt)


version_2_config: ChatModelConfig = ChatModel("weather_bot", version=2).get_config()

print("VERSION 2 PROMPT")
print(version_2_config.system_prompt)


latest_version_config: ChatModelConfig = ChatModel(
    "weather_bot", version="latest"
).get_config()

print("LATEST VERSION PROMPT")
print(latest_version_config.system_prompt)

session_uuid = chat.session_uuid
import asyncio

log_uuid_list = asyncio.run(
    chat.log(
        messages=[{"role": "user", "content": "hello"}],
        metadata={"timestamp": datetime.now().isoformat()},
    )
)
print(log_uuid_list)

asyncio.run(
    chat.log_score(
        score={"bleu": 1},
    )
)

asyncio.run(
    chat.log_score(
        log_uuid=log_uuid_list[0],
        score={"bleu": 1},
    )
)

log_uuid_list = asyncio.run(
    chat.log(
        openai_api_response=res.api_response,
        metadata={"timestamp": datetime.now().isoformat()},
    )
)
print(log_uuid_list)

asyncio.run(
    chat.log_score(
        log_uuid=log_uuid_list[0],
        score={"bleu": 1},
    )
)

log_uuid_list = asyncio.run(
    chat.log(
        openai_api_response=res.api_response,
        messages=[{"role": "user", "content": "hello"}],
        metadata={"timestamp": datetime.now().isoformat()},
    )
)
