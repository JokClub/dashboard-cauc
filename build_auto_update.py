#!/usr/bin/env python3
"""Build the 'auto-update' dashboard - hybrid + publish button."""
import os, re, csv, io, json, sys

WEBAPP = os.path.dirname(os.path.abspath(__file__))

def read(name):
    with open(os.path.join(WEBAPP, name), 'r', encoding='utf-8') as f:
        return f.read()

def natural_key(s):
    parts = re.split(r'(\d+)', str(s))
    return [int(p) if p.isdigit() else p.lower() for p in parts] if s else ['']  # noqa

def neutralize(js_code):
    return js_code.replace('</script>', '<\\/script>')

CSV_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(WEBAPP, 'situacao_maranhao.csv')

with open(CSV_PATH, 'r', encoding='utf-8') as f:
    raw_text = f.read()

lines = raw_text.split('\n')

data_pesquisa = ''
for line in lines:
    if 'Data da Pesquisa' in line:
        m = re.search(r'\d{2}/\d{2}/\d{4}', line)
        if m: data_pesquisa = m.group(0)
        break

header_idx = next(i for i, l in enumerate(lines) if 'CNPJ' in l and 'Regularidade Fiscal' in l)
csv_body = '\n'.join(lines[header_idx:])

reader = csv.DictReader(io.StringIO(csv_body), delimiter=';')
rows = [{k.strip().strip('"'): (v.strip() if v else '') for k, v in r.items() if k} for r in reader]
rows = [r for r in rows if r.get('CNPJ')]

all_keys = list(rows[0].keys()) if rows else []
numeric_cols = [k for k in all_keys if re.match(r'^\d+(\.\d+)+$', k.strip())]

total = len(rows)
direta = sum(1 for r in rows if r.get('Tipo de Administração') == 'Direta')
indireta = sum(1 for r in rows if r.get('Tipo de Administração') == 'Indireta')
a_comprovar = [r for r in rows if r.get('Regularidade Fiscal') == 'A Comprovar']
comprovados = [r for r in rows if r.get('Regularidade Fiscal') == 'Comprovados']

CODIGO_DESCRICAO = {
  "1.1":  "Regularidade quanto a Tributos, Contribuições Previdenciárias Federais e Dívida Ativa da União",
  "1.2":  "Regularidade no pagamento de precatórios judiciais",
  "1.3":  "Regularidade quanto a Contribuições para o FGTS",
  "1.4":  "Adimplência Financeira em Empréstimos e Financiamentos concedidos pela União",
  "1.5":  "Regularidade perante o Poder Público Federal",
  "2.1.1":"Prestação de Contas de Recursos Federais - SIAFI/Subsistema Transferências",
  "2.1.2":"Prestação de Contas de Recursos Federais - Transferegov",
  "3.1.1":"Relatório de Gestão Fiscal (RGF) — Publicação",
  "3.1.2":"Relatório de Gestão Fiscal (RGF) — Encaminhamento ao Siconfi",
  "3.2.1":"Relatório Resumido de Execução Orçamentária (RREO) — Publicação",
  "3.2.2":"RREO — Encaminhamento ao Siconfi",
  "3.2.3":"RREO — Anexo 8 ao Siope",
  "3.2.4":"RREO — Anexo 12 ao Siops",
  "3.3":  "Encaminhamento das Contas Anuais (DCA)",
  "3.4.1":"Matriz de Saldos Contábeis — Mensal",
  "3.4.2":"Matriz de Saldos Contábeis — Encerramento",
  "3.5":  "Cadastro da Dívida Pública (CDP)",
  "3.6":  "Transparência da execução orçamentária e financeira",
  "3.7":  "Adoção de Sistema Integrado de Administração Financeira (Siafic)",
  "4.1":  "Exercício da Plena Competência Tributária",
  "4.2":  "Regularidade Previdenciária",
  "4.3":  "Aplicação Mínima em Saúde (referência)",
  "5.1":  "Aplicação Mínima de Recursos em Educação",
  "5.2":  "Aplicação Mínima de Recursos em Saúde",
  "5.3":  "Limite de Despesas com PPP",
  "5.4":  "Limite de operações de crédito",
  "5.5":  "Fundeb — Aplicação mínima para profissionais da educação básica",
  "5.6":  "Fundeb — Complementação da União em despesas de capital",
  "5.7":  "Fundeb — 50% da complementação VAAT na educação infantil",
  "5.8":  "Fundeb — Outros requisitos"
}

pendencias = []
for r in a_comprovar:
    for col in numeric_cols:
        if r.get(col, '').strip() == 'A Comprovar':
            pendencias.append({
                'CNPJ': r['CNPJ'],
                'Nome': r['Nome'],
                'Tipo de Administração': r['Tipo de Administração'],
                'Código': col,
                'Descrição': CODIGO_DESCRICAO.get(col, '(Descrição não cadastrada)')
            })

