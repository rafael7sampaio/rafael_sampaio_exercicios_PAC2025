
# LAB 2 - Web Crawler Ético - Rafael Sampaio | 2025157604

## Descrição

Este projeto implementa um web crawler educativo em Python que navega por páginas web, extrai informações relevantes e respeita boas práticas éticas de crawling.

## Funcionalidades

- Aceder a uma página inicial e visitar até N páginas
- Extração de:
  - Título da página
  - Todos os links (`<a href="">`)
  - Cabeçalhos (`<h1>`, `<h2>`) *(bónus)*
  - Parágrafos (`<p>`) *(bónus)*
- Evita visitar a mesma página duas vezes
- Respeita o ficheiro `robots.txt` do site
- Delay de 1 segundo entre pedidos (não sobrecarrega o servidor)
- Identifica-se com um `User-Agent` próprio
- Guarda os resultados em ficheiros `.json`
- Filtro opcional de links para o mesmo domínio *(bónus)*
- Grafo de navegação entre páginas *(bónus)*

## Estrutura do projeto

```bash
Lab02_Rafael/
│
├── crawler.py
├── results/
│   ├── resultados.json       (gerado ao executar)
│   └── grafo_navegacao.json  (gerado ao executar)
├── .gitignore
└── README.md
```

## Requisitos

- Python 3.10 ou superior
- Bibliotecas externas:

```bash
pip install requests beautifulsoup4
```

## Como executar

```bash
python crawler.py
```

Por defeito, o crawler acede a `https://example.com` e visita até 5 páginas.

Para configurar outro ponto de partida, editar as variáveis no bloco `if __name__ == "__main__"`:

```python
url_inicial = "https://example.com"
max_paginas = 5
```

## Exemplo de saída JSON (`results/resultados.json`)

```json
[
  {
    "url": "https://example.com",
    "titulo": "Example Domain",
    "links": [
      "https://www.iana.org/domains/example"
    ],
    "headings": [
      "Example Domain"
    ],
    "paragraphs": [
      "This domain is for use in illustrative examples..."
    ]
  }
]
```

## Perguntas de reflexão

### Porque é importante respeitar o robots.txt?

O `robots.txt` é um ficheiro que os sites usam para indicar quais partes não devem ser acedidas por crawlers automáticos. Respeitar este ficheiro é importante por razões éticas e legais: ignora-lo pode violar os termos de serviço do site, causar problemas legais, e sobrecarregar servidores com pedidos não autorizados.

### O que pode acontecer se um crawler for mal implementado?

Um crawler mal implementado pode sobrecarregar servidores com demasiados pedidos em pouco tempo (semelhante a um ataque DoS), ser bloqueado pelo servidor, causar problemas legais por aceder a conteúdo proibido, e recolher dados pessoais de forma não autorizada.

### Qual a diferença entre crawling e scraping?

**Crawling** é o processo de navegar sistematicamente por páginas web, seguindo links para descobrir e indexar páginas (como fazem os motores de busca).

**Scraping** é o processo de extrair dados específicos de páginas web já acedidas — o foco é nos dados, não na navegação.

Os dois processos são frequentemente usados em conjunto: primeiro faz-se crawling para descobrir páginas, depois scraping para extrair a informação desejada.
