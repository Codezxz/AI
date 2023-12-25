import openai
import json
import time

# Define your API key
# api_key = "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"
openai.api_key = "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"
# Function to send a conversation to GPT-3.5 Turbo
def send_message(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
    )
    return response

# Retry function with exponential backoff
def retry_with_backoff(messages, max_retries=5):
    for retry in range(max_retries):
        response = send_message(messages)
        if response.get("error") and response["error"]["code"] == "rate_limited":
            # Exponential backoff with a wait time that doubles each retry
            wait_time = 2 ** retry
            print(f"Rate limited. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            return response
    return None  # Max retries reached

# Main conversation function
def run_conversation():
    messages = [{"role": "user", "content": "What's the weather like in Boston?"}]
    response = retry_with_backoff(messages)
    if response:
        return response
    else:
        return {"error": "Max retries reached"}

# Call the main conversation function
print(run_conversation())
