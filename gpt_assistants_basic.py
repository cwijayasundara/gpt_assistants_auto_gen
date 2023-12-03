import logging
import os

from autogen import config_list_from_json
from autogen import AssistantAgent
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen import UserProxyAgent

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

assistant_id = os.environ.get("ASSISTANT_ID", None)

config_list = config_list_from_json("OAI_CONFIG_LIST.json")
llm_config = {
    "config_list": config_list,
    "assistant_id": assistant_id
}

gpt_assistant = GPTAssistantAgent(name="assistant",
                                  instructions=AssistantAgent.DEFAULT_SYSTEM_MESSAGE,
                                  llm_config=llm_config)

user_proxy = UserProxyAgent(name="user_proxy",
                            code_execution_config={
                                "work_dir": "coding",
                                "use_docker": True
                            },
                            is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
                            human_input_mode="NEVER",
                            max_consecutive_auto_reply=1)

user_proxy.initiate_chat(gpt_assistant, message="Print hello world")

user_proxy.initiate_chat(gpt_assistant, message="Write py code to eval 2 + 2", clear_history=True)

gpt_assistant.delete_assistant()

