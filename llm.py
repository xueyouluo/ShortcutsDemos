from zhipuai import ZhipuAI
import os
import requests


def call_zhipu(prompt, api_key, model='glm-4', temperature=0.5):
    client = ZhipuAI(api_key=api_key)
    response = client.chat.completions.create(
        temperature=temperature,
        model=model,
        messages=[{
            'role': 'user',
            'content': prompt
        }]
    )
    return response.choices[0].message.content

def call_zhipu_vision(image_base64, prompt, api_key):
    client = ZhipuAI(api_key=api_key)
    response = client.chat.completions.create(
        model="glm-4v",  # 填写需要调用的模型名称
        messages=[
            {
                "role": "user",
                "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                    {
                            "type": "image_url",
                            "image_url": {
                                "url": image_base64
                            }
                            }
                ]
            }
        ]
    )
    return response.choices[0].message.content

def call_gpt4(prompt, api_key, model='gpt-4-turbo',temperature=0.5):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": temperature
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']

def call_gpt4v(image_base64, prompt, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ],
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return response.json()['choices'][0]['message']['content']