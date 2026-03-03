import time
import pandas as pd
from typing import List, Union
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv, find_dotenv
from src.prompt_personal_finance import _PROMPT_TEMPLATE

# Model limits of main Groq's model available on free tier
MODELS_LIMITS = {}

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
