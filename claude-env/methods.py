from anthropic import Anthropic
import os
import re

"ANTHROPIC_API_KEY" = ""

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
# Our first function is to call the appropriate model using anthropic api key

def call_model(prompt: str, system_prompt: str="", model = "claude-3-7-sonnet-20250219") -> str:
    """
    Here this function is a blueprint. It calls the specified model, and passes the prompt to it and returns the response from the model as a string
    """

    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    messages = [{"role":"user", "content": prompt}]
    response =client.messages.create(
        model=model,
        max_tokens=4096,
        system=system_prompt,
        messages=messages,
        temperature=0.1,
    )

    return response.content[0].text


def extract_xml(text:str, tag:str)-> str:
    """"
    This function extracts xml tags from the model's response. For instance, it separates the cwe_id, and the newly generated code.
    Here text is a string from our model's response, and tag is the xml tag in the response that denotes specific fields
    """

    match=re.search(f'<{tag}>(.*?)</{tag}>', text, re.DOTALL)
    return match.group(1) if match else ""
