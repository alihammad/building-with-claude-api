# 01_api_fundamentals

This folder contains introductory notebook examples for using the Anthropic Claude API from Python.

## What is included

- `basic_api_call.ipynb`
  - Shows a minimal Anthropic API call.
  - Installs `anthropic` and `python-dotenv`.
  - Loads environment variables from `.env`.
  - Sends a simple user prompt with `client.messages.create()`.

- `conversations.ipynb`
  - Demonstrates a basic chat/conversation workflow.
  - Includes helper functions to add user and assistant messages.
  - Wraps Anthropic `messages.create()` in a `chat(messages)` function.

- `structured_output.ipynb`
  - Demonstrates generating structured or formatted output from the model.
  - Uses the same Anthropic chat/message flow as the conversation example.

- `system_prompt.ipynb`
  - Adds a system prompt layer to control assistant behavior.
  - Shows how to pass a `system` prompt into the request parameters.

- `temperature.ipynb`
  - Demonstrates streaming responses from Anthropic.
  - Uses `client.messages.stream(...)` and iterates over `stream.text_stream`.

## Requirements

- Python 3.14+ (or compatible runtime)
- `anthropic`
- `python-dotenv`

## Setup

1. Create a `.env` file in the repository root with your Anthropic API key:

   ```bash
   ANTHROPIC_API_KEY=your_api_key_here
   ```

2. Ensure `.env` is ignored by Git. This repository already includes `.env` in `.gitignore`.

3. Open the notebooks in Jupyter or VS Code and run the cells.

## Usage

- Run each notebook interactively to explore the example.
- The notebooks are designed to show:
  - a simple API call,
  - message-based conversation handling,
  - structured output prompts,
  - system prompt usage,
  - and streaming response handling.

## Notes

- Do not commit any secret keys or `.env` contents to source control.
- If a secret has been accidentally committed, remove it from history and rotate the key.
