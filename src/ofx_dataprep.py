import os
from typing import List
from ofxparse import OfxParser
import pandas as pd

class OfxDataPrep:
    
    def read_data(self, data_path: str) -> pd.DataFrame:
        """
        Reads OFX files from a specified directory and returns a DataFrame containing transactions data.
        Args:
            data_path (str): Path of OFX file.
            Returns:
            pd.DataFrame: A DataFrame containing transactions data.
        """
        try:
            with open(data_path, 'r', encoding='ISO-8859-1') as ofx_file:

                ofx = OfxParser.parse(ofx_file)
                account_data = self.get_account_data(ofx.account)
                transactions_data = self.get_transaction_data(
                    account_data, 
                    ofx.account.statement.transactions
                )
                df_transactions = pd.DataFrame(transactions_data)
            return df_transactions

        except Exception as ex:
            raise Exception(f"Error reading OFX files: {ex}")

    def get_account_data(self, account) -> pd.DataFrame:
        """
        Extract and return account data from an OFX object.
        Args:
            ofx: An OFX object containing account information.
        Returns:
            dict: A dictionary containing the following account details:
                - account_id (str): The account ID.
                - number (str): The account number (deprecated, returns account_id).
                - routing_number (str): The bank routing number.
                - type (int): The account type (0 - Unknown, 1 - Bank, 2 - CreditCard, 3 - Investment).
                - institution (str): The name of the institution.
                - fid (str): The financial institution ID.
        """
        account_data = {
            'account_id': account.account_id,
            'number': account.number,          
            'routing_number': account.routing_number,
            'type': account.type,   
            'institution': account.institution.organization,
            'fid': account.institution.fid
        }
        return account_data
    
    def get_transaction_data(self, 
                             account_data: pd.DataFrame, 
                             transactions) -> pd.DataFrame:
        """
        Extracts and returns transaction data from an OFX object.
        Args:
            ofx: An OFX object containing transaction information.
        Returns:
            pd.DataFrame: A DataFrame containing the following transaction details:
                - payee (str): The payee name.
                - type (str): The transaction type.
                - date (datetime): The transaction date.
                - user_date (str): The transaction date in user-friendly format.
                - amount (float): The transaction amount.
                - id (str): The transaction ID.
                - memo (str): The transaction memo.
                - sic (str): The Standard Industrial Classification (SIC) code.
                - mcc (str): The Merchant Category Code (MCC).
                - checknum (str): The check number.
        """
        # _arr_transactions = []
        # for t in transactions:
        #     transaction_data = {
        #         'payee': t.payee,
        #         'type': t.type,
        #         'date': t.date,
        #         'user_date': t.user_date,
        #         'amount': t.amount,
        #         'id': t.id,
        #         'memo': t.memo,
        #         'sic': t.sic,
        #         'mcc': t.mcc,
        #         'checknum': t.checknum
        #     }
        #     _arr_transactions.append(transaction_data)

        arr_transactions = [
            {
                'payee': t.payee,
                'type': t.type,
                'date': t.date,
                'user_date': t.user_date,
                'amount': t.amount,
                'id': t.id,
                'memo': t.memo,
                'sic': t.sic,
                'mcc': t.mcc,
                'checknum': t.checknum
            } for t in transactions
        ]
        df_transactions = pd.DataFrame(arr_transactions)
        
        # Merge account data into each transaction
        for key, value in account_data.items():
            df_transactions[key] = value

        return df_transactions

    def get_type_transaction_name(self, type: int) -> str:
        """
        """
        type_dict = {
            0: 'Unknown',
            1: 'Bank',
            2: 'Credit Card',
            3: 'Investment'
        }
        try:
            return type_dict[type]
        except KeyError:
            return 'Unknown'

    def dataprep(self, transactions_data: pd.DataFrame) -> pd.DataFrame:
        """
        """

        # Cast to datetime
        transactions_data['date'] = pd.to_datetime(transactions_data['date'])
        transactions_data['year'] = transactions_data['date'].dt.year
        transactions_data['year_month'] = transactions_data['date'].dt.to_period('M')
        transactions_data['date'] = transactions_data['date'].dt.date

        # Get transaction type name
        transactions_data['type'] = transactions_data['type'].apply(self.get_type_transaction_name)

        # Amount
        transactions_data["amount"] = transactions_data["amount"].astype(float)

        # Classify transactions as income or expense
        transactions_data['in_out'] = transactions_data['amount'].apply(lambda x: 'in' if x > 0 else 'out')

         # flag transactions where contains installment number
        installment_pattern = r"\b(?:0|[1-9]|[1-9][0-9]|100)/(?:0|[1-9]|[1-9][0-9]|100)\b"
        transactions_data['is_installment'] = transactions_data['memo'].str.contains(installment_pattern)

        # Drop unnecessary columns
        drop_columns = ['payee', 'user_date', 'sic', 'mcc', 'checknum', 'routing_number', 'fid']
        transactions_data.drop(columns=drop_columns, inplace=True)

        return transactions_data
    
    def read_and_prep_data(self, data_path: str) -> pd.DataFrame:
        """
        Read and prepare data from the specified path.
        Args:
            data_path (str): The path to the directory containing OFX files.
        Returns:
            pd.DataFrame: A DataFrame containing the prepared transaction data.
        """

        _transactions = self.read_data(data_path=data_path)
        _transactions = self.dataprep(_transactions)

        return _transactions