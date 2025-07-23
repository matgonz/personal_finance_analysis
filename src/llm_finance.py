# from langchain_groq import ChatGroq
# from langchain_core.prompts import PromptTemplate
# from dotenv import load_dotenv, find_dotenv
# import pandas as pd
# from prompt_personal_finance import _PROMPT_TEMPLATE
# from typing import Union, List

# class LLMFinance:

#     def __init__(self, model_name: str):
#         # Load environment variables
#         _ = load_dotenv(find_dotenv())
        
#         # Create model instance
#         self.model_instance(model_name=model_name)

#     def model_instance(self, model_name: str):
#         """
#         Create model instance
#         """
#         # Create prompt
#         self.prompt = PromptTemplate.from_template(template=_PROMPT_TEMPLATE)
#         # Create chat
#         self.chat = ChatGroq(model=model_name)
#         # Using Groq LLM
#         self.chain = self.prompt | self.chat


#     def classify_transactions(self, transaction_memo: str) -> pd.DataFrame:
#         """
#         Classify transactions
#         """
#         category = self.chain.invoke(transaction_memo).content
#         return category
    
#     def classify_batch(self, transactions: Union[List[str], pd.Series]) -> pd.DataFrame:
#         """
#         Classify a list or Series of transactions and return a DataFrame
#         """
#         results = []
#         for memo in transactions:
#             try:
#                 category = self.classify_transaction(memo)
#                 results.append((memo, category))
#             except Exception as e:
#                 results.append((memo, f"Erro: {e}"))

#         return pd.DataFrame(results, columns=["transacao", "categoria"])


import time
import pandas as pd
from typing import List, Union
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv, find_dotenv
from src.prompt_personal_finance import _PROMPT_TEMPLATE


# Model limits of main Groq's model available on free tier
MODELS_LIMITS = {
    "llama3-8b-8192": {"rpm": 30},
    "gemma2-9b-it": {"rpm": 30},
    "deepseek-r1-distill-llama-70b": {"rpm": 30},
}


class LLMFinance:

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model_limits = MODELS_LIMITS.get(model_name, {"rpm": 30})
        self._last_minute_requests = []

        _ = load_dotenv(find_dotenv())
        self.model_instance(model_name)

    def model_instance(self, model_name: str):
        self.prompt = PromptTemplate.from_template(template=_PROMPT_TEMPLATE)
        self.chat = ChatGroq(model=model_name)
        self.chain = self.prompt | self.chat

    def classify_transaction(self, transaction_memo: str) -> str:
        response = self.chain.invoke({"text": transaction_memo})
        return response.content.strip()

    def throttle_if_needed(self):
        """
        Throttle requests to respect the model's RPM limit.
        This method checks the number of requests made in the last minute and waits if necessary.
        """
        now = time.time()
        self._last_minute_requests = [t for t in self._last_minute_requests if now - t < 60]

        if len(self._last_minute_requests) >= self.model_limits["rpm"]:
            time_to_wait = 60 - (now - self._last_minute_requests[0])
            print(f"[Throttle] Waiting for {time_to_wait:.2f} seconds to respect RPM limit...")
            time.sleep(time_to_wait)
            self._last_minute_requests.pop(0)

    def classify_batch(self, transactions: Union[List[str], pd.Series]) -> pd.DataFrame:
        results = []
        for memo in transactions:
            try:
                self.throttle_if_needed()
                category = self.classify_transaction(memo)
                self._last_minute_requests.append(time.time())
                results.append((memo, category))
            except Exception as e:
                results.append((memo, f"Erro: {e}"))

        return pd.DataFrame(results, columns=["memo", "category"])
