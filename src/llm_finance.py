from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv, find_dotenv
import pandas as pd
from _prompt import _PROMPT_TEMPLATE

# from langchain_openai import ChatOpenAI
# from openai import OpenAI
# from langchain_core.output_parsers.string import StrOutputParser


class LLMFinance:

    def __init__(self):
        # Load environment variables
        _ = load_dotenv(find_dotenv())
        
        # Create model instance
        self.model_instance()

    def model_instance(self):
        """
        Create model instance
        """
        # Create prompt
        self.prompt = PromptTemplate.from_template(template=_PROMPT_TEMPLATE)
        # Create chat
        self.chat = ChatGroq(model="llama-3.1-8b-instant")
        # Using Groq LLM
        self.chain = self.prompt | self.chat


    def classify_transactions(self, transaction_memo: str) -> pd.DataFrame:
        """
        Classify transactions
        """
        category = self.chain.invoke(transaction_memo).content
        return category
        


