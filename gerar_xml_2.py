import os
import re
from xml.etree import ElementTree as ET
from datetime import datetime
import random

# Dados fixos do prestador
PRESTADOR = {
    "cnpj": "xxxxxxxxxxxxx", #inclua o CNPJ
    "inscricaoMunicipal": "xxxxxx",
    "razaoSocial": "xxxxxx Comercio LTDA",
    "logradouro": "Rua da Bahia",
    "numero": "4",
    "bairro": "Centro",
    "codigoMunicipio": "3138203",
    "uf": "MG",
    "cep": "37200000", #CEP do municipio, nesse caso, Lavras/MG
    "telefone": "(35) 3xxx 0000",
    "email": "xxxx@exemplo.com"
}

def limpar_valor(valor_str):
    return float(valor_str.replace(',', '.').replace(' ', ''))

def gerar_correlacao_unica():
    agora = datetime.now().strftime("%Y%m%d")  # Últimos dígitos da data
    aleatorio = str(random.randint(100000, 999999))
    return agora[-6:] + aleatorio[:2]  # 8 dígitos total

def extrair_vendas(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='latin-1') as f:
        linhas = f.readlines()

    vendas = []
    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue

        cpf_match = re.match(r'^(\d{11})\s+REQUISICAO', linha)
        if cpf_match:
            cpf = cpf_match.group(1)
            partes = linha.split()
            correlacao = partes[3] if len(partes) > 3 and partes[3].isdigit() else gerar_correlacao_unica()
            valor_match = re.search(r'(\d+,\d+)$', linha)
            if valor_match:
                valor = limpar_valor(valor_match.group(1))
                vendas.append({
                    "cpf": cpf,
                    "valor": valor,
                    "correlacao": correlacao
                })
    return vendas

def agrupar_por_cliente(vendas):
    clientes = {}
    for venda in vendas:
        cpf = venda["cpf"]
        if cpf not in clientes:
            clientes[cpf] = []
        clientes[cpf].append(venda)
    return clientes

def gerar_xml(cliente, vendas):
    root = ET.Element("GovDigital", attrib={
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi:noNamespaceSchemaLocation": "govdigital.xsd"
    })

    emissao = ET.SubElement(root, "emissao")
    nfe = ET.SubElement(emissao, "nf-e")

    numero_rps = vendas[0].get("correlacao", None) or gerar_correlacao_unica()
    ET.SubElement(nfe, "correlacao").text = numero_rps
    ET.SubElement(nfe, "prestacao").text = datetime.now().strftime("%Y-%m-%d")
    ET.SubElement(nfe, "exigibilidade").text = "1"
    ET.SubElement(nfe, "retido").text = "2"
    ET.SubElement(nfe, "municipioIncidencia").text = PRESTADOR["codigoMunicipio"]
    ET.SubElement(nfe, "atividade").text = "4.07"
    ET.SubElement(nfe, "ctiss").text = ""

    tomador = ET.SubElement(nfe, "tomador")
    ET.SubElement(tomador, "documento").text = cliente
    ET.SubElement(tomador, "nome").text = "Cliente Final"
    ET.SubElement(tomador, "cep").text = "37200000"
    ET.SubElement(tomador, "logradouro").text = "Rua Cliente"
    ET.SubElement(tomador, "numero").text = "S/N"
    ET.SubElement(tomador, "complemento").text = "-"
    ET.SubElement(tomador, "bairro").text = "Jardim Residencial"
    ET.SubElement(tomador, "estado").text = "MG"
    ET.SubElement(tomador, "municipio").text = "LAVRAS"
    ET.SubElement(tomador, "pais").text = "BRASIL"
    ET.SubElement(tomador, "telefone").text = "(35) 99999-9999"
    ET.SubElement(tomador, "email").text = "cliente@example.com"

    itens = ET.SubElement(nfe, "itens")
    for idx, venda in enumerate(vendas):
        item = ET.SubElement(itens, "item")
        numero_requisicao = venda.get("correlacao", "XXXXX")
        descricao_item = f"Fórmula Manipulada Requisição Núm: {numero_requisicao}"
        ET.SubElement(item, "descricao").text = descricao_item
        ET.SubElement(item, "valor").text = f"{venda['valor']:.2f}"

    ET.SubElement(nfe, "obs").text = "Nota fiscal eletrônica gerada automaticamente para REQUISICAO."
    deducoes = ET.SubElement(nfe, "deducoes")
    ET.SubElement(deducoes, "deducao", {"codigo": "DESCONTO INCONDICIONAL"}).text = "0.00"

    tree = ET.ElementTree(root)
    filename = f"./xmls/nf_e_requisicao_{cliente}.xml"
    tree.write(filename, encoding="utf-8", xml_declaration=True)
    print(f"✅ Arquivo gerado: {filename}")

if __name__ == "__main__":
    os.makedirs("./xmls", exist_ok=True)

    caminho_arquivo = "Fórmula-Certa - Movimentação de Caixa-0506.TXT"
    vendas = extrair_vendas(caminho_arquivo)
    clientes_agrupados = agrupar_por_cliente(vendas)

    for cliente, dados in clientes_agrupados.items():
        gerar_xml(cliente, dados)