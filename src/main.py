import argparse
import sqlite3
import pandas as pd
import requests
import matplotlib.pyplot as plt
import os

# Caminho absoluto para a raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Caminho para os arquivos
DB_PATH = os.path.join(BASE_DIR, "database.db")
DICT_PATH = os.path.join(BASE_DIR, "dict.csv")
GRAPH_DIR = os.path.join(BASE_DIR, "graphs")

# Criar diretório para gráficos, se não existir
if not os.path.exists(GRAPH_DIR):
    os.makedirs(GRAPH_DIR)

def load_dictionary():
    """Carrega o dicionário de territórios do arquivo dict.csv."""
    return pd.read_csv(DICT_PATH)

def get_territory_name(territory_id, df_dict):
    """Obtém o nome do território a partir do ID usando o dict.csv."""
    row = df_dict[df_dict['id'] == int(territory_id)]
    return row['nome'].iloc[0] if not row.empty else f"Territorio{territory_id}"

def get_territory_id(territory_name, df_dict):
    """Obtém o ID do território a partir do nome usando o dict.csv."""
    row = df_dict[df_dict['nome'].str.lower() == territory_name.lower()]
    return row['id'].iloc[0] if not row.empty else None

def get_dimension_from_db(territory_id):
    """Consulta a dimensão de um território no banco de dados."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT dimensao FROM territorios WHERE id = ?", (territory_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except sqlite3.OperationalError:
        # Se a tabela 'territorios' não existir, retorna None
        return None
    
def get_dimension_from_api(territory_id):
    """Consulta a dimensão de um território na API do IBGE."""
    url = f"https://servicodados.ibge.gov.br/api/v3/malhas/estados/{territory_id}/metadados"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # A resposta da API é uma lista; acessar o primeiro elemento
            if isinstance(data, list) and data:
                metadata = data[0]
                # A área está no campo 'area' -> 'dimensao'
                area_data = metadata.get('area', {})
                dimension = area_data.get('dimensao', 0)
                if dimension == 0:
                    raise ValueError(f"Campo 'area/dimensao' não encontrado na resposta da API para id {territory_id}")
                return dimension
            else:
                raise ValueError(f"Resposta da API não contém dados válidos para id {territory_id}")
        elif response.status_code == 400:
            raise ValueError(f"ID {territory_id} não é válido para a API do IBGE (erro 400)")
        else:
            raise ValueError(f"Erro na requisição à API: status code {response.status_code} para id {territory_id}")
    except requests.RequestException as e:
        raise ValueError(f"Falha na conexão com a API: {str(e)}")
def get_dimension(territory_input, df_dict):
    """Obtém a dimensão de um território, consultando banco ou API."""
    # Verificar se o input é um ID (numérico) ou nome
    try:
        territory_id = int(territory_input)
        # Validar se o ID existe no dict.csv
        if territory_id not in df_dict['id'].values:
            raise ValueError(f"ID {territory_id} não encontrado no dict.csv")
    except ValueError as e:
        if str(e).startswith("ID"):
            raise
        territory_id = get_territory_id(territory_input, df_dict)
        if territory_id is None:
            raise ValueError(f"Território '{territory_input}' não encontrado no dict.csv")

    # Consultar no banco
    dimension = get_dimension_from_db(territory_id)
    if dimension is None:
        # Se não encontrado, consultar na API
        dimension = get_dimension_from_api(territory_id)
    if dimension is None:
        raise ValueError(f"Não foi possível obter a dimensão do território {territory_id}")
    return territory_id, dimension

def generate_single_graph(territory_name, dimension, graph_path):
    """Gera um gráfico de colunas para um único território."""
    plt.figure(figsize=(6, 4))
    plt.bar(territory_name, float(dimension), color='blue', width=0.4)
    plt.title(f"Dimensão de {territory_name}")
    plt.ylabel("Dimensão (km²)")
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    # Adicionar rótulo de valor acima da barra
    plt.text(territory_name, float(dimension), f"{float(dimension):.2f}", ha='center', va='bottom')
    # Ajustar o limite do eixo Y
    plt.ylim(0, float(dimension) * 1.1)  # 10% a mais para dar espaço ao rótulo
    plt.savefig(graph_path)
    plt.close()

def generate_comparison_graph(territory1_name, dimension1, territory2_name, dimension2, difference, graph_path):
    """Gera um gráfico de colunas comparando dois territórios e a diferença."""
    plt.figure(figsize=(8, 4))
    bars = plt.bar([territory1_name, territory2_name, "Diferença"], [float(dimension1), float(dimension2), float(difference)],
                   color=['blue', 'green', 'red'], width=0.4)
    plt.title(f"Comparação entre {territory1_name} e {territory2_name}")
    plt.ylabel("Dimensão (km²)")
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    # Adicionar rótulos de valor acima das barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height, f"{height:.2f}", ha='center', va='bottom')
    # Ajustar o limite do eixo Y
    max_height = max(float(dimension1), float(dimension2), float(difference))
    plt.ylim(0, max_height * 1.1)
    plt.savefig(graph_path)
    plt.close()

def dimensao_command(territory_input):
    """Comando para consultar a dimensão de um território."""
    df_dict = load_dictionary()
    territory_id, dimension = get_dimension(territory_input, df_dict)
    territory_name = get_territory_name(territory_id, df_dict)

    # Gerar gráfico
    graph_path = os.path.join(GRAPH_DIR, f"dimensao_{territory_id}.png")
    generate_single_graph(territory_name, dimension, graph_path)

    # Exibir resultado no formato especificado
    print(">>> Nome:", f"{{{territory_name}}}")
    print(">>> Dimensão:", f"{{{dimension}}}km2")
    print(">>> Gráfico:", f"{{{graph_path}}}")

def comparar_command(territory1_input, territory2_input):
    """Comando para comparar as dimensões de dois territórios."""
    df_dict = load_dictionary()

    # Obter dimensões dos dois territórios
    territory1_id, dimension1 = get_dimension(territory1_input, df_dict)
    territory2_id, dimension2 = get_dimension(territory2_input, df_dict)

    territory1_name = get_territory_name(territory1_id, df_dict)
    territory2_name = get_territory_name(territory2_id, df_dict)
    difference = abs(float(dimension1) - float(dimension2))

    # Gerar gráfico
    graph_path = os.path.join(GRAPH_DIR, f"comparacao_{territory1_id}_{territory2_id}.png")
    generate_comparison_graph(territory1_name, dimension1, territory2_name, dimension2, difference, graph_path)

    # Exibir resultado no formato especificado
    print(">>>", f"{{{territory1_name}}}:", f"{{{dimension1}}}km2")
    print(">>>", f"{{{territory2_name}}}:", f"{{{dimension2}}}km2")
    print(">>> Diferença:", f"{{{difference}}}km2")
    print(">>> Gráfico:", f"{{{graph_path}}}")

def main():
    """Função principal para a CLI."""
    parser = argparse.ArgumentParser(description="CLI para análise de dimensões de territórios brasileiros.")
    subparsers = parser.add_subparsers(dest="command")

    # Comando 'dimensao'
    parser_dimensao = subparsers.add_parser("dimensao", help="Consulta a dimensão de um território")
    parser_dimensao.add_argument("territory", help="ID ou nome do território")

    # Comando 'comparar'
    parser_comparar = subparsers.add_parser("comparar", help="Compara as dimensões de dois territórios")
    parser_comparar.add_argument("territory1", help="ID ou nome do primeiro território")
    parser_comparar.add_argument("territory2", help="ID ou nome do segundo território")

    args = parser.parse_args()

    if args.command == "dimensao":
        dimensao_command(args.territory)
    elif args.command == "comparar":
        comparar_command(args.territory1, args.territory2)

if __name__ == "__main__":
    main()
