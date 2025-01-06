import xml.etree.ElementTree as ET
import os
import pandas as pd

# Pasta onde estão os XMLs
pastaDocs = 'docs'

# Listar os arquivos da pasta
arquivos = os.listdir(pastaDocs)

# Tags específicas a serem extraídas
tags_especificas = ["CPF", "CNPJ", "xNome", "xLgr", "nro", "CEP", "IE"]

# Namespace utilizado no XML
namespace = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

# Lista para armazenar os dados
dados = []

for doc in arquivos:
    caminho = os.path.join(pastaDocs, doc) #Concatena a pasta com o nome do arquivo
    tree = ET.parse(caminho) # Utiliza o nome do arquivo para carregar o arquivo
    root = tree.getroot() # Obtém o elemento raiz do XML

    # Procurar a tag <dest> dentro do namespace
    dest = root.find(".//nfe:dest", namespace)
    if dest is not None:
        linha = {}
        # Acessar as informações de endereços dentro de <enderDest>
        enderDest = dest.find("nfe:enderDest", namespace)

        # Buscar as tags dentro de <dest> e <enderDest>
        for tag in tags_especificas:
            # Definir o elemento de acordo com a tag
            if tag in ["xLgr", "nro", "CEP"]:
                elemento = enderDest.find(f"nfe:{tag}", namespace) if enderDest is not None else None
            else:
                elemento = dest.find(f"nfe:{tag}", namespace)
            
            #Verifica se a tag foi encontrada. Se sim, retorna o valor de texto e grava na base dados, senão, grava o valor nulo
            linha[tag] = elemento.text if elemento is not None else None
        dados.append(linha)

# Criar o DataFrame
df = pd.DataFrame(dados)

# Salvar em uma planilha Excel
df.to_excel("informacoesDestinatario.xlsx", index=False)
print("Planilha gerada com sucesso!")
