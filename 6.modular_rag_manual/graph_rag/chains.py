from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from config import LLM_MODEL
from prompts import evidence_prompt, answer_prompt, validation_prompt

llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

evidence_chain = evidence_prompt | llm | StrOutputParser()
answer_chain = answer_prompt | llm | StrOutputParser()
validation_chain = validation_prompt | llm | StrOutputParser()