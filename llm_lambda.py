# [LLM](https://llm.datasette.io/) plugin providing access to [LambdaLabs API](https://docs.lambdalabs.com/).
import llm
from openai import OpenAI

@llm.hookimpl
def register_models(register):
    register(LLMLambda("lambda-hermes-3-18k"))
    register(LLMLambda("lambda-hermes-3-128k"))

class LLMLambda(llm.Model):
    model_map: dict = {
        "lambda-hermes-3-18k": "hermes-3-llama-3.1-405b-fp8",
        "lambda-hermes-3-128k": "hermes-3-llama-3.1-405b-fp8-128k",
    }

    def __init__(self, model_id):
        self.model_id = model_id

    def build_messages(self, prompt, conversation):
        messages = []
        if not conversation:
            if prompt.system:
                messages.append({"role": "system", "content": prompt.system})
            messages.append({"role": "user", "content": prompt.prompt})
            return messages
        current_system = None
        for prev_response in conversation.responses:
            if (
                prev_response.prompt.system
                and prev_response.prompt.system != current_system
            ):
                messages.append(
                    {"role": "system", "content": prev_response.prompt.system}
                )
                current_system = prev_response.prompt.system
            messages.append({"role": "user", "content": prev_response.prompt.prompt})
            messages.append({"role": "assistant", "content": prev_response.text()})
        if prompt.system and prompt.system != current_system:
            messages.append({"role": "system", "content": prompt.system})
        messages.append({"role": "user", "content": prompt.prompt})
        return messages

    def execute(self, prompt, stream, response, conversation):
        key = llm.get_key("", "lambda", "LLM_LAMBDA_KEY")
        messages = self.build_messages(prompt, conversation)
        client = OpenAI(
            api_key=key,
            base_url="https://api.lambdalabs.com/v1"
        )
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=self.model_map[self.model_id],
            stream=stream
        )
        if stream:
            for chunk in chat_completion:
                yield chunk.choices[0].delta.content or ""
        else:
            yield chat_completion.choices[0].message.content