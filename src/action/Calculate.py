import json
import urllib.parse
import requests
from sympy.parsing.latex import parse_latex

class WolframAlphaQuery:
    def __init__(self, app_id):
        self.app_id = app_id

    def clean_json(self, json_str):
        # 清理JSON数据中的转义字符
        json_str = json_str.replace('\n', '').replace('\\/', '/')
        json_str = json_str.replace('\\t', '').replace('\\r', '').replace('\\b', '').replace('\\f', '')
        return json_str

    def send_query(self, input_expression):
        # 清理输入表达式
        input_expression = urllib.parse.quote(input_expression)
        # 构建查询URL
        query_url = f'http://api.wolframalpha.com/v2/query?appid={self.app_id}&input={input_expression}&output=json'
        # 发送GET请求
        response = requests.get(query_url)
        # 检查请求是否成功
        if response.status_code == 200:
            # 解析响应内容
            data = response.json()
            return data
        else:
            print(f"Request failed with status code {response.status_code}")
            return None

    def process_response(self, data):
        # 初始化Markdown字符串
        markdown_content = ""

        # 提取并结构化信息
        if data["queryresult"]["success"] is True:
            for pod in data["queryresult"]["pods"]:
                pod_title = pod.get("title", "Untitled")
                subpods = pod.get("subpods", [])
                if subpods:
                    subpod_plaintext = subpods[0].get("plaintext", "No plaintext available")

                    # 将提取的信息添加到Markdown字符串
                    markdown_content += f"## {pod_title}\n"
                    markdown_content += f"{subpod_plaintext}\n\n"
            return markdown_content
        else:
            return "WolframAlpha计算失败，请尝试更换表达式或更换方法"

def simple_calculate(latex_expression):
    # 解析 LaTeX 表达式为 SymPy 表达式
    expression = parse_latex(latex_expression)

    # 尝试计算表达式的值
    try:
        result = expression.evalf()  # 否则直接计算
    except Exception as e:
        return f"Error: {e}"

    return result

def main():
    # 简单计算使用示例
    latex_expression = r"\int_{0}^{5} \frac{x^{3}}{5+3x} dx"

    # 调用 simple_calculate 函数进行计算
    result = simple_calculate(latex_expression)

    # 打印结果
    print("simple_calculate 函数\n")
    print(f"函数/方程: {latex_expression}")
    print(f"Result: {result}")

    # 复杂计算使用示例
    app_id = '输入Wolfram|Alpha API密钥'  # Wolfram|Alpha API密钥
    query = WolframAlphaQuery(app_id)

    # 查询表达式
    input_expression = r"\int_{0}^{5} \frac{x^{3}}{5+3x} \cdot \frac{x+5}{x+2}"
    response_data = query.send_query(input_expression)

    print("\nWolframAlphaQuery方法\n")
    # 处理并打印Markdown内容
    if response_data:
        markdown_content = query.process_response(response_data)
        print(markdown_content)

if __name__ == "__main__":
    main()



