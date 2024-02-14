from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from prompt.prompt import prompt
from langchain.chains import LLMChain


def model(chunks, embeddings):
    global db
    db = FAISS.from_documents(chunks, embeddings)

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    global chain
    chain = LLMChain(llm=llm, prompt = prompt)
    # chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff", prompt=prompt)

    # Redirect to the new page where the PDF will be displayed
    return db, chain
