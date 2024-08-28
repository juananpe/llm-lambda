# llm-lambda

This is a plugin for [LLM](https://llm.datasette.io/) that provides access to the [LambdaLabs API](https://docs.lambdalabs.com/on-demand-cloud/using-the-lambda-chat-completions-api) models.

## Installation

Install this plugin in the same environment as LLM:

```bash
llm install llm-lambda
```

## Configuration

You'll need to set an environment variable with your LambdaLabs API key:

```bash
export LLM_LAMBDA_KEY="your-api-key-here"
```

You can also use the `llm keys set` command:
```bash
llm keys set lambda
```

## Usage

This plugin adds two new models:

- `lambda-hermes-3-18k`: Hermes 3 model with 18K context length
- `lambda-hermes-3-128k`: Hermes 3 model with 128K context length

You can use these models like this:

```bash
llm -m lambda-hermes-3-18k "Your prompt here"
``` 

Or:

```bash
llm -m lambda-hermes-3-128k "Your prompt here"
```

## Model details

- `lambda-hermes-3-18k`: This model uses the `hermes-3-llama-3.1-405b-fp8` LambdaLabs model with an 18K token context length.
- `lambda-hermes-3-128k`: This model uses the `hermes-3-llama-3.1-405b-fp8-128k` LambdaLabs model with a 128K token context length.

If a request using the 18K model exceeds its context length, it will automatically fall back to using the 128K model.

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

```bash
cd llm-lambda
python3 -m venv venv
source venv/bin/activate
pip install .
```
You can install the plugin in the llm command for testing/developing:

```bash 
llm install -e .
```

Check that it is there:
```bash 
llm plugins
```


## License

Apache 2.0
