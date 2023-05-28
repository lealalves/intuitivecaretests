import requests
import os
from bs4 import BeautifulSoup
from lxml import etree
from zipfile import ZipFile, ZIP_DEFLATED

# definindo o diretorio absoluto
main_path = os.path.dirname(__file__)

# checando se a pasta output existe. se nao existe, cria ela
# a pasta output é para onde vai os arquivos baixados
output_path = os.path.join(main_path, 'output')
isExist = os.path.exists(output_path)
if not isExist:
    os.makedirs(output_path)


# função que faz o download, recebendo como parametro a url, nome do novo arquivo a ser salvo e o formato
def download(url, name, format):
    final_path = os.path.join(output_path, f'{name}.{format}')

    res = requests.get(url)
    if res.status_code == requests.codes.OK:
        # criando um novo arquivo e escrevendo nele o binario do arquivo que é requisitado pela url passada como parametro
        with open(final_path, 'wb') as novo_arquivo:
            novo_arquivo.write(res.content)
        print(f'Download Finalizado! Arquivo salvo em {final_path}')
    else:
        res.raise_for_status()


# função que compacta todos os arquivos dentro da pasta output
def compactar_output():
    print('Compactando arquivos...')
    # lista o nome de todos os arquivos dentro da pasta output
    nomes_arquivo = os.listdir(output_path)
    # varivel nome_zip define onde vai ser salvo o zip e o seu nome
    nome_zip = os.path.join(main_path, 'output.zip')
    arquivozip = ZipFile(nome_zip, 'w', compression=ZIP_DEFLATED)

    for nome in nomes_arquivo:
        print(f'{nome} compactado em {nome_zip}')
        arquivozip.write(os.path.join(output_path, nome), nome)
    arquivozip.close()
    print('Arquivos compactados!')


def buscar_links(list):
    # fazendo uma requisição a url para que possa retornar o html da pagina e tratando o mesmo para a possibilidade de busca com o xpath
    res = requests.get(
        'https://www.gov.br/ans/pt-br/assuntos/consumidor/o-que-o-seu-plano-de-saude-deve-cobrir-1/o-que-e-o-rol-de-procedimentos-e-evento-em-saude')
    if res.status_code == requests.codes.OK:
        soup = BeautifulSoup(res.text, 'lxml')
        dom = etree.HTML(str(soup))

        print('Fazendo download do arquivos...')
        for i in range(len(list)):
            # iterando a lista de texto e fazendo a busca. extraindo o href do elemento resultante
            name = download_list[i]
            # buscando com xpath o elemento que contem EXATAMENTE o mesmo texto iterado
            url = dom.xpath(f'//*[text()="{list[i]}"]')[0].get('href')
            format = url.split(".")[-1]
            # com a url final do arquivo, é passada para a função de download
            download(url, name, format)
        print('Todos os arquivos foram baixados!')
        compactar_output()
    else:
        res.raise_for_status()


# definido o texto que os elementos que vão ser buscados contém
download_list = ['Anexo I - Lista completa de procedimentos (.pdf)',
                 'Anexo I - Lista completa de procedimentos (.xlsx)',
                 'Anexo II - Diretrizes de utilização (.pdf)',
                 'Anexo III - Diretrizes clínicas (.pdf)',
                 'Anexo IV - Protocolo de utilização (.pdf)'
                 ]


buscar_links(download_list)
