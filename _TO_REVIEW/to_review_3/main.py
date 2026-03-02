from src.ofx_dataprep import OfxDataPrep
from src.llm_finance import LLMFinance

# Inner the root path we have the folders input, output and processed
input_path = "D:\GitHub\_DADOS\personal_finances\input"
output_path = "D:\GitHub\_DADOS\personal_finances\output"


dataprep = OfxDataPrep()

if __name__ == "__main__":

    # Read OFX files and transform it in tabular data
    transactions = dataprep.read_and_prep_data(data_path=input_path)
    print(transactions.shape)

    #Group messages to get unique messages
    trans_grouped = transactions.groupby('memo')['id'].apply(list).reset_index(name='id_list')
    print(trans_grouped.shape)
    
    # Classifying transactions
    llm_finance = LLMFinance(model_name="llama-3.1-8b-instant")
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
    transactions.to_csv(f"{output_path}/transactions.csv", 
                        encoding='utf-8', 
                        index=False)