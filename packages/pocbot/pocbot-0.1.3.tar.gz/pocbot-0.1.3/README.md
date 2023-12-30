# PocBot

## Description
Simple streamlit UI to implement chatbots.
- Objective: Develop a pip installable package to create easy ChatBot interfaces.
- Scope: First iteration - Simple UI. It should work out of the box.

To see it used in a real project, check out the [e-commerce chatbot](https://github.com/thisisqubika/data-studio-e-commerce)

## Installation
Installing is as easy as running `pip install pocbot` in your terminal. Make sure you have your virtual environment activated!

## Usage
Here's a basic example on how to use pocbot. Let's assume we are chatting with Pikachu, who only knows how to say "pika" a random number of times.

```python
from typing import Any, List
from pocbot.ui_template import ChatBotUITemplate
from pocbot.chain_template import ChatBotChain
from random import randint


# LLM Simulation
class Pikachu(ChatBotChain):
    """This is a test chain model"""
    def __init__(self):
        pass
    
    def invoke(self, input: str, chat_history: List[Any]) -> str:
        """"""
        return " ".join(["pika"] * randint(1, 10)) + "!"


# UI
pocbot = ChatBotUITemplate(name="PikaBot", chain=Pikachu())


if __name__ == "__main__":
    pocbot()
```

To get started, copy and paste this code in a file in your Python project. Then, one can run it as any other Streamlit app: `streamlit run <file_name>.py`

That's it! You should see a UI in port 8501.

### Brief Explanation
The `ChatBotUITemplate` class is whre the magic happens. It is thought out to be a simple class that helps one create a UI for a chatbot in a few lines of code. It has the following parameters:
- `name`: Name of the chatbot. It will be displayed in the UI.
- `chain`: `ChatBotChain` object. This is the chain that will be used to generate the responses. It is explained in the next section.

The `ChatBotChain` class is designed to act as an interface between the UI and the logic of the chatbot. It si pretty simple. The only constraint is that it must have an `invoke` method (see example above) defined. 


## Contributing
If you would like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome. 
You can find the repository [here](https://github.com/thisisqubika/pocbot)

## References
- [Streamlit](https://www.streamlit.io/)
- [Qubika's e-commerce chatbot](https://github.com/thisisqubika/data-studio-e-commerce)
