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

## Arquivo interno não pode virar rota

O Mintlify publica **todo `.md` e `.mdx` do repositório**, esteja ou não na
navegação. Ele ignora sozinho apenas `README.md`, `LICENSE.md`, `CHANGELOG.md`
e `CONTRIBUTING.md` — nada além disso.

Então instrução para o time, ferramenta e material bruto precisam entrar no
`.mintignore`, ou viram página pública e indexável. Foi o que quase aconteceu
com este próprio arquivo: sem a linha no `.mintignore`, `SEO.md` vira
`ajuda.atletis.com.br/SEO`.

O `bin/seo-check.py` reprova qualquer arquivo que esteja fora da navegação e
fora do `.mintignore`.

## Mudança de estrutura: pergunte antes

Mudar URL, renomear página, mover de módulo ou reorganizar a hierarquia **descarta
o ranking que aquela URL levou meses acumulando**. Não é refactor de código, onde
o pior caso é reverter — a perda é de fora, e demora para voltar.

**Antes de mexer em estrutura, pergunte ao Gustavo.** Vale para renomear arquivo,
mudar pasta, trocar página de módulo, dividir ou juntar páginas. Sempre diga quais
URLs mudam e o que cada uma vale hoje.

**Depois de mexer, em toda mudança estrutural ou ciclo longo de trabalho:**

1. **Redirect para cada URL que sai.** No `redirects` do `docs.json`, com
   `permanent: true`. Sem isso o Google trata como página morta
2. **Atualize o inventário** — `python3 bin/seo-inventario.py`, e commite o
   `seo/inventario.csv`. É a memória das URLs que já existiram
3. **Regenere a planilha** — `python3 bin/seo-planilha.py`, e mande para quem
   cuida de SEO
4. **Confira o sitemap** em `/sitemap.xml` depois que a mudança subir, e o índice
   de páginas em `/llms.txt`

O `bin/seo-check.py` **reprova URL que saiu da navegação sem redirect**, comparando
com o inventário. É a rede de segurança, não o substituto da pergunta: ele pega a
URL perdida, não a decisão de mudar.

## O inventário de URLs

`seo/inventario.csv` guarda toda rota que já existiu, com `estado` de `ativa` ou
`aposentada`. Uma rota nunca é apagada dali — vira aposentada, e o redirect dela
fica sendo cobrado para sempre.

## Ao criar uma página

1. Title dentro do limite, sem a palavra "Atletis"
2. Description entre 100 e 130
3. `keywords` no frontmatter com os termos de busca reais
4. Prosa suficiente para a página se sustentar sem os componentes
5. Se for material interno e não documentação, entre no `.mintignore`
6. `python3 bin/seo-inventario.py` para registrar a rota nova
7. `python3 bin/seo-check.py` antes de abrir o PR
