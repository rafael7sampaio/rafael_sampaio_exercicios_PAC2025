import re
from datetime import datetime

# Exercicio 1: Ler o ficheiro
with open("dados.txt", "r", encoding="utf-8") as ficheiro:
    conteudo_dados = ficheiro.read()

print("Exercício 1: Ler o ficheiro")
print(conteudo_dados)
print()

# Exercicio 2: Encontrar todos os emails
emails = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", conteudo_dados)
print("Exercício 2: Encontrar todos os emails")
for email in emails:
    print(email)
print()

# Exercicio 3: Encontrar todos os números de telemóvel
telemoveis = re.findall(r"\b\d{9}\b|\b\d{3}-\d{3}-\d{3}\b|\b\d{3} \d{3} \d{3}\b", conteudo_dados)
print("Exercício 3: Encontrar todos os números de telemóvel")
for telemovel in telemoveis:
    print(telemovel)
print()

# Exercicio 4: Extrair apenas os nomes
nomes = re.findall(r"Nome:\s*([^,\n]+)", conteudo_dados)
print("Exercício 4: Extrair apenas os nomes")
for nome in nomes:
    print(nome)
print()

# Exercicio 5: Guardar os dados extraídos num novo ficheiro
registos_extraidos = re.findall(r"Nome:\s*([^,\n]+),\s*Email:\s*([\w\.-]+@[\w\.-]+\.\w+),\s*Telemóvel:\s*(\d{9}|\d{3}-\d{3}-\d{3}|\d{3} \d{3} \d{3})", conteudo_dados)

with open("extraidos.txt", "w", encoding="utf-8") as ficheiro:
    for nome, email, telemovel in registos_extraidos:
        ficheiro.write(f"{nome} | {email} | {telemovel}\n")

print("Exercício 5: Guardar os dados extraídos num novo ficheiro")
print("Ficheiro extraidos.txt criado com sucesso")
print()

# Exercicio 6: Validar emails que terminam em .pt
emails_pt = re.findall(r"[\w\.-]+@[\w\.-]+\.pt\b", conteudo_dados)
print("Exercício 6: Validar emails que terminam em .pt")
for email in emails_pt:
    print(email)
print()

# Ler o ficheiro registos.txt
with open("registos.txt", "r", encoding="utf-8") as ficheiro:
    conteudo_registos = ficheiro.read()

# Exercicio 7: Extrair todos os NIFs (9 dígitos)
nifs = re.findall(r"\b\d{9}\b", conteudo_registos)
print("Exercício 7: Extrair todos os NIFs (9 dígitos)")
for nif in nifs:
    print(nif)
print()

# Exercicio 8: Extrair datas no formato DD/MM/AAAA
datas = re.findall(r"\b\d{2}/\d{2}/\d{4}\b", conteudo_registos)
print("Exercício 8: Extrair datas no formato DD/MM/AAAA")
for data in datas:
    print(data)
print()

# Exercicio 9: Extrair códigos postais portugueses (1234-567)
codigos_postais = re.findall(r"\b\d{4}-\d{3}\b", conteudo_registos)
print("Exercício 9: Extrair códigos postais portugueses (1234-567)")
for codigo in codigos_postais:
    print(codigo)
print()

# Exercicio 10: Extrair apenas os domínios dos sites
dominios = re.findall(r"https?://([^\s|/]+)", conteudo_registos)
print("Exercício 10: Extrair apenas os domínios dos sites")
for dominio in dominios:
    print(dominio)
print()

# Exercicio 11: Validar se todos os NIFs começam com um dígito válido
print("Exercício 11: Validar se todos os NIFs começam com um dígito válido")
for nif in nifs:
    if re.match(r"^[123568]\d{8}$", nif):
        print(f"{nif} -> NIF válido")
    else:
        print(f"{nif} -> NIF inválido")
print()

# Exercicio 12: Criar um ficheiro resumo.txt com os dados organizados
registos_completos = re.findall(
    r"Nome:\s*([^|\n]+)\s*\|\s*NIF:\s*(\d{9})\s*\|\s*Data:\s*(\d{2}/\d{2}/\d{4})\s*\|\s*Código Postal:\s*(\d{4}-\d{3})\s*\|\s*Site:\s*https?://([^\s|/]+)",
    conteudo_registos
)

with open("resumo.txt", "w", encoding="utf-8") as ficheiro:
    for nome, nif, data, codigo_postal, dominio in registos_completos:
        ficheiro.write(f"{nome.strip()} | {nif} | {data} | {codigo_postal} | {dominio}\n")

print("Exercício 12: Criar um ficheiro resumo.txt com os dados organizados")
print("Ficheiro resumo.txt criado com sucesso")
print()

# Exercicio 13: Encontrar registos com datas anteriores a 2025
print("Exercício 13: Encontrar registos com datas anteriores a 2025")
for nome, nif, data, codigo_postal, dominio in registos_completos:
    data_obj = datetime.strptime(data, "%d/%m/%Y")
    if data_obj.year < 2025:
        print(f"{nome.strip()} | {nif} | {data} | {codigo_postal} | {dominio}")
