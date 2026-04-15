# Exercícios Sort
# Rafael Sampaio | 2025157604


# -----------------------------------------------------------------------------
# Exercício 1: Ordenar lista de palavras por ordem alfabética (A -> Z)
# -----------------------------------------------------------------------------
def comparar_palavras(p1, p2):
    """Retorna -1 se p1 < p2, 1 se p1 > p2, 0 se iguais (comparação ASCII)."""
    i = 0
    while i < len(p1) and i < len(p2):
        if ord(p1[i]) < ord(p2[i]):
            return -1
        if ord(p1[i]) > ord(p2[i]):
            return 1
        i += 1
    # Prefixo: a mais curta vem primeiro
    if len(p1) < len(p2):
        return -1
    if len(p1) > len(p2):
        return 1
    return 0


def ordenar_alfabetica(lista):
    resultado = lista[:]
    n = len(resultado)
    for i in range(n):
        for j in range(0, n - i - 1):
            if comparar_palavras(resultado[j], resultado[j + 1]) > 0:
                resultado[j], resultado[j + 1] = resultado[j + 1], resultado[j]
    return resultado


# -----------------------------------------------------------------------------
# Exercício 2: Ordem alfabética inversa (Z -> A), ignorando maiúsculas
# -----------------------------------------------------------------------------
def comparar_ignore_case(p1, p2):
    a, b = p1.lower(), p2.lower()
    i = 0
    while i < len(a) and i < len(b):
        if ord(a[i]) < ord(b[i]):
            return -1
        if ord(a[i]) > ord(b[i]):
            return 1
        i += 1
    if len(a) < len(b):
        return -1
    if len(a) > len(b):
        return 1
    return 0


def ordenar_inversa_ignore_case(lista):
    resultado = lista[:]
    n = len(resultado)
    for i in range(n):
        for j in range(0, n - i - 1):
            # Inverter: maiores primeiro
            if comparar_ignore_case(resultado[j], resultado[j + 1]) < 0:
                resultado[j], resultado[j + 1] = resultado[j + 1], resultado[j]
    return resultado


# -----------------------------------------------------------------------------
# Exercício 3: Ordenar os caracteres de uma palavra por ordem alfabética
# -----------------------------------------------------------------------------
def ordenar_caracteres(palavra):
    chars = list(palavra)
    n = len(chars)
    for i in range(n):
        for j in range(0, n - i - 1):
            if ord(chars[j]) > ord(chars[j + 1]):
                chars[j], chars[j + 1] = chars[j + 1], chars[j]
    return "".join(chars)


# -----------------------------------------------------------------------------
# Exercício 4: Ordenar palavras pela quantidade de letras minúsculas
# -----------------------------------------------------------------------------
def contar_minusculas(palavra):
    total = 0
    for c in palavra:
        if 'a' <= c <= 'z':
            total += 1
    return total


def ordenar_por_minusculas(lista):
    resultado = lista[:]
    n = len(resultado)
    for i in range(n):
        for j in range(0, n - i - 1):
            if contar_minusculas(resultado[j]) > contar_minusculas(resultado[j + 1]):
                resultado[j], resultado[j + 1] = resultado[j + 1], resultado[j]
    return resultado


# -----------------------------------------------------------------------------
# Exercício 5: Agrupar pela letra inicial e ordenar cada grupo (A -> Z)
# -----------------------------------------------------------------------------
def agrupar_e_ordenar(lista):
    grupos = {}
    for palavra in lista:
        if not palavra:
            continue
        letra = palavra[0].lower()
        if letra not in grupos:
            grupos[letra] = []
        grupos[letra].append(palavra)

    for letra in grupos:
        grupos[letra] = ordenar_alfabetica(grupos[letra])

    return grupos


# -----------------------------------------------------------------------------
# Exercícios a funcionar:
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("Exercício 1 — Ordem alfabética (A -> Z):")
    e1 = ["banana", "uva", "abacaxi", "laranja"]
    print(f"  Entrada : {e1}")
    print(f"  Saída   : {ordenar_alfabetica(e1)}")
    print()

    print("Exercício 2 — Ordem alfabética inversa (Z -> A), ignore case:")
    e2 = ["Python", "inteligência", "Aprender", "dados", "Rede"]
    print(f"  Entrada : {e2}")
    print(f"  Saída   : {ordenar_inversa_ignore_case(e2)}")
    print()

    print("Exercício 3 — Ordenar caracteres de uma palavra:")
    e3 = "algoritmo"
    print(f"  Entrada : {e3!r}")
    print(f"  Saída   : {ordenar_caracteres(e3)!r}")
    print()

    print("Exercício 4 — Ordenar por quantidade de letras minúsculas:")
    e4 = ["PYthon", "banana", "CÓDIGO", "intELIGENTE", "dados"]
    print(f"  Entrada : {e4}")
    print(f"  Saída   : {ordenar_por_minusculas(e4)}")
    print()

    print("Exercício 5 — Agrupar pela letra inicial e ordenar cada grupo:")
    e5 = ["banana", "bola", "abacaxi", "arroz", "uva", "urso"]
    print(f"  Entrada : {e5}")
    print(f"  Saída   : {agrupar_e_ordenar(e5)}")
