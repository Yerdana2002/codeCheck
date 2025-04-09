## Detection of vulnerabilities in a code output by Large Language Models (LLMs). 

This project aims to present the usage of Claude 3.7 sonnet by Anthropic as a base model, to detect, and fix vulnerable code outputted by Large Language Models as a part of research done by Siddiq Mohammed, and Joanna Santos. 
Demo, what I learned along the way, description

# Apart from aesthetics, there are measurable metrics that are applicable to the project. 
1) Accuracy. I define it as a correct classification of the CWE vulnerability type.
2) Correctness. I define it as correctness of the output for the modified python code.
3) Latency. This is the time period that the end user waits between sending their prompt, and getting their result back. Although the time depends on speed of the network, or complexity of their task in a prompt, it also depends on the design and implementation of the system.

# Project: LLM Code Vulnerability Analysis (Example Title)

## Introduction

I started this project after reading a paper by Siddiq and Santos. It showed detecting code vulnerabilities is hard. Static analyzers often fail with LLM-generated code. This inspired me to use an LLM for this problem. I aim to fine-tune Claude 3.7 Sonnet. It should find security issues (CWEs) in Python code. It should also suggest fixes.

## How It Works

The system takes Python code as input. I used two agents with the Anthropic API: `generator` and `evaluator`. The `generator` analyzes the code. It uses the code and my prompt. It gets an analysis from Claude. It uses XML tags (`<classification>`, `<mitigation>`) for the output. These tags make parsing easier.

Next, the `evaluator` checks the generator's output. It uses its own instructions to review the output. It assigns a status: `PASS`, `NEEDS_IMPROVEMENT`, or `FAIL`. It checks the CWE ID and the suggested fix for correctness. The evaluator returns `<evaluation>` and `<feedback>` tags.

The system uses a self-correction loop. If the status is not `PASS`, the generator runs again. It gets the feedback and previous attempts as context. This repeats until the status is `PASS`. The final output is the approved analysis and fix.

## What I Learned

An important finding occurred during testing. I used YAML loading code related to `CWE-20`. A simple database might only list `CWE-20`. However, Claude found risks for `CWE-20`, `CWE-22` (Path Traversal), and `CWE-502` (Deserialization). I was surprised it connected these issues. It seemed to understand the full context better than a simple rule lookup. This showed me the LLM could provide deeper analysis. It seemed better than simpler methods.

## Why I Didn't Use Other Ideas?

Before choosing the self-correction loop, I considered other ideas. I thought about vector databases or embeddings. But the cost and setup seemed too high for this task. This task requires specific pattern matching, not broad semantics.

My other main idea used a database. The plan was: LLM predicts a CWE. Then, query my `JSONL` file for example code. Compare the input code to the example code character by character. As a fallback, check related CWEs using `related_weaknesses` data.

But this approach had problems. The process seemed inefficient, even with indexing. Also, I found the `related_weaknesses` data rarely linked many CWEs in my dataset. This made the fallback less useful. The main problem was this method focused only on the first CWE found. It could miss other vulnerabilities. Because of these issues, I chose the current LLM evaluation loop.

## Current Challenges

A remaining challenge is how CWEs are represented to LLMs, where the similarity between them is still unknown to me. Since they can't be studied by their names, or textual attributes but are tied to sample codes that they represent, majority of the weights are determined during the training stage, which I assume we as users have no control of. Also, techniques such as PEFT, namely LoRA can't be used for this purpose. 

## Next Steps

For next steps, I plan to experiment with using explicit tool calling by the large language model depending on the context. Also, I am planning to play with "thinking" parameter of Claude, as well as, trying few shot approaches that seem promising to me. 
