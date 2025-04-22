# TesteScientificCloud

Este projeto foi desenvolvido como parte do **case técnico para a vaga de estágio na ScientificCloud**.

Ele consiste em uma ferramenta **CLI (Command Line Interface)** para análise das dimensões de territórios brasileiros, com suporte para consultar e comparar dimensões de territórios.

---

## ⚙️ Funcionalidades

- **Comando `dimensao`**  
  Consulta a dimensão de um território (por ID ou nome), exibindo:
  - Nome do território
  - Dimensão
  - Caminho para o gráfico gerado  

  **Exemplo:**  
  ```bash
  python src/main.py dimensao 35

Comando comparar
Compara as dimensões de dois territórios (por ID ou nome), exibindo:

Dimensões individuais

Diferença

Caminho para o gráfico gerado

Exemplo:
python src/main.py comparar 35 33

🗂️ Fonte de Dados
Os dados são consultados primeiro no banco de dados (database.db).

Caso o dado não esteja presente, a API do IBGE é consultada automaticamente.

Os gráficos de colunas são gerados e salvos no diretório graphs/.

Suporte a entrada por ID ou nome do território (ex: dimensao 35 ou dimensao "São Paulo").

✅ Requisitos
Python 3.6 ou superior (testado com Python 3.10)

Dependências listadas em requirements.txt

🚀 Instalação
Clone o repositório:
git clone <link-do-repositorio>
cd TesteScientificCloud

Crie um ambiente virtual:
python -m venv teste_env

Ative o ambiente virtual:

Windows (PowerShell):
.\teste_env\Scripts\activate

Linux/Mac ou Git Bash:
source teste_env/bin/activate

Instale as dependências:
pip install -r requirements.txt

Execute os comandos da CLI:
python src/main.py dimensao 35
python src/main.py comparar 35 33

📁 Estrutura do Projeto
TesteScientificCloud/
│
├── database.db        # Banco de dados SQLite (não incluído no Git)
├── dict.csv           # Dicionário com IDs e nomes dos territórios
├── graphs/            # Gráficos gerados (.png)
├── requirements.txt   # Dependências do projeto
└── src/
    ├── main.py        # Script principal da CLI
    └── teste.py       # Script para testar a API do IBGE

ℹ️ Notas
É necessário ter conexão com a internet para a funcionalidade de fallback da API do IBGE.

O arquivo database.db não deve ser alterado e não está incluído no Git, conforme solicitado no enunciado.

💡 Exemplo de Uso
Consultar a dimensão de São Paulo:
python src/main.py dimensao 35

Saída esperada:
Nome: São Paulo
Dimensão: 248219.5 km²
Gráfico: graphs/dimensao_35.png

Comparar São Paulo e Rio de Janeiro:
python src/main.py comparar 35 33

Saída esperada:
São Paulo: 248219.5 km²
Rio de Janeiro: 43696.1 km²
Diferença: 204523.4 km²
Gráfico: graphs/comparacao_35_33.png

👨‍💻 Autor
Cristiano Silveira
