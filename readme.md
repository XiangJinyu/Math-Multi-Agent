# 项目说明

这是一个用于解决数学问题的Multi-Agent的Python项目，它集成了多种方法来分析和解答问题。项目包含以下几个主要部分：

## 主要文件

- `requirements.txt`: 列出了项目所需的Python库及其版本。
- `main.py`: 项目的主程序文件，包含了问题的描述、解题过程和结果输出。
- `action`: 包含了部分可调用行为。

## 结果输出

- 项目的最终答案将输出到 `Final_answer.txt`文件中。
- 每个角色的解题过程和结果将分别保存在以角色编号命名的 `.txt`文件中，例如 `answer_article_1.txt`。
- 最近一次调用Programmer Agent编写并执行的代码输出到`solve_code.py`

## 如何运行

1. 确保已安装所有列出在 `requirements.txt`中的Python库。
   ```
   pip install -r requirements.txt
   ```
2. 在`main.py`及`action/Programmer.py`中填入你的密钥和中转地址，需要填写OpenAI和Anthropic两家公司的密钥。
   ```
   api_key = "输入对应公司的密钥"  
   base_url = "输入中转地址(若直连，则不使用base_url)"
   ```
3. 在`main.py`下的`choose_action`的`wolfram_alpha`这个action处的app_id输入你的Wolfram|Alpha API密钥
   ```
   app_id = '输入Wolfram|Alpha API密钥'
   ```
4. 在`main.py`下的`question`中填入你的数学问题
5. 在命令行中运行 `python main.py`来启动项目。
6. 查看输出的 `Final_answer.txt`文件获取最终答案。
7. 查看各个角色的解题过程，可以在当前目录下找到以角色编号命名的 `.txt`文件。


