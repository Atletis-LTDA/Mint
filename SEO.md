# SEO deste site

Regras que valem para toda página do `ajuda.atletis.com.br`, com o que foi
medido no HTML que o Mintlify realmente entrega — não no que a documentação
promete.

**Confira antes de abrir PR:**

```bash
python3 bin/seo-check.py          # sai 1 se alguma regra dura falhar
python3 bin/seo-check.py --list   # mostra também as páginas que passaram
```

## Title

**O Mintlify acrescenta `" - Atletis"` ao title de toda página.** São 10
caracteres que não aparecem no frontmatter e contam na SERP. Um title de 60 no
arquivo renderiza 70 e é cortado pelo Google.

| Regra | |
|---|---|
| Máximo | **50 caracteres no frontmatter** (60 renderizado) — regra dura |
| Mínimo | 40 no frontmatter (50 renderizado) — recomendação, não erro |
| Marca | **não escreva "Atletis" no title.** O sufixo já põe |

Antes desta regra, 20 das 24 páginas estouravam o limite renderizado, e a home
trazia "Atletis" duas vezes no mesmo title.

## Description

Entre **100 e 130 caracteres**, sem sufixo — vai literal para a
`meta name="description"`, para `og:description` e para o JSON-LD.

Descrição longa demais é cortada; curta demais desperdiça o espaço.

## O que a plataforma controla e nós não

Três apontamentos recorrentes de ferramentas de SEO **não têm correção neste
repositório**. Verificado no HTML de produção em 17/09/2026:

| Apontamento | Por quê |
|---|---|
| `<html lang="en">` | O Mintlify emite `lang="en"` fixo mesmo com `navigation.languages` em `pt-BR`. O seletor mostra "Português (BR)" e a busca filtra por `pt-BR`, mas a raiz não muda. É chamado para o suporte deles |
| "Primeiro heading é H2" | O `<h1>` existe. O Mintlify injeta dois `<h2>` antes dele no `<body>`: um blockquote `sr-only` de "Documentation Index" e o "Na página" do índice lateral |
| Imagens sem `width`/`height` | As únicas imagens são as duas do logo, vindas do `docs.json`, renderizadas pela plataforma com `alt="light logo"` e `alt="dark logo"` |

Estilos inline também são majoritariamente da plataforma. Vale evitar os nossos,
mas remover só os nossos não limpa o apontamento.

## Conteúdo: o que o crawler enxerga

**Componente que depende de JavaScript não conta como conteúdo.** Os embeds de
Instagram da home saem no HTML servido como `<div>` vazias com a altura
reservada:

```html
<div data-as="iframe"><div style="height:660px;width:100%"></div></div>
```

Para o Google, aquilo é altura vazia, não depoimento. O mesmo vale para
qualquer `iframe`.

Cards e Steps também não contam como texto corrido. Uma página montada só com
eles é lida como *thin content* por mais completa que pareça na tela.

**Na prática:** toda página precisa de prosa própria, e um bloco que existe só
via JavaScript pede um equivalente em texto ao lado dele.

## Ao criar uma página

1. Title dentro do limite, sem a palavra "Atletis"
2. Description entre 100 e 130
3. `keywords` no frontmatter com os termos de busca reais
4. Prosa suficiente para a página se sustentar sem os componentes
5. `python3 bin/seo-check.py` antes de abrir o PR
