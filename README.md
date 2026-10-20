# Dashboard CAUC — Maranhão

Painel web para acompanhamento da regularidade fiscal dos órgãos e entidades do Estado do Maranhão, com leitura dos relatórios do CAUC (Tesouro Nacional) e indicadores de governança fiscal para secretarias, batalhões e fundos.

Aplicação **100% client-side** em arquivo HTML único, sem backend. Toda a leitura e o cálculo acontecem no navegador do visitante.

---

## 🏛️ Visão geral

O painel traz em uma única tela duas abas:

- **Regularidade Fiscal** — posição atual dos órgãos do Maranhão junto ao CAUC/STN, com totais, gráficos, ranking por código CAUC e tabela paginada.
- **Governança Fiscal** — indicadores de tempo médio de resolução e reincidência por órgão / secretaria, calculados a partir de uma planilha de episódios que você mantém no Google Drive.

A versão publicada já traz a **Regularidade Fiscal** com os dados mais recentes embutidos, então o painel abre rápido mesmo sem rede. A **Governança Fiscal** requer conexão à internet apenas no momento da leitura da planilha autorizada.

---

## 🧱 Arquitetura

```
┌──────────────────────────┐                ┌──────────────────────────┐
│  Planilha Google Sheets  │──OAuth(ro)──▶  │  Navegador do visitante  │
│  (caderno de episódios)  │                │  (Google Sheets API)     │
└──────────────────────────┘                └────────────┬─────────────┘
                                                        │
                                                        ▼
                                           ┌──────────────────────────┐
                                           │      Renderiza HTML      │
                                           │   (TTR, Reincidência)    │
                                           └──────────────────────────┘

┌──────────────────────────┐                ┌──────────────────────────┐
│ dados-cauc.csv (repo)    │──fetch(no-store)──▶ │ Navegador do visitante │
│ (relatório oficial STN)  │                │  (PapaParse + Chart.js) │
└──────────────────────────┘                └──────────────────────────┘
```

| Aba                     | Fonte                              | Como é lida                                          |
|-------------------------|------------------------------------|------------------------------------------------------|
| Regularidade Fiscal     | `dados-cauc.csv` no repositório    | `fetch('dados-cauc.csv?v=…')` com `cache: no-store` |
| Governança Fiscal       | Planilha no Google Drive           | Google Sheets API + OAuth (escopo somente leitura)   |

A aba **Regularidade Fiscal** funciona totalmente offline — o CSV do último relatório é embutido diretamente no `index.html` publicado, e qualquer atualização no repositório substitui esse snapshot.

A aba **Governança Fiscal** depende exclusivamente da planilha autorizada: o navegador lê via Google Sheets API a cada minuto (e ao retornar à aba), token de curta duração, **nada é gravado em disco**. Por isso **nenhum arquivo de histórico versionado (JSON)** faz parte deste projeto.

---

## 📁 Arquivos do repositório

| Arquivo           | Função                                                                                  |
|-------------------|-----------------------------------------------------------------------------------------|
| `index.html`      | Aplicação completa: HTML, CSS, lógica e bibliotecas embutidas. Abre direto no navegador, inclusive via `file://`. |
| `dados-cauc.csv`  | Relatório CAUC do Maranhão. Substitua este arquivo para atualizar a aba Regularidade Fiscal. |
| `.nojekyll`       | Impede o GitHub Pages de processar a pasta (necessário para servir o `index.html`).     |
| `LICENSE`         | Licença do projeto.                                                                     |
| `README.md`       | Este documento.                                                                          |

---

## 🚀 Como atualizar os dados

### Regularidade Fiscal — relatório oficial do CAUC

1. Gere o relatório mais recente no portal CAUC/STN (`Situação dos Órgãos e Entidades do Ente Federativo – Maranhão – DD-MM-AAAA.csv`).
2. No GitHub → **Add file → Upload files** → arraste o CSV novo, sobrescrevendo `dados-cauc.csv`.
3. Commit. Em até dois minutos, todos que abrirem o link verão os novos valores, porque o `index.html` consulta `dados-cauc.csv` ao abrir e a cada 60 segundos.

### Governança Fiscal — planilha de episódios no Google Drive

As métricas (TTR, reincidência, idade em aberto) são calculadas a partir de uma planilha que **você controla**:

1. Abra a planilha compartilhada com você em modo Leitor.
2. Adicione/atualize linhas na aba `Episódios`. A primeira linha é cabeçalho; as colunas são:

| Coluna | Conteúdo                                                | Exemplo                                  |
|--------|---------------------------------------------------------|------------------------------------------|
| A      | `cnpj` — 14 dígitos, sem máscara                        | `06.354.468/0001-60`                     |
| B      | `nome` — nome do órgão / secretaria                     | `ESTADO DO MARANHAO – SECRETARIA …`     |
| C      | `administracao` — `Direta`, `Indireta` ou `Não classificada` | `Direta`                            |
| D      | `codigo` — item CAUC                                    | `1.3`                                    |
| E      | `status` — `pendente` ou `regularizada`                 | `pendente`                               |
| F      | `data_observacao` — `dd/mm/aaaa` ou `aaaa-mm-dd`        | `20/10/2026`                             |
| G      | `nota` — opcional, livre                                | `Auditoria interna`                      |

