import time
import re
from subprocess import Popen, PIPE, TimeoutExpired
import os
from openai import OpenAI
import sys

# 获取当前Python解释器的路径
current_python_executable = sys.executable


class Python_Programmer:
    def __init__(self, problem):
        self.problem = problem
        self.client = OpenAI(
            base_url="输入中转地址",
            api_key="输入GPT密钥",
        )

    def run_code(self, code, timeout=600):
        with open("solve_code.py", "w", encoding='utf-8') as f:
            f.write(code)
        try:
            # 使用当前Python解释器运行脚本
            process = Popen([current_python_executable, "solve_code.py"], stdout=PIPE, stderr=PIPE)
            try:
                stdout, stderr = process.communicate(timeout=timeout)
                if process.returncode != 0:
                    return "Error", stderr.decode("utf-8", errors='ignore')
                else:
                    return "Success", stdout.decode("utf-8", errors='ignore')
            except TimeoutExpired:
                process.terminate()  # 使用 terminate 来替代 os.kill
                stdout, stderr = process.communicate()
                return "Timeout", "The code execution exceeded the timeout limit.Try to optimize the code, algorithm, or other techniques to reduce the execution time."
        except Exception as e:
            return "Error", str(e)

    def askLLM(self, messages, max_retries=10, delay=2):
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
                response = self.client.chat.completions.create(
                    model=MODEL, messages=messages, temperature=0.7, max_tokens=3000
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"尝试 {attempt + 1}/{max_retries} 失败: {e}")
                time.sleep(delay)
                attempt += 1

        print("重试次数已耗尽，未能成功获取响应。")
        return None

    def extract_code_block(self, code_block):
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

    def solve_problem(self):
        messages = [dict(role="system",
                         content="You are an expert Python programmer. Your task is to write Python code based on the "
                                 "user's requirements. Make sure to add appropriate explanations and your personal "
                                 "thought process to your code. Also, all of the codes should be encapsulated in "
                                 "Python code blocks. "
                                 "the package you can use : numpy,scipy,pandas,sympy,statsmodels,scikit-learn ."
                                 "If you try to import another external package and encounter an error, don't say that it"
                                 "can't be imported. Instead, try to write a new code that avoids this issue. "
                                 "Always output complete code rather than just giving advice or partially modified "
                                 "code, because your code will be run directly. "
                                 "Include test cases with your code, if they are necessary for immediate execution to "
                                 "check for possible bugs. "
                                 "In your response, only the code that needs to be run should be wrapped in multiline "
                                 "code blocks. No other multiline code blocks should appear."
                                 "Your code needs to print out the output after running."
                                 "Your code should not print error messages."
                                 "Output format:"
                                 "```python"
                                 "{Your code}"
                                 "```"
                                 "使用中文输出回答。"),
                    dict(role="user", content=self.problem)]
        result = []
        i = 0
        while i < 3:
            text = self.askLLM(messages)
            code = self.extract_code_block(text)
            status, output = self.run_code(code)

            d = {"role": "assistant", "content": text + status + output}
            result.append(d["content"])
            messages.append(d)

            if status == "Success":
                return result

            time.sleep(2)
            # if i > 1:
            #     del messages[-1]
            i += 1

        return result


def main():
    programmer = Python_Programmer("用蒙特卡洛算法，写一个python代码，求解一个a=3,b=4,高为5的椭球的体积")
    print(programmer.solve_problem())


if __name__ == "__main__":
    main()
