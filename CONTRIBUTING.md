# Contribuindo com o OpenNetManager

## Objetivo deste documento

Este documento define como contribuidores devem colaborar com o OpenNetManager de forma previsível, segura e alinhada à arquitetura do projeto. Como a base pretende se tornar um projeto Open Source maduro, contribuições só serão aceitas quando preservarem coerência de domínio, qualidade técnica, segurança e legibilidade.

## Princípios de contribuição

- Toda contribuição deve respeitar a arquitetura oficial do projeto.
- Nenhuma contribuição pode introduzir acoplamento indevido a vendor específico fora da camada apropriada.
- Toda mudança deve ser coberta por testes compatíveis com seu tipo e risco.
- Toda mudança relevante de arquitetura deve atualizar a documentação correspondente.
- Toda alteração pública de comportamento deve refletir em changelog, requisitos ou ADR quando necessário.

## Fluxo de contribuição

1. Abrir issue ou discutir necessidade antes de mudanças grandes.
2. Confirmar alinhamento com roadmap, arquitetura e escopo da fase.
3. Criar branch a partir de `develop` ou branch principal definida pela governança ativa.
4. Implementar com commits semânticos pequenos e revisáveis.
5. Executar formatação, lint, tipagem e testes.
6. Atualizar documentação afetada.
7. Abrir Pull Request com contexto, motivação, riscos e evidências.

## Tipos de contribuição aceitos

- correção de bugs;
- testes;
- documentação;
- melhorias de arquitetura;
- novas integrações por vendor;
- observabilidade e segurança;
- pequenas melhorias de UX server-driven.

## Tipos de contribuição não aceitos sem discussão prévia

- troca radical de stack;
- introdução de SPA frontend desacoplado;
- bypass da camada de serviço;
- acesso direto ao ORM em views;
- dependências pesadas sem justificativa forte;
- feature fora do roadmap sem problema claramente demonstrado.

## Padrões obrigatórios

### Qualidade de código

- Black para formatação.
- isort para imports.
- Flake8 para estilo.
- mypy para tipagem estática gradual.
- pytest para suíte principal.

### Arquitetura

Contribuições devem respeitar, no mínimo, as seguintes regras:

- Views chamam services, não repositories nem ORM diretamente.
- Services orquestram regras e coordenação.
- Repositories persistem e consultam dados.
- Drivers lidam com particularidades por vendor.
- Parsers transformam texto bruto em estruturas de domínio.
- SSH é responsabilidade exclusiva da camada de transporte/conector.

## Requisitos de teste por tipo de mudança

| Tipo de mudança | Teste mínimo esperado |
|---|---|
| Parser novo/alterado | Testes unitários com fixtures reais de CLI |
| Driver novo/alterado | Testes unitários com mocks + integração controlada |
| Service novo/alterado | Testes unitários e integração conforme impacto |
| Repository novo/alterado | Testes de integração com banco |
| View/API | Testes de request/response e autorização |
| Segurança | Testes específicos de regressão e acesso |

## Política de documentação

Toda alteração que modifique comportamento, contrato, fluxo operacional, modelo de dados, endpoints, variáveis de ambiente ou decisões arquiteturais deve atualizar a documentação correspondente no mesmo PR. PRs que entregam código sem atualização documental adequada podem ser rejeitados mesmo quando o código estiver funcional.

## Commits

O projeto adota Conventional Commits. Exemplos:

- `feat(devices): add device registration service`
- `fix(parser): handle missing client table footer`
- `docs(architecture): clarify repository boundaries`
- `test(drivers): add ap130 snapshot contract tests`
- `refactor(services): extract snapshot orchestration policy`

## Pull Requests

Todo PR deve conter:

- problema endereçado;
- motivação;
- escopo exato;
- trade-offs;
- evidências de testes;
- impacto em segurança, banco e compatibilidade;
- documentos atualizados.

## Critérios de rejeição imediata

- ausência de testes quando exigidos;
- violação arquitetural explícita;
- vazamento de credenciais ou segredos;
- código acoplado ao AP130 fora das camadas específicas;
- documentação desatualizada em mudança relevante;
- PR excessivamente grande e não revisável sem justificativa.
