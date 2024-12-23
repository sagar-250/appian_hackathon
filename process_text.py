from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)
def process(text:str)->str:
    system = "You are a helpful assistant. whose work is clean up and organize given text . there might be some time the text is of a application form .. so you also need to add 'no value' .. if there is no value infront of a particular field"
    human = "{text}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
    system = "You are a helpful assistant."
    chain = prompt | llm
    response=chain.invoke({"text": text})
    print(response.content)
    return response.content

