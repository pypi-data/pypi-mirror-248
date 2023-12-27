
[Paper link](https://arxiv.org/abs/2311.08562)

## Introduction

MAgIC is the benchmark to assess LLM-powered multi-agents' capabilities including cognition, adaptability, rationality and collaboration. Based on it, you can quantitatively measure your own LLM's ability and compare it with the cutting-edge LLMs.

## Installation

```bash
pip install MAgIC_LLM==0.6.0
```

Need to assign the OPENAI_API_KEY, if you are trying to use openai api
```bash
export OPENAI_API_KEY=""
```


## Usage

To assess your own large language model, follow the below instructions

```python

import MAgIC_LLM
import time
import openai
import google.generativeai as palm
import cohere
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT


# Here we use GPT-4-turbo as the example
def chatbox(messages,temperature,max_tokens):
    time.sleep(9)
    response = openai.ChatCompletion.create(model="gpt-4-1106-preview",
                                        messages=messages,                          
                                        temperature = temperature,
                                        n=3,
                                        max_tokens=max_tokens)
    response = response['choices'][0]['message']['content']
    #print(response)
    return response


# configure the path you want to save the assessment results
path = 'result.json' 

# Here is the name of your own LLM
test_player_model_name = 'My_LLM'

MAgIC_LLM.run(chatbox,path,test_player_model_name,PGM=False)
```

If any interruption happens in the process, you can just simple re-excute your programme and it will continue to assess your LLM from the point where interruption happens.

Currently, PGM method can be used to enhance your own LLM, the usage is below:

```
MAgIC_LLM.run(chatbox,path,test_player_model_name,PGM=True)
```

## License
MIT License


