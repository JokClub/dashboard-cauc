# Dashboard CAUC — Maranhão

Painel web (HTML único offline) que processa o arquivo CSV exportado pelo CAUC da STN
e apresenta os indicadores de regularidade fiscal dos órgãos/entidades do Ente Federativo.

## Snapshot embutido (09/09/2026)

- 27 órgãos monitorados
- 26 com pendências (96,3% do total)
- 42 pendências distribuídas em 7 códigos CAUC
- 1 secretaria da Administração Direta com pendência:
  ESTADO DO MARANHAO - SECRETARIA DE ESTADO DO DESENVOLVIMENTO SOCIAL
  CNPJ 02.940.097/0001-48 — códigos 1.5 e 2.1.1

## Arquivos do pacote

| Arquivo | Tamanho | Função |
|---|---|---|
| `index.html` | ~1,12 MB | Dashboard pronto, com dados embutidos. Use no GitHub Pages. |
| `dashboard_auto_update.html` | ~58 KB | Editor local: abra, arraste o CSV e clique em 🚀 Publicar. |
| `build_auto_update.py` | ~9 KB | Pipeline CLI: `python3 build_auto_update.py caminho.csv`. |
| `dados-cauc.csv` | ~7 KB | Snapshot do CSV usado para gerar o `index.html`. |

## Como publicar no GitHub Pages

1. Crie um repositório público (sugestão: `dashboard-cauc`).
2. Suba apenas o `index.html` e o `dados-cauc.csv` na raiz do repositório.
3. Settings → Pages → Source: `main` / `(root)`.
4. Aguarde 1–2 minutos. O painel estará em
   `https://SEU-USUARIO.github.io/dashboard-cauc/`.

## Atualização diária (manual via web)

1. Baixe o CSV novo no portal do CAUC (≈1 min).
2. Abra `dashboard_auto_update.html` no navegador.
3. Arraste o CSV na barra de upload (5 s).
4. Clique em 🚀 Publicar atualização (5 s).
5. Salve o `index.html` gerado (substituirá o anterior).
6. Suba o novo `index.html` no GitHub (30 s).

Total: ≈3 min. Sem token, sem terminal.

## Layout responsivo (corrigido nesta versão)

- Grid do dashboard usa `minmax(0, …)` — sem overflow horizontal.
- Box-sizing global em `border-box`.
- Listas de códigos com scroll vertical próprio (max-height 260 px).
- Quadro "Secretarias DIRETAS" filtra apenas órgãos cujo nome
  contém "SECRETARIA" e exclui ente raiz e unidades operacionais
  (Batalhão, Unidade Mista, Companhia, …).

## Pré-requisitos

- Python 3.8+ (apenas para o pipeline CLI).
- Navegador moderno (Chrome, Edge, Firefox, Safari) para abrir o HTML.
