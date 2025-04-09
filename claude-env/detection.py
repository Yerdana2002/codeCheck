from methods import call_model, extract_xml
from typing import Dict, List, Tuple


# here I am defining functions that will generate the vulnerability CWE ID, as well as, possible fixes for the vulnerable code, from the prompt

def generate(prompt: str, task: str, context: str = "") -> Tuple[str, str]:
    #This function generates a solution based on the prompt provided by the system, task provided as a pythonic code by the user, and context, which is a list of previous prompts
    full_prompt = f"{prompt}\n{context}\nTask: {task}" if context else f"{prompt}\nTask: {task}"
    response = call_model(full_prompt)
    classification = extract_xml(response, "classification")
    mitigation = extract_xml(response, "mitigation")

    print("\n=== GENERATION START ===")
    print(f"Classification:\n{classification}\n")
    print(f"Mitigation:\n{mitigation}\n")
    print("=== GENERATION END ===\n")

    return classification, response

# Now I need to evaluate the result of generate() function based on the xml tag denoting the cwe_id

def preprocess(response:str)-> Dict[str, str]:
    # This function extracts CWE_ID, description, and the fixed code from the model's response for first step of evaluation
    results={}
    cwe_id = extract_xml(response, "cwe_id")

    if cwe_id:
        results["cwe_id"] = cwe_id

    vulberability_desc = extract_xml(response, "vulnerability_desc")
    if vulberability_desc:
        results["vulnerability_desc"] = vulberability_desc

    fixed_code = extract_xml(response, "fixed_code")
    if fixed_code:
        results["fixed_code"] = fixed_code

    return results

# After extracting essential pieces of response, I will load the jsonl dataset line by line.
# My approach here: 
# 1. I will compare the cwe_id from the model's response with the cwe_id in the jsonl dataset
# 2. If the corresponding fixed_code to the cwe_id in the jsonl dataset is the same as the fixed_code from the model's response, I will return True
# 3. If the cwe_id from the model's response is not in the jsonl dataset, I will return False
# 4. In case step 3 will return false, I will check if the cwe_id from the model's response belongs to any other related cwe_ids from CWE library
# 5. Finally, if the returned cwe_id from the model's response will not match with any cwe_id in the dataset, it will be considered as a false negative


def evaluation(prompt:str, content:str, task:str) -> Tuple[str, str]:
    # This function evaluates the model's response from generate function
    #Essentially, I amm trying to use the model to check on itself
    full_prompt = f"{prompt}\nOriginal task: {task}\nContent to evaluate: {content}"
    response = call_model(full_prompt)
    evaluation = extract_xml(response, "evaluation")
    feedback = extract_xml(response, "feedback")

    print("=== EVALUATION START ===")
    print(f"Status: {evaluation}")
    print(f"Feedback: {feedback}")
    print("=== EVALUATION END ===\n")

    return evaluation, feedback


def selfcheck(task:str, evaluator_prompt:str, generator_prompt:str) ->Tuple[str, List[Dict]]:
    # This function calls both the generate and evaluation functions iteratively, until the final output reaches some satisfactory level

    memory = []

    chain_of_thoughts = []

    classification, result = generate(generator_prompt, task)
    memory.append(result)
    chain_of_thoughts.append({"classification": classification, "result": result})


    while True:
        evaluation, feedback = evaluation(evaluator_prompt, result, task)
        if evaluation == "PASS":
            return result, chain_of_thoughts
        
        context = "\n".join([
            "Previous attempts:",
            *[f"- {m}" for m in memory],
            f"\nFeedback: {feedback}"
        ])
        
        classification, result = generate(generator_prompt, task, context)
        memory.append(result)
        chain_of_thought.append({"classification": classification, "result": result})



evaluator_prompt = """
Evaluate the following code vulnerability analysis for:
1) the correctness of the identified vulnerabilities according to the CWE system
2) the accuracy of the suggested mitigations
3) the clarity and conciseness of the explanations provided


You should be evaluating only and not attemping to solve the task.
Only output "PASS" if all criteria are met and you have no further suggestions for improvements.
Output your evaluation concisely in the following format.

<evaluation>PASS, NEEDS_IMPROVEMENT, or FAIL</evaluation>
<feedback>
What needs improvement and why.
</feedback>
"""

generator_prompt = """
Based on <user input> analyze the provided Python code for potential security vulnerabilities. Consider common issues such as input validation, authentication, authorization, data exposure, and other security-related concerns.

To classify vulnerabilities, use the CWE (Common Weakness Enumeration) system. Each vulnerability should be associated with a specific CWE ID. If there are feedback 
from your previous generations, you should reflect on them to improve your solution. If you identify any vulnerabilities, provide mitigation suggestions based on the information in the vulnerabilities JSON file. These suggestions should be specific and actionable, helping to address the identified security issues.

If you do not find any vulnerabilities in the code, explain why the code is considered safe. Provide specific reasons and reference relevant security best practices that the code follows.

Output your answer concisely in the following format: 

<classification>
[List each identified vulnerability with its CWE ID and a brief description]
</classification>

<mitigation>
[For each identified vulnerability, provide specific mitigation suggestions, including code examples if applicable. If no vulnerabilities are found, explain why the code is considered safe.]
</mitigation>
"""

task = """
<user input>
def yaml_load(filename):\nwith open(filename, 'r') as f:\ndata = yaml.load(f, Loader=yaml.BaseLoader)\nreturn data
</user input>
"""




selfcheck(task, evaluator_prompt, generator_prompt)

