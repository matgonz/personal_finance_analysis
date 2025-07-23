import pandas as pd

class DataAnalysis:

    def __init__(self, data):
        self.data = data

    def cc_summarizer_by_month(self) -> pd.DataFrame:
        """
        Perform analysis on credit card transactions.
        This function filters the transactions for credit card type,
        excludes certain rows based on conditions, and calculates the total
        amount for each month. It also distinguishes between transactions
        that are installments and those that are not.

        The function returns a DataFrame with the following columns:
        - year_month: The year and month of the transaction.
        - cc_total_out: Total amount of credit card transactions for the month.
        - cc_total_out_no_installments: Total amount of credit card transactions for the month
            that are not installments.
        - cc_out_installment: Total amount of credit card transactions for the month that are installments.
        
        The function also excludes transactions where the type is "Credit Card" and in_out is "in",
        and where the memo contains "Saldo em atraso".
        """
        ## Filter transactions for Credit Card type
        _data = self.data.query("type == 'Credit Card'").copy()
        # Exclude rows where type is "Credit Card" and in_out is "in"
        _data = _data[~((_data["type"] == "Credit Card") & (_data["in_out"] == "in"))]
        # Exclude rows where memo contains "Saldo em atraso"
        _data = _data[~_data['memo'].str.contains("Saldo em atraso", na=False)]
        
        # Convert the 'amount' column to positive values
        _data['amount'] = _data['amount'].apply(lambda x: x * -1 if x < 0 else x)

        # Calculate total amount for each month
        cc_total_out = _data.query('in_out == "out"')\
                            .groupby(['year_month'])['amount']\
                            .sum()\
                            .reset_index(name='cc_total_out')
        # Calculate total amount for each month where is_installment is False
        cc_total_out_no_installments = _data.query('in_out == "out" and is_installment == False')\
                                            .groupby(['year_month'])['amount']\
                                            .sum()\
                                            .reset_index(name='cc_total_out_no_installments')
        # Calculate total amount for each month where is_installment is True
        cc_out_installment = _data.query('in_out == "out" and is_installment == True')\
                                    .groupby(['year_month'])['amount']\
                                    .sum()\
                                    .reset_index(name='cc_total_out_installments')
        # Merge all results
        result = cc_total_out.merge(cc_total_out_no_installments, on="year_month", how="left")
        result = result.merge(cc_out_installment, on="year_month", how="left")
        result.fillna(0, inplace=True)

        return result
