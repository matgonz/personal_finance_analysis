_PROMPT_TEMPLATE = """
Você é um analista de dados, trabalhando em um projeto de limpeza de dados.
Seu trabalho é escolher uma categoria adequada para cada lançamento financeiro
que vou te enviar em um arquivo csv.

Todas as transações são transações financeiras de uma pessoa física e correspondem a transações de um cartão de crédito.

Escolha uma dentre as seguintes categorias:
- Assinaturas e Serviços: Sempre que tiver "Cinemark","Wellhub","Netflix","Facebk","Openai","Ebn*Spotify" no nome da transação
- Transporte: Sempre que tiver "Uber","Top Sp","Buser" no nome da transação
- Mercado: Sempre que tiver "Extra Hiper","Nagumo","Minimercado" no nome da transação
- Horti Fruti: Sempre que tiver "Horti Fruti" no nome da transação
- Compras Parceladas: Sempre que tiver "Parcela" no nome da transação
- Saúde: Sempre que tiver "Drogasil" no nome da transação
- Restaurantes: Sempre que tiver "Black Dogs" no nome da transação
- Telefone: Sempre que tiver "Recarga de celular" no nome da transação
- Posto de Gasolina

Escolha a categoria deste item:
{text}

Responda apenas com a categoria correspondente sem pontuação.
"""

# - Receitas: Sempre que tiver "Transferência recebida pelo Pix - MATHEUS GONZALEZ EUGENIO" no nome da transação
# - Moradia: Sempre que tiver "ELETROPAULO","Pagamento de boleto efetuado - PJBANK PAGAMENTOS S A","CONDOMINIO EDIFICIO" no nome da transação
# - Fatura: Sempre que tiver "Pagamento de fatura","Pagamento recebido" no nome da transação
# - Investimento: Sempre que tiver "RDB","NuInvest" no nome da transação
# - Transferências para terceiros