3. Quem abrir o painel verá um cartão **Conecte sua planilha no Google Drive**. Ao clicar em **🔐 Conectar ao Google**, o popup nativo do Google solicita consentimento com escopo apenas leitura. As métricas se recalculam em tempo real. Linhas fora do esquema são listadas em um bloco de avisos, sem corromper o restante.

---

## ⚙️ Configurar a integração com Google Sheets (uma vez)

Esta aba usa o fluxo OAuth do Google Identity Services — **não** requer chave de API secreta nem backend, apenas configuração única no Google Cloud:

1. **Console do Google Cloud** (`console.cloud.google.com`) → crie um projeto (ou use um existente) → **APIs e Serviços → Biblioteca** → habilite **Google Sheets API**.
2. **Tela de consentimento OAuth** → adicione o escopo `https://www.googleapis.com/auth/spreadsheets.readonly`.
3. **Credenciais → Criar credenciais → ID do cliente OAuth** → tipo **Aplicativo da Web**:
   - **Origens JavaScript autorizadas**: `https://jokclub.github.io` (e qualquer domínio customizado). Sem esse item o navegador bloqueia o popup.
   - **URI de redirecionamento**: não é necessário para o fluxo `token`.
4. No seu editor, abra o `index.html` e localize o bloco:

   ```html
   <script id="caucGovernanceConfig" type="application/json">
     {"spreadsheetId": "YOUR_GOOGLE_SHEETS_ID",
      "tabName": "Episódios",
      "clientId": "YOUR_OAUTH_CLIENT_ID.apps.googleusercontent.com"}
   </script>
   ```

   …e preencha os três campos:

   - `spreadsheetId` — trecho entre `/d/` e `/edit` na URL da planilha.
   - `tabName` — nome exato da aba (`Episódios`, por padrão).
   - `clientId` — o ID gerado no passo 3.

5. Suba o `index.html` atualizado.

> O `clientId` é público por design — ele identifica seu projeto, **não é senha**. Quem o vê não consegue acessar nada sozinho: cada visitante precisa autorizar com a própria conta Google e ter a planilha compartilhada com ele.

---

## 🌐 Publicação

O site é servido via **GitHub Pages** do próprio repositório:

1. Repositório: `https://github.com/jokclub/dashboard-cauc`.
2. **Settings → Pages → Build and deployment → Source**: `Deploy from a branch` → `main` / `/ (root)`.
3. Endereço público: **`https://jokclub.github.io/dashboard-cauc/`**.

Atualizações futuras não exigem rebuild — basta alterar `index.html`, `dados-cauc.csv` ou a planilha no Drive.

---

## 🔐 Segurança

- **Nunca** publique a planilha como "qualquer pessoa com o link" — isso vaza toda a base sem controle. Use sempre compartilhamento por e-mail em modo **Leitor**.
- O navegador **não grava nada** do que é lido: o token de acesso vive apenas em memória, dura ~1 hora e é renovado a cada minuto e ao retornar à aba.
- A aba Regularidade Fiscal funciona 100% offline (snapshot embutido). A aba Governança Fiscal precisa apenas de acesso à internet no momento da leitura.
- Toda comunicação com a planilha passa pelo endpoint oficial `https://sheets.googleapis.com/v4/spreadsheets/…` autenticado com OAuth.

---

## 📊 Indicadores da aba Governança Fiscal

| Indicador                | Como é calculado                                                                                                                                                                              |
|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Abertas confirmadas      | Itens com `status=pendente` na última leitura.                                                                                                                                                |
| Sem confirmação atual    | Episódios abertos, mas ausentes ou `Desativado` no último relatório. **Não contam como resolução.**                                                                                          |
| TTR (tempo médio)        | Média dos dias corridos entre a primeira observação `pendente` e a primeira `regularizada` por CNPJ + código, apenas em episódios com início conhecido e sem lacuna de observação.        |
| Reincidência (30 dias)   | Retornos do mesmo CNPJ + código dentro de 30 dias após a resolução ÷ resoluções com a janela decorrida e o par ainda observado no último relatório.                                         |
| Maior idade em aberto    | Maior número de dias entre a primeira observação `pendente` e a última leitura.                                                                                                               |

**Sem base ≠ 0%**. O painel mostra "Sem base" sempre que o denominador está vazio (poucos episódios, lacunas de observação ou janela não decorrida).

### Como uma resolução é detectada

Uma transição `pendente → regularizada` no mesmo CNPJ + código `encerra` um episódio. Um novo `pendente` depois disso `abre` outro episódio, preservando o anterior para calcular reincidência.

Linhas fora do esquema (CNPJ, código, data, status inválidos) são listadas em um bloco de aviso no topo da aba, sem afetar o restante.

---

## 🛠️ Solução de problemas

- **Planilha não conecta**: confirme os três campos do bloco `caucGovernanceConfig`; verifique se **Origens JavaScript autorizadas** no Google Cloud contém exatamente a URL do GitHub Pages (`https://`, sem barra no final).
- **Indicadores sempre "Sem base"**: revise se as linhas estão ordenadas da mais antiga para a mais recente e se `status` está exatamente como `pendente` ou `regularizada` (sem acento, espaço extra ou caixa diferente).
- **Linhas rejeitadas**: o painel mostra, no topo da aba Governança Fiscal, as primeiras entradas inválidas com a posição na planilha. Corrija e clique em **↻ Atualizar histórico**.

---

## 📝 Licença

Veja [`LICENSE`](./LICENSE) para detalhes.
