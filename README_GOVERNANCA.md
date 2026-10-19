# Dashboard CAUC — Governança Fiscal

Mantém o novo template e adiciona a aba Governança Fiscal. A base foi atualizada com o CSV real de 19/10/2026 consultado no repositório JokClub/dashboard-cauc: 43 pendências, sendo 1 Direta. O histórico compara 16 e 19/10/2026. Nenhum dado histórico foi inventado.

## Publicar pela interface web

1. Faça backup do repositório. Substitua index.html e adicione historico_pendencias.json na raiz. Mantenha o seu dados-cauc.csv mais recente; o CSV do pacote é a base pública de 19/10/2026. Não substitua um relatório mais novo pelo antigo.
2. Para a atualização persistente automática, adicione scripts/atualizar_historico.py e .github/workflows/governanca-pages.yml nas pastas indicadas. Pela interface web, Add file > Create new file permite digitar o caminho completo, incluindo .github.
3. Settings > Pages > Build and deployment > Source: GitHub Actions.
4. Em Actions, abra CAUC - histórico e publicação e use Run workflow na primeira instalação, se necessário. O workflow valida o CSV, atualiza o JSON, faz commit e publica o site. Não requer token pessoal. A conta que configura precisa de permissão de escrita/administração; políticas da organização ou proteção de branch podem exigir autorização.
5. Nas atualizações seguintes, substitua somente dados-cauc.csv e confirme o commit. Confira se a execução em Actions terminou em verde.

## Só instalar o HTML e o JSON

A aba funciona e lê o JSON publicado, mas o navegador NÃO grava no repositório. Sem o workflow, atualize o histórico rodando o script ou publique um JSON válido produzido por ele. Os dois relatórios reais disponíveis ainda não oferecem resoluções elegíveis para TTR ou reincidência. Importar JSON só altera a sessão atual. O botão Gerar HTML Atualizado embute os dados e o histórico carregados, inclusive para uso offline.

## Métricas

- TTR: dias corridos entre primeira pendência observada e primeira regularização observada, média de episódios encerrados com início conhecido e sem lacuna de observação do item. Casos preexistentes no primeiro relatório ficam fora da média. Não é o instante real de início ou resolução.
- Idade aberta: dias desde a primeira observação até o último relatório do histórico. É um limite inferior para os casos de início desconhecido.
- Reincidência: episódios resolvidos com retorno do mesmo CNPJ/código em até 30 dias, divididos pelas resoluções com ao menos 30 dias decorridos e CNPJ/código observado no relatório final. Numerador e denominador usam a mesma base madura. O acompanhamento é amostral nas datas dos relatórios; retornos entre coletas podem não ser detectados.
- Filtro de período: aplicado à data da resolução para TTR, encerradas e reincidência. Pendências abertas refletem a posição final. Direta é o filtro inicial; é possível selecionar Indireta ou Todas.
- Identificação por CNPJ. Não se infere vinculação de fundos/batalhões a uma secretaria. O gráfico mostra até 12 órgãos com maior valor; a tabela lista todos no filtro.
- Sem base não significa zero. Taxa de 0% só aparece quando existe denominador elegível.

## Qualidade e proteção do histórico

O processador aceita apenas CNPJs válidos, exige Data da Pesquisa e colunas CAUC, não usa a data do upload e não considera ausência, traço, campo vazio ou Desativado como regularização. Registros CNPJ/código pendentes com status fiscal incompatível bloqueiam o processamento para revisão.

O mesmo relatório é idempotente, inclusive se mudar apenas a quebra de linha. Uma versão diferente da mesma data ou relatório anterior é rejeitada: correções retroativas exigem reprocessar os CSVs originais em ordem cronológica. Queda no total de órgãos bloqueia atualização para conferir se o relatório está completo; ajuste legítimo exige revisão do script por responsável técnico. Isso é uma salvaguarda, não prova de completude do CSV.

O histórico inicial compara 2 relatórios reais (16 e 19/10/2026). Os 67 episódios registrados em 16/10 tinham início desconhecido. Em 19/10, 43 itens continuam confirmados como pendentes (1 Direta e 42 Indiretas); 24 itens não têm confirmação de regularização (16 Diretas e 8 Indiretas), pois foram desativados ou não estão comprovados. Esses casos ficam em Sem confirmação atual e não são encerrados artificialmente. Não há resoluções observadas elegíveis; TTR e reincidência começam sem base. Não foram inferidos eventos dos dias intermediários.

Guarde backups dos CSVs diários: o JSON conserva eventos e identificadores dos relatórios, mas não substitui os arquivos-fonte para reconstrução. O workflow captura os relatórios que efetivamente processa; uploads rápidos em sequência podem ser consolidados e não são uma ferramenta de importação histórica em lote.

Os dados do JSON e do CSV ficarão públicos, como o repositório e o dashboard. Nunca grave tokens, credenciais ou informações não autorizadas. Nenhuma credencial é embutida no HTML.
