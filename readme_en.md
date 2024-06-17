# Math-Multi-Agent

> Solution for the project "Special Agent Universe," which won the 2nd place globally in the AI track at the 2024 Alibaba Global Mathematics Competition.

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
     English | <a href="./readme.md" >简体中文</a>
    <br />
    <a href="https://github.com/isaacJinyu/Math-Multi-Agent/issues">Report Bug</a>
    ·
    <a href="https://github.com/isaacJinyu/Math-Multi-Agent/issues">Request Feature</a>
  </p>

</p>

## 🎯News
- [2024.6] 🎉🎉 We have open-sourced all our code!

## Table of Contents

- [Directory Structure](#🌴directory-structure)
- [How to Run](#🎨how-to-run)
- [Project Principle](#🛠project-principle)
- [Team Members](#🤗team-members)
- [Acknowledgements](#acknowledgements)

### 🌴Directory Structure
```
filetree
├── imgs/: Image resources
├── LICENSE.txt
├── README.md
├── /src/: Core code
│ ├── /action/
│ │ ├── Calculate.py
│ │ └── Programmer.py
├── main.py: Main function
├── requirements.txt: Lists the required Python libraries and their versions.
```

### 🎨How to Run
First, clone the repository:
```sh
git clone https://github.com/isaacJinyu/Math-Multi-Agent.git
```
Then follow these steps:
1. Ensure all libraries listed in `requirements.txt` are installed. 
   ```
   pip install -r requirements.txt
   ```
2. Enter your keys and proxy address in `main.py` and `action/Programmer.py`, including keys for OpenAI and Anthropic.
   ```
   api_key = "Enter the respective company's key"  
   base_url = "Enter the proxy address (if not connecting directly, do not use base_url)"
   ```
3. Enter your Wolfram|Alpha API key in the wolfram_alpha action in `main.py`
   ```
   app_id = 'Enter Wolfram|Alpha API key'
   ```
4. Enter your math question in question in `main.py`.
5. Run `python main.py` in the command line to start the project.
6. Check the `Final_answer.txt` file for the final answer.
7. To see the problem-solving process of each agent, find ``.txt` files named after the agent numbers in the current directory.

### 🛠Project Principle
<p align="center">
  <img src="./imgs/solve.png" alt="Logo" width="500" >
</p>

### 🤗Team Members
- Xiang Jinyu: Southwest Jiaotong University
- Wang Xunzhi: Nankai University
- Fei Qingyu: Graduate of the University of Bristol, currently a Product Manager at Tencent
- Zhang Ziqiu: City University of Macau

### Acknowledgements
- Special Agent Universe
- ...



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
