#!/usr/bin/env python3
"""Confere as regras de SEO das paginas contra o que o Mintlify realmente renderiza.

Uso:  python3 bin/seo-check.py          # confere e sai 1 se houver falha
      python3 bin/seo-check.py --list   # mostra todas as paginas, mesmo as ok
"""
import json, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

TITLE_MIN, TITLE_MAX = 50, 60      # do <title> renderizado
DESC_MIN, DESC_MAX = 100, 130      # da meta description

def site_name():
    return json.load(open('docs.json', encoding='utf-8')).get('name', '')

def frontmatter(path):
    s = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---\n', s, re.S)
    return m.group(1) if m else None

def field(fm, key):
    m = re.search(rf'^{key}:\s*"(.*?)"\s*$', fm, re.M)
    return m.group(1) if m else None

def main():
    show_all = '--list' in sys.argv
    # o Mintlify acrescenta " - <name>" ao title de toda pagina
    suffix = f' - {site_name()}'
    fails, warns, checked = [], [], 0

    for path in sorted(glob.glob('**/*.mdx', recursive=True)):
        fm = frontmatter(path)
        if fm is None:
            fails.append((path, 'sem frontmatter'))
            continue
        title, desc = field(fm, 'title'), field(fm, 'description')
        checked += 1
        problems = []

        if not title:
            problems.append('sem title')
        else:
            rendered = len(title) + len(suffix)
            if rendered > TITLE_MAX:
                problems.append(f'title renderiza {rendered} (max {TITLE_MAX}); '
                                f'corte {rendered - TITLE_MAX} caractere(s)')
            elif rendered < TITLE_MIN:
                # limite brando: title curto nao e erro, so desperdicia espaco na SERP
                warns.append((path, f'title renderiza {rendered}, abaixo dos '
                                    f'{TITLE_MIN} recomendados'))
            if re.search(r'\bAtletis\b', title):
                problems.append('title repete "Atletis", que o sufixo ja acrescenta')

        if not desc:
            problems.append('sem description')
        elif not (DESC_MIN <= len(desc) <= DESC_MAX):
            problems.append(f'description tem {len(desc)} (faixa {DESC_MIN}-{DESC_MAX})')

        if problems:
            fails.append((path, '; '.join(problems)))
        elif show_all:
            print(f'ok    {path}')

    for path, why in warns:
        print(f'aviso {path}: {why}')
    for path, why in fails:
        print(f'FALHA {path}: {why}')

    print(f'\n{checked} paginas conferidas, {len(fails)} com falha, '
          f'{len(warns)} com aviso (sufixo do title: "{suffix}")')
    return 1 if fails else 0

if __name__ == '__main__':
    sys.exit(main())
