from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import enum

from llm import call_gpt4,call_gpt4v,call_zhipu,call_zhipu_vision
from tts import tts

# 创建一个FastAPI实例
app = FastAPI()

class ImageModelName(str, enum.Enum):
    gpt4 = "gpt4"
    zhipu = "zhipu"

class PromptModelName(str, enum.Enum):
    gpt4 = "gpt-4-turbo"
    gpt3 = "gpt-3.5-turbo"
    glm4 = "glm-4"
    glm3 = "glm-3-turbo"

class ImageRequest(BaseModel):
    image_base64: str
    prompt: str
    api_key: str
    image_model_name: ImageModelName = ImageModelName.zhipu

class PromptRequest(BaseModel):
    prompt: str
    api_key: str
    prompt_model_name: PromptModelName = PromptModelName.glm4
    temperature: Optional[float] = 0.5

class TTSRequest(BaseModel):
    text: str
    app_id: str
    access_token: str

class ModelResponse(BaseModel):
    content: str

class TTSResponse(BaseModel):
    data: str

@app.post("/image_prompt")
async def image_prompt(image_request: ImageRequest):
    if image_request.image_model_name == ImageModelName.gpt4:
        content = call_gpt4v(image_request.image_base64, image_request.prompt, image_request.api_key)
    elif image_request.image_model_name == ImageModelName.zhipu:
        content = call_zhipu_vision(image_request.image_base64, image_request.prompt, image_request.api_key)
    else:
        raise ValueError("Invalid image model name")
    return ModelResponse(content=content)

@app.post("/text_prompt")
async def text_prompt(prompt_request: PromptRequest):
    if prompt_request.prompt_model_name in [PromptModelName.gpt4, PromptModelName.gpt3]:
        content = call_gpt4(prompt_request.prompt, prompt_request.api_key, prompt_request.prompt_model_name.value, prompt_request.temperature)
    elif prompt_request.prompt_model_name in [PromptModelName.glm4, PromptModelName.glm3]:
        content = call_zhipu(prompt_request.prompt, prompt_request.api_key, prompt_request.prompt_model_name.value, prompt_request.temperature)
    else:
        raise ValueError("Invalid prompt model name")
    return ModelResponse(content=content)

@app.post("/tts")
async def tts_request(tts_request: TTSRequest):
    tts_response = tts(tts_request.app_id, tts_request.access_token, tts_request.text)
    return TTSResponse(data=tts_response)