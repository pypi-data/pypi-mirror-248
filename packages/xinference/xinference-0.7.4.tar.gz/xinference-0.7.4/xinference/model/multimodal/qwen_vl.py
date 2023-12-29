# Copyright 2022-2023 XProbe Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import operator
import time
import uuid
from typing import Dict, Iterator, List, Optional, Union

from ...types import (
    ChatCompletion,
    ChatCompletionChoice,
    ChatCompletionChunk,
    CompletionUsage,
)
from ..utils import select_device
from .core import LVLM, LVLMFamilyV1, LVLMSpecV1


class QwenVLChat(LVLM):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tokenizer = None
        self._model = None

    @classmethod
    def match(
        cls, model_family: "LVLMFamilyV1", model_spec: "LVLMSpecV1", quantization: str
    ) -> bool:
        if "qwen" in model_family.model_name:
            return True
        return False

    def load(self):
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from transformers.generation import GenerationConfig

        device = self.kwargs.get("device", "auto")
        device = select_device(device)

        self._tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            trust_remote_code=True,
            code_revision=self.model_spec.model_revision,
        )
        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            device_map=device,
            trust_remote_code=True,
            code_revision=self.model_spec.model_revision,
        ).eval()
        # Specify hyperparameters for generation
        self._model.generation_config = GenerationConfig.from_pretrained(
            self.model_path,
            trust_remote_code=True,
            code_revision=self.model_spec.model_revision,
        )

    def _message_content_to_qwen(self, content) -> str:
        if not isinstance(content, str):
            content = [
                {"image": c["image_url"]["url"], "type": "image"}
                if c.get("type") == "image_url"
                else c
                for c in content
            ]
            content = sorted(content, key=operator.itemgetter("type"))
            return self._tokenizer.from_list_format(content)
        return content

    def chat(
        self,
        prompt: Union[str, List[Dict]],
        system_prompt: Optional[str] = None,
        chat_history: Optional[List[Dict]] = None,
        generate_config: Optional[Dict] = None,
    ) -> Union[ChatCompletion, Iterator[ChatCompletionChunk]]:
        prompt = self._message_content_to_qwen(prompt)
        # Convert openai history to qwen vl history
        qwen_history = []
        query_to_response: List = []
        for h in chat_history or []:
            role = h["role"]
            content = self._message_content_to_qwen(h["content"])
            if len(query_to_response) == 0 and role == "user":
                query_to_response.append(content)
            if len(query_to_response) == 1 and role == "assistant":
                query_to_response.append(content)
            if len(query_to_response) == 2:
                qwen_history.append(query_to_response)
                query_to_response = []
        response, history = self._model.chat(
            self._tokenizer, query=prompt, history=qwen_history
        )
        return ChatCompletion(
            id="chat" + str(uuid.uuid1()),
            object="chat.completion",
            created=int(time.time()),
            model=self.model_uid,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message={"role": "assistant", "content": response},
                    finish_reason="stop",
                )
            ],
            usage=CompletionUsage(
                prompt_tokens=-1, completion_tokens=-1, total_tokens=-1
            ),
        )
