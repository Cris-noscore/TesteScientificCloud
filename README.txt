TesteCientifiCloud

Este projeto foi desenvolvido como parte do case técnico para a vaga de estágio na ScientificCloud. Ele consiste em uma ferramenta CLI (Command Line Interface) para análise das dimensões de territórios brasileiros, com suporte para consultar a dimensão de um território e comparar as dimensões de dois territórios.

Funcionalidades

Comando dimensao: Consulta a dimensão de um território (por ID ou nome), exibe o nome, a dimensão e o caminho para o gráfico gerado.

Exemplo: python src/main.py dimensao 35 (consulta a dimensão de São Paulo).

Comando comparar: Compara as dimensões de dois territórios (por ID ou nome), exibe as dimensões, a diferença e o caminho para o gráfico gerado.

Exemplo: python src/main.py comparar 35 33 (compara São Paulo e Rio de Janeiro).


Dados são consultados primeiro no banco de dados database.db. Se não houver dados, a API do IBGE é consultada.

Gráficos de colunas são gerados e salvos no diretório graphs/.

Suporte para entrada por ID ou nome do território (ex.: dimensao 35 ou dimensao "São Paulo").

Requisitos

Python 3.6 ou superior (testado com Python 3.10).

Dependências listadas em requirements.txt.

Instalação

Clone o repositório:

git clone <link-do-repositorio>
cd testecientificcloud

Crie um ambiente virtual e ative-o:

python -m venv teste_env

No Windows (PowerShell):

.\teste_env\Scripts\activate

No Linux/Mac ou Git Bash:

source teste_env/bin/activate


Instale as dependências:

pip install -r requirements.txt

Execute os comandos da CLI, por exemplo:

python src/main.py dimensao 35
python src/main.py comparar 35 33

Estrutura do Projeto

src/: Contém os scripts principais do projeto.

main.py: Script principal da CLI.

teste.py: Script para testar a API do IBGE.

graphs/: Diretório onde os gráficos gerados são salvos.

database.db: Banco de dados SQLite (não incluído no Git).

dict.csv: Dicionário com IDs e nomes dos territórios.

requirements.txt: Lista de dependências do projeto.

Notas

O arquivo database.db não está incluído no controle de versão (conforme exigido pelo case técnico). O programa não altera o banco de dados durante a execução.

Certifique-se de ter conexão com a internet para consultar a API do IBGE, caso os dados não estejam no banco.

Exemplo de Uso

Consultar a dimensão de São Paulo:

python src/main.py dimensao 35

Saída esperada:

>>> Nome: {São Paulo}
>>> Dimensão: {248219.5}km2
>>> Gráfico: {graphs\dimensao_35.png}

Comparar São Paulo e Rio de Janeiro:

python src/main.py comparar 35 33

Saída esperada:

>>> {São Paulo}: {248219.5}km2
>>> {Rio de Janeiro}: {43696.1}km2
>>> Diferença: {204523.4}km2
>>> Gráfico: {graphs\comparacao_35_33.png}

Autor
Cristiano Silveira