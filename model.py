# Chat Model Documents: https://python.langchain.com/v0.2/docs/integrations/chat/
# OpenAI Chat Model Documents: https://python.langchain.com/v0.2/docs/integrations/chat/openai/
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI(azure_deployment="gpt-4o",
                      api_version="2023-03-15-preview",
                      azure_endpoint="https://dblunt.openai.azure.com/",
                      openai_api_key="92061e05ce11414bb8196cbe5b1448d0")

result = llm.invoke("What is 81 divided by 9?")

print(result.content)
