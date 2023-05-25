import re
import pandas as pd
from flask import Flask, jsonify, request, json

df = pd.read_csv('Relatorio_cadop.csv', encoding='iso-8859-1', on_bad_lines='skip', sep=';', skiprows=1, dtype=str, keep_default_na=False)

# app = Flask(__name__)
# json.provider.DefaultJSONProvider.ensure_ascii = False

dfr = pd.DataFrame()

dfc = list(df.columns)

for i in range(len(dfc)):
    filter = df[dfc[i]].str.contains('registro', flags=re.UNICODE, case=False)
    result = df[filter]

    print(f'{len(result)} resultados na coluna: {dfc[i]}')
    print(f'RESULTADO: {result}')

    if len(result) > 0:
        print(f'LISTA ANTES: {dfr}, TAMANHO {len(dfr)}')

        dfr = pd.concat([result])

        print('ADICIONOU VALORES')
        print(f'LISTA DEPOIS: {dfr}, TAMANHO {len(dfr)}')

print(f'RESULTADO FINAL: {dfr}, TAMANHO {len(dfr)}')

# @app.route('/')
# def hello_word():
#     return 'Hello Word!'
#
#
# @app.get('/cadastros')
# def cadastros():
#     args = request.args
#     busca = args.get('busca')
#
#     if busca:
#         dfr = pd.DataFrame()
#
#         dfc = list(df.columns)
#
#         for i in range(len(dfc)):
#             filter = df[dfc[i]].str.contains(busca, flags=re.UNICODE, case=False)
#
#             print(f'{len(df[filter])} resultados na coluna: {dfc[i]}')
#
#             if len(df[filter]) > 0:
#                 dfr = pd.concat([df[filter]])
#
#         data = dfr.to_json(force_ascii=False, orient='records')
#         return jsonify(data)
#     else:
#         data = df.to_json(force_ascii=False, orient='records')
#         return jsonify(data)
#
#
# app.run(port=3000)




