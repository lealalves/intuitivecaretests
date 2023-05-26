import re
import pandas as pd
from flask import Flask, request

df = pd.read_csv('Relatorio_cadop.csv', encoding='iso-8859-1', on_bad_lines='skip', sep=';', skiprows=1, dtype=str, keep_default_na=False)

app = Flask(__name__)

dfr = pd.DataFrame()

dfc = list(df.columns)


@app.route('/')
def hello_word():
    return 'Hello Word!'


@app.get('/cadastros')
def cadastros():
    args = request.args

    busca = args.get('busca')
    skip = 0 if args.get('skip') is None else int(args.get('skip'))
    limit = 10 if args.get('limit') is None else int(args.get('limit'))

    if busca:
        result_list = []
        for i in range(len(dfc)):
            filter = df[dfc[i]].str.contains(busca, flags=re.UNICODE, case=False)
            result = df[filter]

            if len(result) > 0:
                result_list.append(result)

        if len(result_list) == 0:
            return {
                'message': 'No results found'
            }

        dfr = pd.concat(result_list, ignore_index=True).drop_duplicates()
        data = dfr.loc[skip:limit]

        return data.to_json(force_ascii=False)
    else:
        data = df.loc[skip:limit]
        return data.to_json(force_ascii=False)


app.run(port=3000, debug=True)




