import re
import pandas as pd
from flask import Flask, request
from flask_cors import CORS
df = pd.read_csv('Relatorio_cadop.csv', encoding='iso-8859-1', on_bad_lines='skip', sep=';', skiprows=1, dtype=str, keep_default_na=False)

app = Flask(__name__)
CORS(app)

dfr = pd.DataFrame()

dfc = list(df.columns)


@app.route('/')
def hello_word():
    return 'Hello Word!'


@app.get('/cadastros')
def cadastros():
    args = request.args

    busca = args.get('busca')

    if busca:
        result_list = []
        for i in range(len(dfc)):
            filter = df[dfc[i]].str.contains(busca, flags=re.UNICODE, case=False)
            result = df[filter]
            print(busca)
            print(f'{len(result)} resultados na coluna {dfc[i]}')
            if len(result) > 0:
                result_list.append(result)

        if len(result_list) == 0:
            print('sem resultados')
            return result_list

        dfr = pd.concat(result_list, ignore_index=True).drop_duplicates()

        return dfr.to_json(force_ascii=False, orient='values')
    else:
        return df.to_json(force_ascii=False, orient='values')


app.run(port=3000, debug=True)




