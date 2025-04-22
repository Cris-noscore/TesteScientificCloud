import requests

# URL base da API
url_base = "https://servicodados.ibge.gov.br/api/v3/malhas/estados/{}/metadados"

# Faixa de IDs a testar (de 11 a 53)
ids_testar = range(11, 54)

# Resultados
ids_ok = []
ids_erro = []

print("Testando estados...\n")

for id_estado in ids_testar:
    url = url_base.format(id_estado)
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"ID {id_estado}: ✅ OK")
            ids_ok.append(id_estado)
        else:
            print(f"ID {id_estado}: ❌ Erro {response.status_code}")
            ids_erro.append(id_estado)
    except requests.Timeout:
        print(f"ID {id_estado}: ❌ Timeout na requisição")
        ids_erro.append(id_estado)
    except requests.RequestException as e:
        print(f"ID {id_estado}: ❌ Exceção -> {e}")
        ids_erro.append(id_estado)

print("\n--- Resumo ---")
print(f"IDs OK ({len(ids_ok)}): {ids_ok}")
print(f"IDs com erro ({len(ids_erro)}): {ids_erro}")