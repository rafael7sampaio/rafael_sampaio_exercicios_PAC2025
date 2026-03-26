
import json
import re

with open("dados.json", "r", encoding="utf-8") as ficheiro:
    dados = json.load(ficheiro)

print("Exercicio 1 : Ler o ficheiro JSON")
print(dados)
print()

padrao_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
padrao_nif = r"^[123568]\d{8}$"

registos_validos = []

print("Exercicio 2 : Validar emails com regex")
for pessoa in dados:
    if re.match(padrao_email, pessoa["email"]):
        print(f'{pessoa["email"]} -> email válido')
    else:
        print(f'{pessoa["email"]} -> email inválido')
print()

print("Exercicio 3 : Extrair domínios dos sites")
for pessoa in dados:
    dominio = re.sub(r"^https?://(www\.)?", "", pessoa["site"])
    print(dominio)
print()

print("Exercicio 4 : Validar NIFs com regex")
for pessoa in dados:
    if re.match(padrao_nif, pessoa["nif"]):
        print(f'{pessoa["nif"]} -> NIF válido')
    else:
        print(f'{pessoa["nif"]} -> NIF inválido')
print()

print("Exercicio 5 : Guardar apenas os registos válidos num novo ficheiro JSON")
for pessoa in dados:
    email_valido = re.match(padrao_email, pessoa["email"])
    nif_valido = re.match(padrao_nif, pessoa["nif"])

    telemovel_limpo = re.sub(r"\D", "", pessoa["telemovel"])
    telemovel_valido = len(telemovel_limpo) == 9

    if email_valido and nif_valido and telemovel_valido:
        registos_validos.append(pessoa)

with open("registos_validos.json", "w", encoding="utf-8") as ficheiro:
    json.dump(registos_validos, ficheiro, ensure_ascii=False, indent=2)

print("Registos válidos guardados em registos_validos.json")
print(registos_validos)
print()

print("Exercicio 6 : Criar um ficheiro .txt com a keys nome e email")
with open("nomes_emails.txt", "w", encoding="utf-8") as ficheiro:
    for pessoa in dados:
        ficheiro.write(f'Nome: {pessoa["nome"]}\n')
        ficheiro.write(f'Email: {pessoa["email"]}\n')
        ficheiro.write("\n")

print("Ficheiro nomes_emails.txt criado com sucesso")
