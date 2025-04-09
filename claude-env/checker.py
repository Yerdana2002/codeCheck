import anthropic

client  = anthropic.Anthropic()

message = client.messages.create(
    model='claude-3-5-sonnet-20241022',
    max_tokens=1000,
    temperature=0.1,
    system='You are a programmer well versed in Common Weakness Enumeration. Respond only with CWE ID,  name of the weakness, and recommended fix should rely only on CWE potential mitigation description. Your response should also include the fixed version of the prompt code provided.',
    messages=[
        {
            "role":"user",
            "content": [
                {
                    "type":"text",
                    "text": "detect the vulnerability in the give code def yaml_load(filename):\nwith open(filename, 'r') as f:\ndata = yaml.load(f, Loader=yaml.BaseLoader)\nreturn data"
                }
            ]
        }
    ]
)



print(message.content)