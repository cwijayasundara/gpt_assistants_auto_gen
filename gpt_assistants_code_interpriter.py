import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST.json",
    file_location=".",
    filter_dict={
        "model": ["gpt-4-1106-preview"],
    },
)

# Example 1: Math Problem-Solving

from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
from autogen.agentchat import AssistantAgent, UserProxyAgent

# Initiate an agent equipped with code interpreter
gpt_assistant = GPTAssistantAgent(
    name="Coder Assistant",
    llm_config={
        "tools": [
            {
                "type": "code_interpreter"
            }
        ],
        "config_list": config_list,
    },
    instructions="You are an expert at solving math questions. Write code and run it to solve math problems. Reply "
                 "TERMINATE when the task is solved and there is no problem.",
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
    code_execution_config={
        "work_dir": "coding",
        "use_docker": True,
    },
    human_input_mode="NEVER"
)

# When all is set, initiate the chat.
user_proxy.initiate_chat(gpt_assistant,
                         message="If $725x + 727y = 1500$ and $729x+ 731y = 1508$, what is the value "
                                 "of $x - y$ ?",
                         clear_history=True)

# Example 2: Plotting with Code Interpreter

gpt_assistant = GPTAssistantAgent(
    name="Coder Assistant",
    llm_config={
        "tools": [
            {
                "type": "code_interpreter"
            }
        ],
        "config_list": config_list,
    },
    instructions="You are an expert at writing python code to solve problems. Reply TERMINATE when the task is solved "
                 "and there is no problem.",
)

user_proxy.initiate_chat(gpt_assistant,
                         message="Draw a line chart to show the population trend in US. Show how you "
                                 "solved it with code.",
                         clear_history=True)

from PIL import Image
import io
from IPython.display import display

api_response = gpt_assistant.openai_client.files.with_raw_response.retrieve_content("ile-pk1ElgDOghstaxChHZvDDRZj")

if api_response.status_code == 200:
    content = api_response.content
    image_data_bytes = io.BytesIO(content)
    image = Image.open(image_data_bytes)
    display(image)
