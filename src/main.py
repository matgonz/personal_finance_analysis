from ofx_dataprep import OfxDataPrep
from llm_finance import LLMFinance


if __name__ == '__main__':

    _path = 'D:/GitHub/_data/personal_finances/input'
    _output = 'D:/GitHub/_data/personal_finances/output'

    dataprep = OfxDataPrep()
    transactions = dataprep.read_data(data_path=_path)
    transactions = dataprep.dataprep(transactions)

    #Group messages to get unique messages
    trans_grouped = transactions.groupby('memo')['id'].apply(list).reset_index(name='id_list')
    
    # Classifying transactions
    llm_finance = LLMFinance()
    category = []
    for text in trans_grouped["memo"]:
        category.append(llm_finance.classify_transactions(text))
    trans_grouped['category'] = category

    # Merge
    transactions = transactions.merge(\
                                        trans_grouped.explode('id_list')[['id_list', 'category']], 
                                        left_on='id', 
                                        right_on='id_list', 
                                        how='left')\
                                .drop(columns=['id_list'])

    # Save classification
    transactions.to_csv(f"{_output}/transactions.csv", 
                        encoding='utf-8', 
                        index=False)