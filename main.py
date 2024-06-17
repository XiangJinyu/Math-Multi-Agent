# coding=utf-8
from openai import OpenAI
from src.action.Calculate import WolframAlphaQuery, simple_calculate
from src.action import Programmer
print('ok')
import openai
import os
import re
import ast
from datetime import datetime
import time

api_key_1 = "输入GPT密钥"
base_url_1 = "输入转接地址"

api_key_2 = "输入Claude密钥"
base_url_2 = "输入转接地址"

GPT_client = openai.Client(api_key=api_key_1, base_url=base_url_1)

Claude_client = OpenAI(api_key=api_key_2, base_url=base_url_2)

question = """
3、A 与 B 二人进行 “ 抽鬼牌 ”游戏 。游戏开始时， A 手中有n张两两不同的牌 。 B 手上有n+1张牌，其中n张牌与 A 手中的牌相同，另一张为“鬼牌 ”，与其他所有牌都不同。游戏规则为：

i) 双方交替从对方手中抽取一张牌， A 先从 B 手中抽取。

ii) 若某位玩家抽到对方的牌与自己手中的某张牌一致，则将两张牌丢弃。

iii) 最后剩一张牌（鬼牌）时，持有鬼牌的玩家为输家。

假设每一次抽牌从对方手上抽到任一张牌的概率都相同，请问下列n中哪个n使 A 的胜率最大？（单选题）


A.n = 31


B.n = 32


C.n = 999


D.n = 1000

E.对所有的n，A 的胜率都一样
"""


def askLLM(messages, max_retries=10, delay=2):
    """
    参数:
    - messages: 发送到模型的消息
    - max_retries: 最大重试次数
    - delay: 重试之间的等待时间（秒）

    返回:
    - 模型的响应内容，或在重试次数耗尽后返回None
    """
    MODEL = "gpt-4-turbo-2024-04-09"
    attempt = 0

    while attempt < max_retries:
        try:
            response = GPT_client.chat.completions.create(
                model=MODEL, messages=messages, temperature=0.7, max_tokens=3000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"尝试 {attempt + 1}/{max_retries} 失败: {e}")
            time.sleep(delay)
            attempt += 1

    print("重试次数已耗尽，未能成功获取响应。")
    return None


def actLLM(messages, the_model, max_retries=10, delay=2):
    attempt = 0

    while attempt < max_retries:
        try:

            if the_model == "GPT":
                MODEL = "gpt-4-turbo-2024-04-09"
                response = GPT_client.chat.completions.create(
                    model=MODEL, messages=messages, temperature=0.7, max_tokens=3000
                )
                return response.choices[0].message.content

            if the_model == "Claude":
                MODEL = "claude-3-opus-20240229"
                response = Claude_client.chat.completions.create(
                    model=MODEL, messages=messages, temperature=0.7, max_tokens=3000
                )
                return response.choices[0].message.content

        except Exception as e:
            print(f"尝试 {attempt + 1}/{max_retries} 失败: {e}")
            time.sleep(delay)
            attempt += 1

    print("重试次数已耗尽，未能成功获取响应。")
    return None


def extract_code_block(code_block):
    match = re.search(r'```python(.*?)```', code_block, re.DOTALL)
    if match:
        code = match.group(1)
        try:
            code = code.encode('utf-8', 'ignore').decode('utf-8')
        except UnicodeEncodeError:
            code = code.encode('utf-8', 'ignore').decode('utf-8')
        return code
    else:
        return 'No code'


def choose_action(list, message, question, the_model):
    action = list[0]
    query = list[1]

    if action == "wolfram_alpha":
        app_id = '输入你的wolfram_alpha key'
        Wolfram = WolframAlphaQuery(app_id)
        response_data = Wolfram.send_query(query)
        if response_data:
            answer = Wolfram.process_response(response_data)
            print(answer)
            return answer
        else:
            return "高级计算出错"

    if action == "simple_calculate":
        answer = simple_calculate(query)
        print("Result:", answer)
        return answer

    if action == "deep_thinking":
        think_message = [{"role": "system",
                          "content": f"""你是一名数学指导，think step by step，
                      根据目前的对话信息及问题，进行深度分析，提出建设性的建议和问题。分析当前亟待解决的问题以及可能解决问题的一些路径，并尝试解决它们。不需要提出接下来需要调用的方法。尽可能多地使用LateX公式进行推导。
                      """},
                         {"role": "user", "content": "历史对话内容如下:" + str(message) + "\n当前疑问：" + query}]
        answer = actLLM(think_message, the_model)
        return answer

    if action == "deduction":
        derivation_message = [{"role": "system",
                               "content": f"""你是一名数学推导大师，think step by step，
                      根据目前的对话信息及问题，进行深度分析，严谨地使用LaTeX格式进行推导。
                      请先列出已知信息，然后再开始严谨的推导。
                      尽可能多地使用LateX公式进行推导。
                      不需要提出接下来需要调用的方法。
                      """},
                              {"role": "user", "content": "历史对话内容如下:" + str(message) + "\n当前疑问：" + query}]
        answer = actLLM(derivation_message, the_model)
        return answer
    if action == "programmer":
        programmer = Programmer.Python_Programmer(f"问题：{question}\n目的：{query}")
        answer = programmer.solve_problem()
        for ans in answer:
            print(ans)
        return str(answer)

    if action == "Resolve":
        return True

    else:
        return "调用出错"


