

# Math-Multi-Agent

> 2024年阿里全球数学竞赛AI赛道全球第2名项目（特工宇宙）解决方案。

<!-- PROJECT SHIELDS -->
<!-- [![Contributors][contributors-shield]][contributors-url] -->
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
<!-- [![MIT License][license-shield]][license-url] -->


<!-- PROJECT LOGO -->
<br />

<p align="center">
  <a href="https://github.com/isaacJinyu/Math-Multi-Agent">
    <img src="./imgs/logo.webp" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Math-Multi-Agent</h3>
  <p align="center">
    简体中文 | <a href="./readme_en.md" >English</a>
    <br />
    <a href="https://github.com/isaacJinyu/Math-Multi-Agent/issues">报告Bug</a>
    ·
    <a href="https://github.com/isaacJinyu/Math-Multi-Agent/issues">提出新特性</a>
  </p>

</p>

## 🎯News
- [2024.6] 🎉🎉我们开源了我们的所有代码！

## 目录

- [文件目录说明](#🌴文件目录说明)
- [如何运行](#🎨如何运行)
- [项目原理](#🛠项目原理)
- [项目成员](#🤗成员)
- [鸣谢](#鸣谢)

### 🌴文件目录说明 
```
filetree 
├── imgs/：存放图像资源
├── LICENSE.txt
├── README.md
├── /src/：核心代码
│  ├── /action/
│  │  ├── Calculate.py
│  │  └── Programmer.py
├── main.py：主函数
├── requirements.txt： 列出了项目所需的Python库及其版本。
```

### 🎨如何运行 
首先克隆仓库：
```sh
git clone https://github.com/isaacJinyu/Math-Multi-Agent.git
```

然后依次执行如下步骤：
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


### 🛠项目原理
<p align="center">
  <img src="./imgs/solve.png" alt="Logo" width="500" >
</p>

### 🤗成员
- 向劲宇：西南交通大学
- 王训志：南开大学
- 费清语：布里斯托大学毕业，目前腾讯产品经理
- 张紫璆：澳门城市大学

### 鸣谢
- 特工宇宙
- …


<!-- links -->
[your-project-path]:isaacJinyu/Math-Multi-Agent
[contributors-shield]: https://img.shields.io/github/contributors/isaacJinyu/Math-Multi-Agent/graphs.svg?style=flat-square
[contributors-url]: https://github.com/isaacJinyu/Math-Multi-Agent/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/isaacJinyu/Math-Multi-Agent.svg?style=flat-square
[forks-url]: https://github.com/isaacJinyu/Math-Multi-Agent/network/members
[stars-shield]: https://img.shields.io/github/stars/isaacJinyu/Math-Multi-Agent.svg?style=flat-square
[stars-url]: https://github.com/isaacJinyu/Math-Multi-Agent/stargazers
[issues-shield]: https://img.shields.io/github/issues/isaacJinyu/Math-Multi-Agent.svg?style=flat-square
[issues-url]: https://img.shields.io/github/issues/isaacJinyu/Math-Multi-Agent.svg
[license-shield]: https://img.shields.io/github/license/isaacJinyu/Math-Multi-Agent.svg?style=flat-square
[license-url]: ./LICENSE.txt




