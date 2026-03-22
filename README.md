# gerador-xml-nfs-ia
# Gerador de xml para NFS-e no município de Lavras/MG

> Sistema para geração automática de Nota Fiscal de Serviço Eletrônica (NFS-e) e recibos com base em arquivos `.txt`, seguindo o schema XSD do município de **Lavras - MG**.

Este projeto permite:
- Ler dados de um arquivo `.txt` com informações do serviço prestado;
- Validar os dados conforme as regras do município;
- Gerar o **XML da NFS-e** compatível com o portal [NF-e Cidades](https://www.nfse-cidades.com.br);
- Gerar um **recibo de prestação de serviço** (em PDF ou HTML).

Ideal para autônomos, pequenas empresas e contadores que desejam automatizar a emissão de notas fiscais.

---

## 📥 Entrada: Arquivo TXT

O programa lê um arquivo `.txt` com os seguintes campos (um por linha):
CNPJ Prestador
Inscrição Municipal Prestador
Razão Social Prestador
Endereço Prestador
CNPJ Tomador
CPF/CNPJ Tomador (se for pessoa física, usar CPF)
Nome/Razão Social Tomador
Endereço Tomador
Email Tomador
Descrição do Serviço
Valor do Serviço (ex: 150.00)
ISS Retido (Sim/Não)
Código do Serviço (ex: 11.01)


👉 Veja exemplo em `data/entrada_exemplo.txt`.

---

## 🧾 Saída: Arquivos Gerados

1. **XML da NFS-e**: Salvo em `output/nfses/`, pronto para envio ao portal.
2. **Recibo em PDF/HTML**: Salvo em `output/recibos/`, para entrega ao cliente.

---

## ⚙️ Tecnologias Utilizadas

- Python 3.8+
- `lxml` para geração e validação XML
- `weasyprint` ou `reportlab` para PDF (opcional)
- Validação com XSD oficial de Lavras/MG

---

## 🛠 Como Usar

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/nfs-lavras-mg.git
cd nfs-lavras-mg