def main():
    # 获取当前时间
    start_time = datetime.now()
    print("开始时间:", start_time)
    # m为总共有几名角色进行解题
    m = 5
    # n为每个角色解题总共最多几轮
    n = 15
    # 生成m个思路，为不同角色提供不同的解题路径
    process_message = [{"role": "system",
                        "content": rf"""
                        你是一名数学家，思考{m}个不同的解题方向和思路，使用List的格式输出。(输出格式为：[str,str,...])
                        除了输出Python格式的List之外，不要输出任何其它的内容，你的回复将直接用于python程序的解析。
                        不要给出答案，而是给出不同解题的方向和思路。使用中文。
                       """},
                       {"role": "user", "content": question}]
    way = askLLM(process_message)

    # 将m个思路解析成列表
    way_list = ast.literal_eval(way)
    print(way)

    total_summary = ""
    # 开启进程循环,这里的process遍历一个为解题一轮
    for process in range(m):
        # 选择方法Prompt
        choose_template = [{"role": "system",
                            "content": r"""你将对对话解析，认为接下来需要调用的方法及输入的内容是什么？使用List的格式输出。(输出格式为：str,str)
                           可以调用的方法如下：
                          ```
                          1.wolfram_alpha : 该方法可以对复杂的方程或函数进行求解。Output Format:["wolfram_alpha","LaTeX格式表示的公式（只有公式，没有任何其它解释）"]. Example:["wolfram_alpha","\int_{0}^{5} \frac{x^{3}}{5+3x} \cdot \frac{x+5}{x+2}"]
                          2.simple_calculate : 该方法可以对简单的方程或函数进行求解。Output Format:["simple_calculate","LaTeX格式表示的公式（只有公式，没有任何其它解释）"]. Example:["simple_calculate","\int_{0}^{5} \frac{x^{3}}{5+3x} dx"]
                          3.deep_thinking : 该方法会对当前已知信息进行深度分析，并给出接下来可能的探索方向。Output Format:["deep_thinking","目前的困惑或疑问"]. Example:["deep_thinking","如何找到一条路径以最大化右转数量，并最小化总等待时间？"]
                          4.deduction ：该方法启动链式思考，分析需要得到的结论，进行逐步推导.Output Format:["deduction","LaTeX格式表示需要推导的公式或用自然语言描述需要推导的问题"]. Example:["deduction","对已知的方程进行推导"]
                          5.programmer ：调用程序员，为你撰写Python代码求解出所需要的问题的数值解。调用该方法时，请完整精确说出需求(包括优化的方法等)，因为程序员只能看到题目，无法看到你之前的推导过程。Output Format:["programmer","LaTeX格式表示需要推导的公式或用自然语言描述需要推导的问题，涉及的公式或问题及参数必须详细准确，不能有信息缺失"]. Example:["programmer","用蒙特卡洛算法，写一个python代码，求解一个a=3,b=4,高为5的椭球的体积"]
                          6.Resolve ： 该方法代表你已经得出了最终答案，将输出最终答案并结束这个问题的解答。Output Format:["Resolve","最终答案/结论或求解结果"]. Example:["Resolve","通过上述推导步骤，我给出该题最终结果为18"]
                          ```
                          只能调用一个方法，不要输出其它任何解释，只输出List.
                          LaTeX格式表示的公式禁止使用\[,\],\(以及\)。请统一使用$$。
                          Latex表达时，也请使用\来调用特殊格式，而不是双斜杠。因为你的公式直接被读取，不用担心被解析为转义字符。
                           """}]
        # 主进程Prompt
        message = [{"role": "system",
                    "content": r"""你是一名数学学家，请先拆解问题，然后think step by step，
                      可以使用Latex表达式，进行公式推导，分析当前已知信息，然后根据目前的推导，决策接下来需要进行的步骤。
                      注意，LaTeX格式表示的公式禁止使用\[,\],\(以及\)。请统一使用$$。
                      你的推导尽可能严谨，因为这个题目是一个全球数学竞赛题（允许进行编程求解）将你的每个推导结论转为疑问，来进行进一步思考和自问。
                      在最后的结尾，必须加上你认为下一步可以做的行动，可以调用以下行为：
                      ```
                      1.调用wolfram_alpha : 该方法可以对复杂的方程或函数进行求解，在说明使用该方法时，请一并使用LaTeX格式给出方程/公式
                      2.调用simple_calculate : 该方法可以对简单的方程或函数进行求解，如初等函数或简单积分微分，在说明使用该方法时，请一并使用LaTeX格式给出方程/公式
                      3.调用deep_thinking : 该方法会对当前已知信息进行深度分析，并给出接下来可能的探索方向
                      4.使用deduction ： 该方法启动链式思考，分析需要得到的结论，进行逐步推导
                      5.使用programmer ： 该方法调用程序员，是一个较通用的方法，为你撰写Python代码求解出所需要的问题的数值解，该方法应该作为优先级较高的方法。可以进行大规模计算以及解决复杂的数值解问题，也可在推导/证明等过程中方便试错和推测最终答案。你几乎可以在任何情况下使用这个方法。但如果较复杂的程序会导致超时（运行大于10分钟），这时可以考虑测试特殊情况或将范围缩小进行代码运行后参考，或者更换其它解决方式。
                      6.Resolve ： 该方法代表你已经得出了最终答案，将输出最终答案并结束这个问题的解答。注意，这个方法不会帮助你解决问题，仅仅是在你确定最终答案后进行汇报的方式。
                      ```
                      每次只能选择一个行动，并使用着重符号标明需要调用的行为。
                      始终使用中文输出回答。
                      """}, {"role": "user", "content": question}, {"role": "user", "content": way_list[process]}]

        answer_article = ""

        # 不同角色交替使用GPT和Claude来作为action的Model，增加答案可能性
        if process % 2 == 0:
            the_model = "Claude"
        else:
            the_model = "GPT"

        # 单进程循环，这里i遍历一个代表思考一轮（进行一轮行动）
        for i in range(n):
            # 每一轮开始时，都对当前形势进行思考，作为answer
            answer = askLLM(message)
            answer_article += answer + "\n"
            print(answer)
            message.append({"role": "assistant", "content": answer})

            # 分析完当前形势后，挑选下一步的行动
            choose_message = choose_template
            choose_message.append(
                {"role": "user", "content": str(message[-1])})
            choice = askLLM(choose_message)
            answer_article += choice + "\n"
            print(choice)

            # 将选择行动的str解析为list
            choice_list = ast.literal_eval(choice)

            # 将选择行动的list传入选择行动函数，调用对应的方法，返回结果
            answer = choose_action(choice_list, message, question, the_model)
            answer_article += str(answer) + "\n"
            print(answer)

            # 当得出角色认为的正确答案，则退出该角色的解题循环
            if answer is True:
                final_answer = choice_list[1]
                answer_article += "本循环最终答案：" + final_answer + "\n"
                print(final_answer)
                break

            # 将调用行动得到的答案加入到主进程中
            message.append({"role": "user", "content": answer})

            # 当角色进程来到最后一轮时，强制给出目前认为最可能的答案
            if i == n - 1:
                message.append({"role": "user",
                                "content": "现在，根据之前所有的推导和证明，给出你认为最可能的答案或结果，哪怕这个答案你还不够确定，并且不需要给出下一步行动。"})
                answer = askLLM(message)
                answer_article += answer + "\n"
                print(answer)

        # 对刚刚角色的整个做题流程进行总结
        summary_message = [{"role": "system",
                            "content": rf"""
                            根据题目及完整解题流程，给出一个精简的解题流程总结，step by step，给出每一步的解题的说明。你的总结应该尽可能专业，并包含涉及到的公式。也需要明确给出解题过程中最终得出的结论（如果严谨得出，信心程度为强，如果只是推测或其它方式，则为一般或弱）。
                            output format:
                            ```
                            1.
                            2.
                            3.
                            ...
                            最终结论：xxx
                            信心程度：强/一般/弱
                            ```
                           """},
                           {"role": "user", "content": f"\n原问题：{question}\n\n解题过程：{answer_article}"}]

        model = "Claude"
        summary = actLLM(summary_message, model)

        summary = f"关键解题步骤摘要及结论：\n\n{summary}\n\n"

        # 将每一轮的结果都封装到一起
        total_summary += f"# 第{process + 1}名角色解题关键过程及结果为：\n\n{summary}"

        # 将关键结果总结和完整解题步骤整理在一起，方便查看
        answer_article = summary + answer_article

        # 将完整结果存入txt文件中
        with open(f"answer_article_{process + 1}.txt", "w", encoding="utf-8") as file:
            file.write(answer_article)

    # 评审角色对每一轮（即每个角色）的结果进行整理分析，评选出最可能的结果
    review_message = [{"role": "system",
                       "content": rf"""
                        根据问题及多个角色的推理过程及得到的答案，先给出你的总结和分析，step by step，最终给出你认为最可能的正确答案。
                        数值解，理论推导，解析解等方法都可以作为最终答案，主要关注给出每个答案的人数及过程是否正确。
                       """},
                      {"role": "user", "content": f"\n问题：{question}\n\n解题结果：{total_summary}"}]
    print(total_summary)
    review = askLLM(review_message)

    print(review)

    # 获取当前时间
    end_time = datetime.now()
    print("开始时间:", start_time)
    print("结束时间:", end_time)

    # 计算耗时
    time_difference = end_time - start_time
    total_seconds = time_difference.total_seconds()
    # 将总秒数转换为分钟
    total_minutes = total_seconds / 60
    print("耗时分钟:", total_minutes)

    # 将最终评审结果整理到txt文件中
    with open(f"Final_answer.txt", "w", encoding="utf-8") as file:
        file.write(review)


if __name__ == "__main__":
    main()