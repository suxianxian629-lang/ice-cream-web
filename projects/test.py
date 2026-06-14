from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

with open("projects/note.txt", "r", encoding="utf-8") as f:
    knowledge = f.read()

while True:
    question = input("你：")

    if question.lower() == "exit":
        break

    response = client.chat.completions.create(
        model="deepseek-r1-distill-qwen-14b",
        messages=[
            {
                "role": "user",
                "content": f"""
知识库：

{knowledge}

问题：
{question}
"""
            }
        ]
    )

    print("\nAI：")
    print(response.choices[0].message.content)