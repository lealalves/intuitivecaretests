import tabula
import pandas as pd
from zipfile import ZipFile, ZIP_DEFLATED

df = pd.DataFrame()

print('Extraindo tabelas...')
for i in range(3, 181):
    print(f'Pagina atual: {i}')
    tabela = tabula.read_pdf('Anexo I - Lista completa de procedimentos (.pdf).pdf', pages=f'{i}', output_format='dataframe')

    dft = tabela[0]

    # substituindo valores OD e AMB para seus respectivos significado na legenda da tabela
    update_dft = dft.replace({'OD': 'Seg. Odontológica', 'AMB': 'Seg. Ambulatorial'})

    # concatenando a tabela(dft) atual a varivel df
    df = pd.concat([df, update_dft])

print('Convertendo para CSV...')
# removendo colunas unnamed
df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1, inplace=True)
df.to_csv('Anexo I.csv', encoding='UTF-16')

print('Comprimindo...')
arquivozip = ZipFile('Teste_Vinicius_Leal_Alves.zip', 'w', compression=ZIP_DEFLATED)
arquivozip.write('Anexo I.csv')
arquivozip.close()

print('Compressão finalizada.')


