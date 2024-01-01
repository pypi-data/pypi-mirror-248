import os
from typing import TYPE_CHECKING, AsyncIterator, Dict, Generator, List

from transformers import AutoTokenizer
from vllm import AsyncEngineArgs, AsyncLLMEngine, SamplingParams

from ..utils.vllm_monkey_patch import llama_attn_bias_monkey_patch


if TYPE_CHECKING:
    from transformers import PreTrainedTokenizerBase
    from vllm import RequestOutput


class ChatModel:
    def __init__(self) -> None:
        if int(os.environ.get("ENABLE_ATTN_BIAS")):
            llama_attn_bias_monkey_patch()

        engine_args = AsyncEngineArgs(model=os.environ.get("CHAT_MODEL"))
        self._engine = AsyncLLMEngine.from_engine_args(engine_args)
        self._tokenizer: "PreTrainedTokenizerBase" = AutoTokenizer.from_pretrained(
            pretrained_model_name_or_path=os.environ.get("CHAT_MODEL")
        )

    def _generate(
        self, messages: List[Dict[str, str]], request_id: str, **gen_kwargs
    ) -> AsyncIterator["RequestOutput"]:
        input_ids = self._tokenizer.apply_chat_template(
            conversation=messages, tokenize=True, add_generation_prompt=True
        )
        sampline_params = SamplingParams(
            temperature=gen_kwargs.get("temperature", None) or 1.0,
            top_p=gen_kwargs.get("top_p", None) or 1.0,
            max_tokens=gen_kwargs.get("max_tokens", None) or 1024,
        )
        result_generator = self._engine.generate(
            prompt=None, sampling_params=sampline_params, request_id=request_id, prompt_token_ids=input_ids
        )
        return result_generator

    async def chat(self, messages: List[Dict[str, str]], request_id: str, **gen_kwargs) -> str:
        generator = self._generate(messages, request_id, **gen_kwargs)
        prev_text = ""
        async for result in generator:
            prev_text = result.outputs[0].text
        return prev_text

    async def stream_chat(
        self, messages: List[Dict[str, str]], request_id: str, **gen_kwargs
    ) -> Generator[str, None, None]:
        generator = self._generate(messages, request_id, **gen_kwargs)
        prev_text = ""
        async for result in generator:
            delta_text = result.outputs[0].text[len(prev_text) :]
            prev_text = result.outputs[0].text
            yield delta_text
