# Dashboard CAUC — Maranhão

Pacote de distribuição da ferramenta que processa o relatório **"Situação dos Órgãos e Entidades do Ente Federativo"** do CAUC (Tesouro Nacional) e gera um dashboard interativo pronto para publicação.

> Snapshot embutido: **09/09/2026** — 27 órgãos (2 Direta · 25 Indireta), 26 "A Comprovar", 42 pendências em 5 códigos distintos.

---

## 📂 O que há neste pacote

| Arquivo | Função | Quando usar |
|---|---|---|
| **`index.html`** (1,12 MB) | Dashboard pronto para hospedar (GitHub Pages, Netlify, servidor interno). Abre **já com os dados** do último CSV embutido. | Substituir/criar no seu site público. |
| **`dashboard_auto_update.html`** (55 KB) | Ferramenta local do operador — abre o CSV do dia, mostra o painel e gera novos arquivos. | Quem for atualizar diariamente. **Privado, mantém local.** |
| **`build_auto_update.py`** (8 KB) | Gerador Python do `index.html` (serve para processar em lote ou agendar). | Equipes que preferem terminal ou automação via Cron/GitHub Actions. |
| `dados-cauc.csv` (7,3 KB) | Snapshot do CSV de 09/09/2026 já com nome esperado pelo site. Use como **referência** ou para a primeira publicação quando não houver CSV do dia. | Já vai na raiz do repositório. |
| `README.md` (este arquivo) | Manual completo em português. | Leitura inicial. |

Dependências externas: **nenhuma** para abrir o `index.html` em qualquer navegador moderno (Chrome, Edge, Firefox, Safari). O Python é necessário **apenas** se quiser rodar o `build_auto_update.py`.

---

## 🚀 Quick start — três fluxos possíveis (escolha um)

### Fluxo 1 — Já está hospedado e quer atualizar o site (≈ 30 s por dia) ⭐ recomendado
1. Abra **`dashboard_auto_update.html`** (duplo-clique).
2. Arraste o **CSV do dia** (do CAUC) na barra de upload.
3. Clique em **🚀 Publicar atualização** → o navegador baixa `index.html` + `dados-cauc.csv`.
4. No GitHub Pages (ou Netlify/Vercel), em **Add file → Upload files**, arraste **os dois arquivos** na raiz do repositório e clique em **Commit changes**.
5. Em 1–2 minutos o site serve a versão nova. Em **até 10 min** todas as abas abertas puxam o `dados-cauc.csv` automaticamente — ninguém precisa dar F5.

> **Por que dois arquivos?** O `index.html` é a página (carrega uma vez). O `dados-cauc.csv` é a fonte que o `index.html` lê periodicamente para se atualizar. Sem o segundo, ninguém recebe a versão nova sem reabrir a aba.

### Fluxo 2 — Equipe sem GitHub Pages (envio por e-mail / WhatsApp)
1. Abra `dashboard_auto_update.html`, arraste o CSV, clique **Publicar**.
2. Envie somente o **`index.html`** gerado para os destinatários — ele abre direto no navegador, sem precisar de servidor.
   - Vantagem: chegar cheio de ícones e botões (Exportar Excel, Imprimir).
   - Limitação: o destinatário precisa baixar um `index.html` novo a cada atualização (não há auto-refresh via HTTP por causa do protocolo `file://`).

### Fluxo 3 — Operação 100 % por linha de comando
```bash
# Pré-requisito: Python 3.8+ e as bibliotecas-padrão csv, json, re.
# Não há pacotes externos a instalar.
python3 build_auto_update.py situacao_09-09-2026.csv
# → Gera ./index.html pronto para hospedar.
```
Aceita qualquer arquivo `situacao_*.csv` com o mesmo formato (cabeçalho `CNPJ;Nome;Tipo de Administração;Regularidade Fiscal;…`).

---

## 🔍 O que o painel mostra

