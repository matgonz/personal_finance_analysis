import os
from typing import List
from ofxparse import OfxParser
import pandas as pd

class OfxDataPrep:
    
    def __init__(self):
        pass

    def read_data(self, data_path: str) -> pd.DataFrame:
        """
        Reads OFX files from a specified directory and returns a DataFrame containing transaction data.
        Args:
            data_path (str): The path to the directory containing OFX files.
            Returns:
            pd.DataFrame: A DataFrame containing transaction data.
        """

        _arr_transactions = []
        _files = self.list_ofx_files(data_path=data_path)
        for file in _files:
            with open(file, 'r', encoding='ISO-8859-1') as ofx_file:
                _ofx = OfxParser.parse(ofx_file)
                
                account_data = self.get_account_data(_ofx.account)
                
                transactions_data = self.get_transaction_data(account_data, 
                                                            _ofx.account.statement.transactions)
                
                _arr_transactions.append(transactions_data)

        transactions_dataframe = pd.concat(_arr_transactions)

        return transactions_dataframe
    
    def list_ofx_files(self, data_path: str) -> List[str]:
        """
        Lists all OFX files in a specified directory.
        Args:
            data_path (str): The path to the directory containing OFX files.
        Returns:
            List[str]: A list of file paths for all OFX files in the directory.
        """
        return [os.path.join(data_path, file) \
                for file in os.listdir(data_path) \
                if file.endswith('.ofx')]

    def get_account_data(self, account) -> pd.DataFrame:
        """
        Extracts and returns account data from an OFX object.
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
        _arr_transactions = []
        for t in transactions:
            transaction_data = {
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
            }
            _arr_transactions.append(transaction_data)
        
        transactions_dataframe = pd.DataFrame(_arr_transactions)
        
        # Merge account data into each transaction
        for key, value in account_data.items():
            transactions_dataframe[key] = value

        return transactions_dataframe

    def getTypeTransactionName(self, type: int) -> str:
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
        transactions_data['type'] = transactions_data['type'].apply(self.getTypeTransactionName)

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
        Reads and prepares data from the specified path.
        Args:
            data_path (str): The path to the directory containing OFX files.
        Returns:
            pd.DataFrame: A DataFrame containing the prepared transaction data.
        """

        _transactions = self.read_data(data_path=data_path)
        _transactions = self.dataprep(_transactions)

        return _transactions