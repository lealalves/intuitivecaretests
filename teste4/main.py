import re
import pandas as pd
from flask import Flask, request
from flask_cors import CORS

# lendo o CSV
df = pd.read_csv('Relatorio_cadop.csv', encoding='iso-8859-1', on_bad_lines='skip', sep=';', skiprows=1, dtype=str, keep_default_na=False)

# configurando o modulo flask
app = Flask(__name__)
CORS(app)

# dataframe vazio
dfr = pd.DataFrame()
# listando as colunos do csv
dfc = list(df.columns)


# rota /cadastros, que tem uma query parameter opcional: busca
@app.get('/cadastros')
def cadastros():
    args = request.args

    busca = args.get('busca')
    # realizando busca coluna por coluna
    if busca:
        # lista vazia de possiveis resultados
        result_list = []
        for i in range(len(dfc)):
            filter = df[dfc[i]].str.contains(busca, flags=re.UNICODE, case=False)
            result = df[filter]

            if len(result) > 0:
                # resultados são adicionado a lista de resultados
                result_list.append(result)

        if len(result_list) == 0:
            return result_list
        # é concatenado a lista junto ao dataframe vazio criado, e removendo duplicatas
        dfr = pd.concat(result_list, ignore_index=True).drop_duplicates()
        # é retornado ao frontend o json do dataframe contendo o resultado da busca
        return dfr.to_json(force_ascii=False, orient='values')
    else:
        return df.to_json(force_ascii=False, orient='values')


app.run(port=3000)




