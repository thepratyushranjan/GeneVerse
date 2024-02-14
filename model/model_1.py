from langchain.chat_models import ChatOpenAI
from prompt.prompt_1 import prompt
from langchain.chains import LLMChain
from dotenv import load_dotenv
load_dotenv()
 
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
global chain
chain = LLMChain(llm=llm, prompt = prompt)

def generate_response(message):
    best_practice = "Hello"
    response = chain.run(message = message, best_practice = best_practice)
    return response