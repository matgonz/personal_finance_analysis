from ofx_dataprep import OfxDataPrep


if __name__ == '__main__':

    _path = 'D:/GitHub/_data/personal_finances/input'
    _output = 'D:/GitHub/_data/personal_finances/output'

    dataprep = OfxDataPrep()
    transactions = dataprep.read_data(data_path=_path)
    transactions = dataprep.dataprep(transactions)
    transactions.to_csv(f'{_output}/transactions.csv', index=False, encoding='utf-8')