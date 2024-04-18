# import openai
# openai.api_key=""
# openai.base_url="https://lonlie.plus7.plus/v1"
# response = openai.Completion.create(
#     prompt=[
#         {
#             "role":"system",
#             "content":"You are a helpful assistant."
#         },
#     ],
#     engine="gpt-3.5-turbo",
# )
# print(response)
import openai
from openai import OpenAI
client = OpenAI(api_key="",base_url="https://lonlie.plus7.plus/v1")
response = client.chat.completions.create(
    messages=[
        {
            "role":"system","content":"You are a helpful assistant."
        },
    ],
    model="gpt-3.5-turbo",
)
print(response)
