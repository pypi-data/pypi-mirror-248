class Prompt:
    
    @staticmethod
    def build_prompt(history, knowledge):
        history_str = build_hitory(history, "User:", "Assistant:")
        input_format = (
            "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n"
            "### Instruction: <knowledge> {knowledge} {history} Assistant: \n\n"
            "### Response:"
        )
        prompt = input_format.format(knowledge=knowledge, history=history_str)
        return prompt
    
def build_hitory(history, first_role_code, second_role_code):
    history_str = ""
    for i, uttr in enumerate(history):
        if i == 0 or i % 2 == 0:
            history_str += " {user} {uttr}\n".format(user=first_role_code, uttr=uttr)
        else:
            history_str += " {system} {uttr}\n".format(system=second_role_code, uttr=uttr)
    return history_str.strip()