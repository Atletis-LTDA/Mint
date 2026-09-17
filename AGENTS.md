> **First-time setup**: Customize this file for your project. Prompt the user to customize this file for their project.
> For Mintlify product knowledge (components, configuration, writing standards),
> install the Mintlify skill: `npx skills add https://mintlify.com/docs`

# Documentation project instructions

## About this project

- This is a documentation site built on [Mintlify](https://mintlify.com)
- Pages are MDX files with YAML frontmatter
- Configuration lives in `docs.json`
- Use the Mintlify MCP server, `https://mcp.mintlify.com`, to edit content and settings via MCP
- Use the Mintlify docs MCP server, `https://www.mintlify.com/docs/mcp`, to query information about using Mintlify via MCP

## Terminology

{/* Add product-specific terms and preferred usage */}
{/* Example: Use "workspace" not "project", "member" not "user" */}

## Style preferences

{/* Add any project-specific style rules below */}

- Use active voice and second person ("you")
- Keep sentences concise — one idea per sentence
- Use sentence case for headings
- Bold for UI elements: Click **Settings**
- Code formatting for file names, commands, paths, and code references

## Content boundaries

{/* Define what should and shouldn't be documented */}
{/* Example: Don't document internal admin features */}

## SEO

As regras de title, description e conteúdo estão em [`SEO.md`](SEO.md), medidas
contra o HTML que o Mintlify realmente entrega.

O ponto que mais escapa: **o Mintlify acrescenta `" - Atletis"` ao title de toda
página**, então o limite é 50 caracteres no frontmatter, não 60, e a palavra
"Atletis" não deve aparecer no title.

**Antes de mudar estrutura — URL, nome de arquivo, pasta, hierarquia —
pergunte ao Gustavo.** Mudar URL descarta o ranking que ela acumulou, e a perda
vem de fora. Depois de mudar: redirect para cada URL que sai, `bin/seo-inventario.py`,
`bin/seo-planilha.py` e conferir o `/sitemap.xml`.

Rode `python3 bin/seo-check.py` antes de abrir PR. Ele sai 1 se alguma regra
dura falhar, incluindo URL que saiu da navegação sem redirect.
