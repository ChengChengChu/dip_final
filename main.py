import openai


PDDL_PROMPT_TEMPLATE = 'Domain: [PDDL Domain]\nExample problems: [PDDL Training Tasks]\nWrite a short summary of this domain in words.'

def CoT(pddl_example, pddl_input ,pddl_domain='sokoban') :
    pddl_input = PDDL_PROMPT_TEMPLATE.replace('[PDDL Domain]', pddl_domain).replace('[PDDL Training Tasks]', pddl_input)
    msg = [
            {"role": "system", "content": "You are a helpful AI game planning assistant. You will give a the summary for the given task example."},
            {'role': 'user', 'content': f"Here are examples: {pddl_example}."}, 
            {"role": "user", "content": pddl_input}
        ]
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=msg
    )
    response_1 = response.choices[0].message.content
    
    msg.append({'role': 'assistant', 'content': response_1})
    msg.append({'role': 'user', 'content': f'There is a simple strategy for solving all problems in this domain. What is that strategy?\nDomain summary: {response_1}'})
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=msg
    )

    response_2 = response.choices[0].message.content
    msg.append({'role': 'assistant', 'content': response_2})
    msg.append({'Now, you have proposed a strategy, please implement the strategy as a Python function. The code should be of the form\ndef get_plan(objects, init, goal):\n    # Your code here\n    return plan\nwhere\nobjects is a set of (objectname,typename) init is a set of ground atoms represented as tuples of predicate names and arguments (e.g., (predicate-foo, object- bar, ...))tuples\ngoal is also a set of ground atoms represented in the same way\nplan is a set of actions, where each action is a ground operator represented as a string(e.g. up, down, right, left)'})

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=msg
    )

    return response.choices[0].message.content
