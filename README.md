# 📊 Dashboard CAUC — Maranhão

> Painel interativo de acompanhamento da **Situação dos Órgãos e Entidades do Ente Federativo** do Estado do Maranhão, com base nos dados do **CAUC — Serviço Auxiliar de Informações para Transferências Voluntárias** da Secretaria do Tesouro Nacional.

[![Status](https://img.shields.io/badge/status-ativo-success)](https://github.com)
[![Licença](https://img.shields.io/badge/licen%C3%A7a-MIT-blue)](LICENSE)
[![Plataforma](https://img.shields.io/badge/plataforma-Web-orange)](#)
[![Offline](https://img.shields.io/badge/100%25-offline-green)](#)
[![Made for Brazil](https://img.shields.io/badge/feito%20no-Brasil-yellow)](#)

🔗 **Acesse o dashboard publicado**: [https://SEU-USUARIO.github.io/dashboard-cauc/](https://SEU-USUARIO.github.io/dashboard-cauc/)

---

## 📋 Sumário

- [Sobre o projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Estrutura do repositório](#-estrutura-do-repositório)
- [Como publicar (GitHub Pages)](#-como-publicar-no-github-pages)
- [Como atualizar o dashboard diariamente](#-como-atualizar-o-dashboard-diariamente)
- [Personalização](#-personalização)
- [Tecnologias utilizadas](#-tecnologias-utilizadas)
- [Privacidade e segurança](#-privacidade-e-segurança)
- [Fonte dos dados](#-fonte-dos-dados)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

---

## 🎯 Sobre o projeto

O **Dashboard CAUC — Maranhão** é uma aplicação web **estática e 100% offline** que processa o relatório CSV da situação dos órgãos e entidades do Maranhão (disponibilizado pelo Tesouro Nacional) e apresenta os dados em um painel visual interativo.

### Para quê serve?

- 📊 **Visualização rápida** do panorama de regularidade fiscal dos órgãos estaduais
- ⚠️ **Identificação imediata** de órgãos com pendências documentais ("A Comprovar")
- 🏆 **Ranking automático** dos órgãos com maior número de pendências
- 📈 **Análise por código CAUC** — quais itens têm mais não-conformidades
- 📤 **Exportação para Excel** dos dados tratados em formato consolidado

### Por que esta solução?

| Característica | Benefício |
|---|---|
| 🔒 **100% client-side** | Nenhum dado sensível trafega por servidores |
| ⚡ **Sem backend** | Hospedagem gratuita em GitHub Pages, Netlify, Vercel |
| 📦 **Arquivo único** | Fácil distribuição por e-mail, pendrive ou intranet |
| 🌐 **Funciona offline** | Pode ser usado em ambientes sem internet após download |
| 🆓 **Open source** | Auditável, modificável, redistribuível |

---

## ✨ Funcionalidades

### 📊 Indicadores principais (KPIs)
- 🏛️ Total de órgãos no relatório (com divisão Direta/Indireta)
- ⚠️ Quantidade e percentual de órgãos com Regularidade Fiscal "A Comprovar"
- 🚨 Total de pendências (itens individuais por código)
- ✅ Órgãos com situação "Comprovados"
- 🔢 Quantidade de códigos CAUC com pendência (de 30 monitorados)

### 📈 Visualizações
- **Gráfico de barras interativo** com pendências por código CAUC (tooltip com descrição completa)
- **Ranking de órgãos** com pódio para os top 3 (ouro, prata, bronze)
- **Lista detalhada de códigos** com descrição oficial do Tesouro Nacional

### 🛠️ Ações disponíveis
- 🔄 **Upload de novo CSV** — atualiza o dashboard com dados do dia
- ⬇️ **Exportação Excel** — planilha consolidada com 3 abas:
  - Pendências (linha por código pendente)
  - Resumo por Órgão (CNPJ + nome + tipo + códigos pendentes)
  - Dicionário CAUC (descrição oficial de cada código)
- 🖨️ **Impressão** — versão otimizada para PDF e impressão física

---

## 📁 Estrutura do repositório

```
dashboard-cauc/
├── 📄 index.html              # Dashboard principal (auto-suficiente)
├── 📁 historico/              # Snapshots diários (opcional, para auditoria)
│   ├── 09-06-2026.html
│   ├── 10-06-2026.html
│   └── ...
├── 📁 dados/                  # CSVs originais (opcional)
│   ├── Situacao_09-06-2026.csv
│   └── ...
├── 📄 README.md               # Este arquivo
└── 📄 LICENSE                 # Licença MIT
```

> 💡 **Dica**: a pasta `historico/` é opcional, mas recomendada para auditoria. Cada snapshot fica acessível em URLs como `https://seu-usuario.github.io/dashboard-cauc/historico/09-06-2026.html`.

---

## 🚀 Como publicar no GitHub Pages

### Pré-requisitos
- ✅ Conta no [GitHub](https://github.com) (gratuita)
- ✅ Arquivo `dashboard_cauc_hibrido_DD-MM-AAAA.html` baixado e renomeado para `index.html`

### Passo a passo

#### 1️⃣ Criar o repositório

1. Acesse [github.com/new](https://github.com/new)
2. Preencha:
   - **Repository name**: `dashboard-cauc`
   - **Description**: `Dashboard CAUC do Maranhão — Atualização diária`
   - Marque ✅ **Public** (obrigatório para GitHub Pages gratuito)
   - Marque ✅ **Add a README file**
3. Clique em **Create repository**

#### 2️⃣ Subir o arquivo HTML

1. No repositório recém-criado, clique em **Add file** → **Upload files**
2. Arraste o seu arquivo (já renomeado como `index.html`)
3. Em **Commit changes**, descreva: `Dashboard inicial — 09/06/2026`
4. Clique em **Commit changes**

#### 3️⃣ Ativar o GitHub Pages

1. No repositório, clique em **Settings** (⚙️ no topo)
2. No menu lateral, clique em **Pages**
3. Em **Build and deployment**:
   - **Source**: `Deploy from a branch`
   - **Branch**: `main`
   - **Folder**: `/ (root)`
4. Clique em **Save**

#### 4️⃣ Aguardar publicação

- Em **1-3 minutos** sua página estará disponível em:
  ```
  https://SEU-USUARIO.github.io/dashboard-cauc/
  ```
- A URL exata aparece no topo da página Settings → Pages com a mensagem:
  > ✅ Your site is live at https://...

#### 5️⃣ Compartilhar

Pronto! Envie a URL pública para gestores, equipe ou stakeholders.

---

## 🔄 Como atualizar o dashboard diariamente

Existem **três métodos** dependendo do seu nível de conforto técnico:

### 🟢 Método 1: Pela interface do GitHub (mais simples)

**Sem instalar nada — só usa o navegador.**

1. Baixe o CSV do dia do CAUC
2. Gere um novo `index.html` (usando a ferramenta de build do projeto ou solicitando ao gerador)
3. Acesse seu repositório no GitHub
4. Clique no arquivo `index.html`
5. Clique no ícone de **lápis** (✏️ Edit)
6. **Apague todo o conteúdo** (Ctrl+A → Delete)
7. **Cole o novo conteúdo** do `index.html`
8. Role até o final → **Commit changes**
9. Em **1-2 minutos** o site é atualizado automaticamente

### 🔵 Método 2: Upload por substituição

1. Acesse o repositório
2. Clique em `index.html` e depois no ícone de **lixeira** (🗑️) para deletar
3. Em **Commit changes**, confirme a remoção
4. Volte ao repositório e clique em **Add file → Upload files**
5. Arraste o novo `index.html`
6. Confirme em **Commit changes**

### ⚫ Método 3: Com Git via linha de comando (avançado)

Para quem quer automatizar:

```bash
# Clonar o repositório (primeira vez)
git clone https://github.com/SEU-USUARIO/dashboard-cauc.git
cd dashboard-cauc

# Substituir o arquivo
cp /caminho/para/novo_dashboard.html index.html

# Versionar com a data como mensagem
git add index.html
git commit -m "Atualização — DD/MM/AAAA"
git push origin main
```

### 💡 Boas práticas de atualização

- ✅ Sempre **mantenha um histórico** dos snapshots em `historico/`:
  ```
  historico/09-06-2026.html
  historico/10-06-2026.html
  ```
- ✅ Use **mensagens de commit** descritivas com a data: `Atualização — 10/06/2026`
- ✅ **Verifique no navegador** se o dashboard ainda funciona após cada update
- ✅ **Compartilhe a URL fixa** (não as URLs do histórico) para uso diário

---

## 🎨 Personalização

### Mudar título e identidade visual

Edite o arquivo `index.html` e localize:

```html
<title>Dashboard CAUC — Maranhão</title>
...
<h1>Dashboard CAUC — Maranhão</h1>
<p class="subtitle">Situação dos Órgãos e Entidades do Ente Federativo</p>
```

### Trocar as cores do tema

No início do `<style>`, edite as variáveis CSS:

```css
:root{
  --primary: #2563eb;        /* Azul principal */
  --warn: #ea580c;           /* Laranja de alerta */
  --danger: #dc2626;         /* Vermelho de erro */
  --success: #16a34a;        /* Verde de sucesso */
}
```

### Adicionar logo do órgão

Substitua o emoji 📊 no cabeçalho por uma `<img>`:

```html
<div class="brand-logo">
  <img src="logo.png" alt="Logo" style="width:40px;height:40px">
</div>
```

E suba o arquivo `logo.png` no mesmo diretório.

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Versão | Uso |
|---|---|---|
| [HTML5](https://developer.mozilla.org/pt-BR/docs/Web/HTML) | — | Estrutura |
| [CSS3](https://developer.mozilla.org/pt-BR/docs/Web/CSS) | — | Estilo e responsividade |
| [JavaScript (ES6+)](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript) | — | Lógica e interatividade |
| [PapaParse](https://www.papaparse.com/) | 5.4.1 | Parsing do CSV |
| [SheetJS](https://sheetjs.com/) | 0.18.5 | Geração de arquivos Excel (.xlsx) |
| [Chart.js](https://www.chartjs.org/) | 4.4.1 | Gráficos interativos |

> Todas as bibliotecas estão **embutidas no próprio HTML** — não há dependências externas em tempo de execução.

---

## 🔐 Privacidade e segurança

### ✅ O que este projeto faz
- Processa o CSV **inteiramente no navegador do usuário**
- Não envia dados para nenhum servidor
- Não usa cookies, analytics ou rastreamento
- Funciona em redes corporativas e governamentais com restrição

### ❌ O que este projeto **não** faz
- Não armazena dados de usuários
- Não conecta a APIs externas em tempo de execução
- Não requer login ou autenticação
- Não coleta informações pessoais

### 📋 Conformidade
- ✅ Compatível com **LGPD** (Lei Geral de Proteção de Dados)
- ✅ Compatível com **Lei de Acesso à Informação** (Lei 12.527/2011)
- ✅ Dados públicos do CAUC, conforme transparência fiscal nacional

---

## 📚 Fonte dos dados

Os dados utilizados neste dashboard são originados do **CAUC — Serviço Auxiliar de Informações para Transferências Voluntárias**, mantido pela Secretaria do Tesouro Nacional (STN) do Ministério da Fazenda.

### Links oficiais
- 🏛️ [Portal CAUC — Tesouro Nacional](https://www.tesourotransparente.gov.br/temas/estados-e-municipios/cauc-sistema-de-informacoes-sobre-requisitos-fiscais)
- 📄 [Metadados oficiais dos itens CAUC](https://www.tesourotransparente.gov.br/)
- 📜 [Arcabouço legal](https://sti.tesouro.gov.br/cauc/)
- 🌐 [Sistema CAUC online](https://cauc.tesouro.gov.br/)

### Códigos CAUC monitorados (30 itens)

<details>
<summary><strong>Clique para expandir a lista completa</strong></summary>

| Código | Descrição |
|---|---|
| 1.1 | Regularidade quanto a Tributos, Contribuições Previdenciárias Federais e Dívida Ativa da União |
| 1.2 | Regularidade no pagamento de precatórios judiciais |
| 1.3 | Regularidade quanto a Contribuições para o FGTS |
| 1.4 | Adimplência Financeira em Empréstimos e Financiamentos concedidos pela União |
| 1.5 | Regularidade perante o Poder Público Federal |
| 2.1.1 | Prestação de Contas de Recursos Federais - SIAFI/Subsistema Transferências |
| 2.1.2 | Prestação de Contas de Recursos Federais - Transferegov |
| 3.1.1 | Relatório de Gestão Fiscal (RGF) — Publicação |
| 3.1.2 | Relatório de Gestão Fiscal (RGF) — Encaminhamento ao Siconfi |
| 3.2.1 | RREO — Publicação |
| 3.2.2 | RREO — Encaminhamento ao Siconfi |
| 3.2.3 | RREO — Anexo 8 ao Siope |
| 3.2.4 | RREO — Anexo 12 ao Siops |
| 3.3 | Encaminhamento das Contas Anuais (DCA) |
| 3.4.1 | Matriz de Saldos Contábeis — Mensal |
| 3.4.2 | Matriz de Saldos Contábeis — Encerramento |
| 3.5 | Cadastro da Dívida Pública (CDP) |
| 3.6 | Transparência da execução orçamentária e financeira |
| 3.7 | Adoção de Sistema Integrado de Administração Financeira (Siafic) |
| 4.1 | Exercício da Plena Competência Tributária |
| 4.2 | Regularidade Previdenciária |
| 4.3 | Aplicação Mínima em Saúde (referência) |
| 5.1 | Aplicação Mínima de Recursos em Educação |
| 5.2 | Aplicação Mínima de Recursos em Saúde |
| 5.3 | Limite de Despesas com PPP |
| 5.4 | Limite de operações de crédito |
| 5.5 | Fundeb — Aplicação mínima para profissionais da educação básica |
| 5.6 | Fundeb — Complementação da União em despesas de capital |
| 5.7 | Fundeb — 50% da complementação VAAT na educação infantil |
| 5.8 | Fundeb — Outros requisitos |

</details>

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para sugerir melhorias:

1. Faça um **Fork** deste repositório
2. Crie uma **branch** para sua feature: `git checkout -b melhoria/nova-funcionalidade`
3. Faça **commit** das alterações: `git commit -m 'Adiciona nova funcionalidade'`
4. Faça **push** para a branch: `git push origin melhoria/nova-funcionalidade`
5. Abra um **Pull Request**

### Ideias para futuras melhorias
- [ ] Histórico de comparação entre dias (gráfico de evolução)
- [ ] Notificações automáticas via e-mail quando órgão sair/entrar da lista
- [ ] Integração com API do CAUC para atualização automática
- [ ] Dashboard com filtros avançados por código
- [ ] Versão multilíngue (PT/EN)
- [ ] PWA (Progressive Web App) com instalação offline

---

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT** — veja o arquivo [LICENSE](LICENSE) para detalhes.

```
MIT License — Copyright (c) 2026

É concedida permissão, gratuita, a qualquer pessoa que obtenha uma cópia
deste software e dos arquivos de documentação associados, para usar, copiar,
modificar, fundir, publicar, distribuir, sublicenciar e/ou vender cópias do
Software, e para permitir que pessoas a quem o Software é fornecido o façam.

O SOFTWARE É FORNECIDO "COMO ESTÁ", SEM GARANTIA DE QUALQUER TIPO.
```

---

## 📞 Contato e suporte

- 🐛 **Bugs e sugestões**: abra uma [Issue](../../issues)
- 💬 **Discussões gerais**: use a aba [Discussions](../../discussions)
- 📧 **Contato direto**: adicione seu e-mail aqui

---

## 🙏 Agradecimentos

- [Secretaria do Tesouro Nacional](https://www.gov.br/tesouronacional/) — pela disponibilização pública e diária dos dados CAUC
- [Tesouro Transparente](https://www.tesourotransparente.gov.br/) — pela documentação detalhada dos metadados
- Comunidade open source mantenedora das bibliotecas PapaParse, SheetJS e Chart.js

---

<div align="center">

**Feito com 💙 para a transparência pública brasileira**

⭐ Se este projeto foi útil, considere dar uma estrela no repositório!

</div>
