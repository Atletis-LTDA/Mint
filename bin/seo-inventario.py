#!/usr/bin/env python3
"""Gera o inventario de URLs do site em seo/inventario.csv.

O inventario e a memoria das URLs que ja existiram. O seo-check.py usa ele para
reprovar URL que sumiu sem redirect -- e assim que se evita perder SEO numa
mudanca de estrutura.

Rode depois de adicionar, renomear ou remover pagina, e commite o resultado.
"""
import csv, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
CSV = 'seo/inventario.csv'

def paginas():
    d = json.load(open('docs.json', encoding='utf-8'))
    nav, out = d.get('navigation', {}), []
    for lang in nav.get('languages', [{'tabs': nav.get('tabs', [])}]):
        for tab in lang.get('tabs', []):
            def walk(node, grupo):
                for x in node.get('pages', []):
                    walk(x, node.get('group', grupo)) if isinstance(x, dict) else out.append(
                        (x, tab.get('tab', ''), grupo))
                for g in node.get('groups', []):
                    walk(g, g.get('group', ''))
            walk(tab, '')
    return out

def campo(fm, k):
    m = re.search(rf'^{k}:\s*"(.*?)"\s*$', fm, re.M)
    return m.group(1) if m else ''

def main():
    antigas = {}
    if os.path.exists(CSV):
        with open(CSV, encoding='utf-8') as f:
            for row in csv.DictReader(f):
                antigas[row['rota']] = row
    linhas, atuais = [], set()
    for slug, tab, grupo in paginas():
        rota = '/' if slug == 'index' else f'/{slug}'
        atuais.add(rota)
        fm = re.match(r'^---\n(.*?)\n---\n', open(f'{slug}.mdx', encoding='utf-8').read(), re.S).group(1)
        linhas.append({'rota': rota, 'modulo': tab, 'grupo': grupo,
                       'title': campo(fm, 'title'), 'description': campo(fm, 'description'),
                       'estado': 'ativa'})
    # rota que existia antes e nao existe mais fica registrada como aposentada
    for rota, row in antigas.items():
        if rota not in atuais:
            row['estado'] = 'aposentada'
            linhas.append(row)
    linhas.sort(key=lambda r: (r['estado'], r['rota']))
    os.makedirs('seo', exist_ok=True)
    with open(CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, ['rota', 'modulo', 'grupo', 'title', 'description', 'estado'])
        w.writeheader(); w.writerows(linhas)
    ativas = sum(1 for r in linhas if r['estado'] == 'ativa')
    apos = len(linhas) - ativas
    print(f'{CSV}: {ativas} ativas, {apos} aposentadas')
    if apos:
        print('Confira se cada rota aposentada tem redirect no docs.json '
              '(o seo-check.py reprova se faltar).')

if __name__ == '__main__':
    sys.exit(main())
