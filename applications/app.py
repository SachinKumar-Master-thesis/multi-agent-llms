import chainlit as cl
from chainlit.input_widget import *
from joblib import Parallel, delayed
import pandas as pd
import openai
from llama_index.llms.azure_openai import AzureOpenAI
import os
import sys
sys.path.insert(0, '/workspace/')
import chainlit as cl
from os import path
import yaml
from IPython.display import Markdown, display

from multi_agent_llms.utils.opensearch_utils import GetUIIndexSchemas
from multi_agent_llms.utils.agent_prompts import agent_dict
from multi_agent_llms.agents.es_agent import ElastiSearchcAgent
from multi_agent_llms.utils.opensearch_utils import OpensearchDataReader

import mlflow
# mlflow.set_experiment("ES Agent Workflow Tutorial")


city = os.getenv('CITY', None)
openai.api_type = os.getenv('OPENAI_API_TYPE')
openai.api_base = os.getenv('OPENAI_API_BASE')
openai.api_key = os.getenv('OPENAI_API_KEY')



# @cl.password_auth_callback
# def auth_callback(username: str, password: str):
#     username_ = os.getenv('CHAINLIT_USERNAME', None)
#     password_ = os.getenv('CHAINLIT_PASSWORD', None)

#     if (username, password) == (username_, password_):
#         return cl.User(
#             identifier="admin", metadata={"role": "admin", "provider": "credentials"}
#         )
#     else:
#         return None


@cl.on_chat_start
async def start():
    llm = AzureOpenAI(
                    model=os.getenv('OPENAI_API_MODEL'),
                    deployment_name=os.getenv('OPENAI_API_DEPLOYMENT_NAME'),
                    api_token=openai.api_key,
                    azure_endpoint=openai.api_base,
                    api_version='2024-06-01',
                    is_chat_model=False
                    )

    run_config_address = path.abspath(os.getenv('RUN_CONFIG_ADDRESS'))
    with open(run_config_address, 'r') as handle:
        run_config = yaml.full_load(handle)

    ui_indexes_schema = GetUIIndexSchemas(host=os.getenv('INDEXER_HOST'),
                                            user=os.getenv('INDEXER_USER'),
                                            password=os.getenv('INDEXER_PASSWORD'),
                                            selected_events=list(run_config.keys())
                                        ).run()

    opensearch_client  = OpensearchDataReader(host=os.getenv('OPENSEARCH_HOST'),
                                            port=os.getenv('OPENSEARCH_PORT'),
                                            user=os.getenv('OPENSEARCH_USER'),
                                            password=os.getenv('OPENSEARCH_PASSWORD'),
                                            )
    
    es_agent = ElastiSearchcAgent(llm=llm,
                              agent_dict=agent_dict,
                              schema_dict=ui_indexes_schema,
                              opensearch_client=opensearch_client,
                              max_errors=5,
                              city=city,
                              timeout=100
                              )


    cl.user_session.set("agent", es_agent)
    await cl.Message(author="Obi-one", content="I am an interactive ES agent. How can i can i help you").send()

@cl.on_message
async def main(message: cl.Message):
    data_scientist = cl.user_session.get("agent")
    if data_scientist is None:
        await cl.Message(
        author="Obi-one", content="ES agent is not initialized"
    ).send()

    result = await data_scientist.run(query=message.content)
    cl.user_session.set('result_dict', result)

    if not result.exited_with_error:
        inferences=[cl.Text(name='Inference', content=str(result.query_response_synthesis.response), display="inline")]
    else:
        inferences=[cl.Text(name='Error', content=str('Failed to sucessfully run the process'), display="inline")]
    await cl.Message(content="", elements=inferences).send()

    actions = [cl.Action(name="display_algorithm", value='Algorithmus', description="Algorithmus!", collapsed=False)]
    if len(result.error_lists)>0:
        actions.append(cl.Action(name="display_exception", 
                                value='Fehlermeldungen', 
                                description="Fehlermeldungen!", 
                                collapsed=False))

    text = cl.Text(name='Additional Information', content='Click on the button to display aditional information', display="inline")
    await cl.Message(content="",elements=[text], actions=actions).send()
    


@cl.action_callback("display_algorithm")
async def on_action(action: cl.Action):
    import json
    result = cl.user_session.get('result_dict')
    dict_markdown = json.dumps(result.query_generator_response.query, indent=4)
    message_ = [cl.Text(name='Query', content=f"Here is your ES query:\n\n```json\n{dict_markdown}\n```", display="inline")]
    markdown_list = "\n".join(f"- {item}" for item in result.query_generator_response.cot)
    message_.append(cl.Text(name='Algorithm', content=markdown_list, display="inline"))
    await cl.Message(content="", elements=message_).send()

    
@cl.action_callback("display_exception")
async def on_action(action: cl.Action):
    result = cl.user_session.get('result_dict')
    message_ = [cl.Text(name='Inference', content=str(result.error_lists), display="inline")]
    await cl.Message(content="", elements=message_).send()


if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit(__file__)