# Detectar ente federativo principal: linhas "Direta" cujo nome começa com "ESTADO "
# (genérico - funciona para MA, SP, MG, etc.)
ESTADO_NOME_RE = re.compile(r'^\s*ESTADO\s+(DE|DO|DA)\s+', re.IGNORECASE)
estado_raiz_rows   = [r for r in rows if r.get('Tipo de Administração') == 'Direta'
                       and ESTADO_NOME_RE.match(r.get('Nome', ''))]
estado_raiz_nomes  = sorted({rr['Nome'].strip() for rr in estado_raiz_rows}, key=len)
estado_raiz_nome   = estado_raiz_nomes[0] if estado_raiz_nomes else 'Ente Federativo Principal'
estado_raiz_cnpj   = next((rr['CNPJ'] for rr in estado_raiz_rows if rr['Nome'].strip() == estado_raiz_nome), '')

estado_ids = {rr['CNPJ'] for rr in estado_raiz_rows}
estado_secretarias = []
for rr in estado_raiz_rows:
    if rr['Nome'].strip() != estado_raiz_nome:
        estado_secretarias.append({'cnpj': rr['CNPJ'], 'nome': rr['Nome']})

estado_pendencias_list = [p for p in pendencias if p['CNPJ'] in estado_ids]
estado_codigos = sorted({p['Código'] for p in estado_pendencias_list}, key=natural_key)
estado_pendencias_full = sorted(
    [{'CNPJ': p['CNPJ'], 'Nome': p['Nome'],
      'Tipo de Administração': p['Tipo de Administração'],
      'Código': p['Código'], 'Descrição': p['Descrição']}
     for p in estado_pendencias_list],
    key=lambda p: (p['Nome'], natural_key(p['Código'])))

estado_data = {
    'raiz_nome':         estado_raiz_nome,
    'raiz_cnpj':         estado_raiz_cnpj,
    'secretarias_count': len(estado_secretarias),
    'pendencias':        estado_pendencias_full,
    'qtd_pendencias':    len(estado_pendencias_full),
    'codigos':           estado_codigos,
}

code_counts = {}
for p in pendencias:
    code_counts[p['Código']] = code_counts.get(p['Código'], 0) + 1

groups = {}
for p in pendencias:
    cnpj = p['CNPJ']
    if cnpj not in groups:
        groups[cnpj] = {'CNPJ': cnpj, 'Nome': p['Nome'], 'Tipo': p['Tipo de Administração'], 'codes': []}
    groups[cnpj]['codes'].append(p['Código'])

ranking = sorted(groups.values(), key=lambda g: -len(g['codes']))

orgs_unicos = len(groups)
media = round(len(pendencias) / orgs_unicos, 1) if orgs_unicos else 0

totals = {
    'total': total,
    'direta': direta,
    'indireta': indireta,
    'aComprovar': len(a_comprovar),
    'aComprovarPct': round((len(a_comprovar) / total) * 100, 1) if total else 0,
    'comprovados': len(comprovados),
    'comprovadosPct': round((len(comprovados) / total) * 100, 1) if total else 0,
    'pendencias': len(pendencias),
    'mediaPorOrgao': media,
    'codigosUnicos': len(code_counts),
}

print(f'=== Build auto-update dashboard ===')
print(f'CSV:              {CSV_PATH}')
print(f'Data:             {data_pesquisa}')
print(f'Total órgãos:     {total}')
print(f'A Comprovar:      {len(a_comprovar)}')
print(f'Pendências:       {len(pendencias)}')
print(f'Ente raiz:        {estado_raiz_nome} ({estado_raiz_cnpj})')
print(f'Secretarias:      {len(estado_secretarias)}')
print(f'Pendências ente:  {len(estado_pendencias_full)}')

template = read('dashboard_auto_update.html')
papa     = neutralize(read('papaparse.min.js'))
xlsx_js  = neutralize(read('xlsx.full.min.js'))
chartjs  = neutralize(read('chart.umd.min.js'))

template = template.replace('__PAPAPARSE__', papa)
template = template.replace('__XLSX__', xlsx_js)
template = template.replace('__CHARTJS__', chartjs)
template = template.replace('__DATA_PESQUISA__', data_pesquisa or '—')
template = template.replace('__TOTAL_ORGAOS__', str(total))
template = template.replace('__TOTALS_JSON__', json.dumps(totals, ensure_ascii=False))
template = template.replace('__PENDENCIAS_JSON__', json.dumps(pendencias, ensure_ascii=False))
template = template.replace('__CODE_COUNTS_JSON__', json.dumps(code_counts, ensure_ascii=False))
template = template.replace('__RANKING_JSON__', json.dumps(ranking, ensure_ascii=False))
template = template.replace('__ESTADO_JSON__', json.dumps(estado_data, ensure_ascii=False))

out_path = os.path.join(WEBAPP, 'index.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(template)

size_kb = os.path.getsize(out_path) / 1024
print(f'\nGerado:  {out_path}')
print(f'Tamanho: {size_kb:.1f} KB')
