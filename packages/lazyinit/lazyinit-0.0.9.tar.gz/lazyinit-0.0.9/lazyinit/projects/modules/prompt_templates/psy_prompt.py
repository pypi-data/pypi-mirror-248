class Prompt:
    
    @staticmethod
    def build_prompt(id, history, query):
        history = "\n".join(history)
#         input_format = """
# \n[Round {id}]
# 问：
# 我想让你扮演一个来自心理咨询工作室的心理咨询师，你需要将自己代入角色并根据提供的对话历史、角色描述等补充信息来回答用户问题，同时需要遵守以下规则和要求：\n
# 1、使用心理咨询师的语气、专业词汇等角色鲜明的特征来进行回答；\n
# 2、尽可能多地去照顾对方情绪，不要只给出生硬、冰冷的解决措施;\n
# 3、你了解心理咨询师的所有相关知识并能灵活使用这些知识进行对话。\n
# 以下是对心理咨询师的角色描述：\n
#     用于帮助用户提供心理疏导和安慰，注重情绪陪伴。
# 以下是相关的对话历史，作为对话背景的了解和参考：\n
# {history}
# 以下是用户提出的问题，需要使用你的专业素养来进行回答：
#     {query}
    
# 答：
# """
        input_format = """
\n\n[Round {id}]\n\n问：\n\n{query}\n\n答：
"""
        return input_format.format(id=str(id), history=history, query=query)