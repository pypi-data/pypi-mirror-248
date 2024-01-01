# Bash GPT

This is a simple bash script that uses OpenAI's GPT-4 to write bash commands to answer your questions. For instance see the below screenshots of the tool in action:

![Example 1](./examples/example1.png)
![Example 2](./examples/example2.png)
![Example 3](./examples/example3.png)

You can also pass the --explain parameter to give a reason why that command was chosen and what the output means:

![Example 4](./examples/example4.png)

## Installation

You can either install from source or install direct from PyPi using:

```bash
pip install bash-gpt
```

## Deployment

Give deploy.sh execution permissions with chmod +x deploy.sh, and then run it with ./deploy.sh.