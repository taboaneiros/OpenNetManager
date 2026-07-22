# Qualidade e Governança de Entrega

## Objetivo

Consolidar Definition of Done, Definition of Ready, estratégia de branches, commits, revisão e templates operacionais do OpenNetManager.

## Definition of Ready

Um item de backlog está pronto para implementação quando:

- objetivo está claro;
- escopo está delimitado;
- impacto arquitetural foi entendido;
- dependências foram identificadas;
- critérios de aceitação existem;
- documentação afetada foi identificada.

## Definition of Done

Um item está pronto quando:

- código implementado e revisado;
- testes adequados criados/atualizados;
- lint, formatação e tipagem aprovados;
- documentação atualizada;
- impactos em segurança e banco avaliados;
- sem regressão conhecida crítica;
- PR aprovado e pipeline verde.

## Conventional Commits

Padrão adotado:

- `feat:` nova funcionalidade
- `fix:` correção
- `docs:` documentação
- `refactor:` refatoração sem mudança funcional
- `test:` testes
- `chore:` manutenção
- `perf:` performance
- `ci:` pipeline
- `build:` build e dependências

## Branch strategy

Estratégia recomendada inicial:

- `main`: estável/publicável
- `develop`: integração contínua principal
- `feature/*`: novas funcionalidades
- `fix/*`: correções
- `hotfix/*`: correções urgentes sobre `main`
- `docs/*`: documentação ampla quando isolada

## Git Flow

Adotar uma forma leve de Git Flow, sem burocracia excessiva. O objetivo é separar claramente linha estável, integração e trabalho temporário, preservando revisão e rastreabilidade.

## Semantic Versioning

O projeto deve adotar versionamento semântico:

- MAJOR para breaking changes;
- MINOR para adições compatíveis;
- PATCH para correções compatíveis.

## Review checklist

- a mudança respeita a arquitetura?
- existe acoplamento indevido ao AP130?
- view acessa ORM diretamente?
- parser faz transporte ou persistência?
- driver está apenas orquestrando?
- testes cobrem o risco da mudança?
- documentação foi atualizada?
- há impacto de segurança ou segredo?
- migrations são seguras e revisáveis?

## Pull Request template

```markdown
## Objetivo

## Problema resolvido

## Escopo da mudança

## Decisões e trade-offs

## Testes executados

## Impacto em banco, segurança e compatibilidade

## Documentação atualizada
```

## Issue templates

### Bug report

```markdown
## Descrição
## Comportamento esperado
## Comportamento atual
## Passos para reproduzir
## Evidências
## Ambiente
```

### Feature request

```markdown
## Contexto
## Problema
## Proposta
## Alternativas consideradas
## Impacto arquitetural presumido
```
