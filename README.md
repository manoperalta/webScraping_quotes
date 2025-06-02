# Raspador de Citações - Quotes to Scrape

Este projeto realiza a raspagem de dados do site (http://quotes
.toscrape.com), coletando citações, autores e tags. Ele permite buscas específicas, exporta os resultados em CSV e JSON, e tira screenshots das páginas, inicialmente no scanPage, somente a primeira páginas.

## Requisitos

- Python 3.7 ou superior
- Google Chrome + ChromeDriver compatível
- Bibliotecas Python:

## bash
pip install requests beautifulsoup4 selenium pandas

## Funcionalidades Principais

### scanPage(link_inicial, max_paginas=10)

Varre diversas páginas do site e extrai todas as citações, autores e tags.

- link_inicial: URL inicial da raspagem (ex: http://quotes.toscrape.com).
- max_paginas: número máximo de páginas a percorrer.

Salva:
- resultados/resultado_scan_<alvo>_<timestamp>.csv
- resultados/resultado_scan_<alvo>_<timestamp>.json
- Screenshot da 1ª página: screenshot/screenshot_<timestamp>.png

### findAutor(link, autor_busca)

Filtra citações de um autor específico na página inicial.

- link: URL da página a ser analisada.
- autor_busca: nome do autor (ex: "Albert Einstein").

Salva:
- resultados/resultado_<autor>_<timestamp>.csv
- resultados/resultado_<autor>_<timestamp>.json
- Screenshot da página: screenshot/screenshot_<timestamp>.png

### findTags(link, tag_busca)

Busca citações que contenham uma determinada tag.

- link: URL da página.
- tag_busca: nome da tag (ex: "humor").

Salva:
- resultados/resultado_tag_<tag>_<timestamp>.csv
- resultados/resultado_tag_<tag>_<timestamp>.json
- Screenshot da página: screenshot/screenshot_<timestamp>.png

### screenShot(link, data_inicio=None)

Tira uma captura de tela da página informada usando navegador headless.

- link: URL da página.
- data_inicio: (opcional) timestamp para nome do arquivo.

Salva:
- screenshot/screenshot_<timestamp>.png

## Exemplo de Uso

As funções abaixo são chamadas automaticamente no final do script:

```python
scanPage("http://quotes.toscrape.com", max_paginas=10)
findAutor("http://quotes.toscrape.com/", autor_busca="Albert Einstein")
findTags("http://quotes.toscrape.com/", tag_busca="humor")
```

## Aviso

Este projeto tem fins educacionais. Alguns sites utilizam o arquivo robots.txt do site para determinar os termos e regras de uso.

## Colaborador

- Jonathas M. Peralta.
- @devser_mano.