1. **Cabeçalho / filtro** — *chip* com a data do CSV, *snapshot* com contagem de órgãos.
2. **🏛️ Banner do Ente Federativo Principal** — Estado do Maranhão em destaque, com bandeira, CNPJ raiz, contagem de pendências e lista dos códigos.
3. **🏛️ Secretarias da Administração Direta com Pendências** *(novo)* — quadro só com as secretarias estaduais e seus códigos específicos.
4. **KPIs** — 6 cartões (Órgãos, "A Comprovar", Pendências, Comprovados, % etc.).
5. **📊 Pendências por Código CAUC** — gráfico de barras + lista com descrição oficial (Tesouro Nacional).
6. **🏆 Ranking de Órgãos com Pendências** — *podium* (medalhas ouro/prata/bronze) + lista ordenada.
7. Rodapé — selos verde/azul fixos para auditoria.

---

## 🧠 Como a "atualização automática para todos" funciona

```
┌──────────────────────────┐    upload     ┌──────────────────────────┐
│ Browser do destinatário  │ ◄──────────►  │ Repositório (GitHub/...) │
│  (index.html + JS)       │    HTTP/GET   │  └─ index.html           │
│                          │   a cada 10m  │  └─ dados-cauc.csv       │ ← este muda
└──────────────────────────┘ + onFocus      └──────────────────────────┘
```

- O `index.html` é estático e carrega 1 vez.
- Após o carregamento, ele faz `GET dados-cauc.csv` a cada **10 minutos** e sempre que a aba volta do segundo plano (`visibilitychange`).
- Se o conteúdo mudou, ele reprocessa o CSV, recalcula **tudo** (KPIs, quadro DIRETAS, gráfico, ranking) e mostra o *toast* `"🔄 Atualização automática aplicada (DD/MM/AAAA)"`.
- O endereço fonte vive numa única linha do `index.html` (`const DATA_SOURCE_URL = 'dados-cauc.csv'`). Se um dia você precisar mudar de fonte (SharePoint, S3, API interna), é só editar essa linha.

---

## 🛠️ Como abrir localmente (sem hospedar)

| Destinatário | Ação |
|---|---|
| Público (com `index.html` em qualquer pasta) | Duplo-clique em `index.html`. Abre no navegador padrão com tudo embutido. |
| Operador do dia a dia | Duplo-clique em `dashboard_auto_update.html`. Interface com área de upload. |
| Equipe técnica | `python3 build_auto_update.py caminho-do.csv` |

**Nenhuma** dessas ações precisa de internet.

---

## ⚠️ Limitações & honestidade

- **Atualização automática para todos** exige que o `index.html` esteja em **http ou https** (GitHub Pages, Vercel, Netlify, servidor interno). Abrindo o arquivo via `file://`, o navegador não deixa o JavaScript ler outro arquivo por segurança — nesse caso o que importa é o *snapshot* embutido e/ou clicar em **🚀 Publicar atualização** localmente.
- CSV do CAUC deve ter: separador `;`, codificação UTF-8, as 5 primeiras linhas com cabeçalho humano (cabeçalho de dados a partir da 6ª linha), colunas obrigatórias `CNPJ`, `Nome`, `Tipo de Administração` e `Regularidade Fiscal`, e colunas numéricas nomeadas como `1.1`, `1.2`, `3.2.3` etc.
- O dicionário CAUC tem **30 códigos oficiais** fixos no `index.html`. Para acrescentar/alterar descrições, edite o objeto `CODIGO_DESCRICAO` (uma vez só por release).

---

## 📞 Manutenção / mudanças

- Para **alterar visual** (cores, fontes, layout): edite o bloco `<style>` no `index.html` ou `dashboard_auto_update.html`.
- Para **alterar lógica** (filtros, contagens, regex de "Direta"): edite o bloco `<script>` no final do HTML e/ou o `build_auto_update.py`.
- Para publicar uma nova release no GitHub Pages: troque **`index.html`** e **`dados-cauc.csv`** na raiz do repositório, commit, e pronto.

Dúvidas ou pedidos: responda ao membro que enviou este pacote.

---

*Versão: Distribuição 09/09/2026 · Bibliotecas embutidas (offline): PapaParse 5.4.1, SheetJS 0.18.5, Chart.js 4.4.1.*
