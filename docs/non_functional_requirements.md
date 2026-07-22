# Requisitos Não Funcionais

## Objetivo

Este documento especifica os requisitos não funcionais do OpenNetManager e traduz expectativas de qualidade em critérios verificáveis. Em um sistema que lida com credenciais, SSH, parsing, histórico operacional e colaboração Open Source, esses requisitos são tão importantes quanto as features.

## Categorias cobertas

- arquitetura e manutenibilidade;
- segurança;
- desempenho;
- confiabilidade;
- usabilidade;
- observabilidade;
- testabilidade;
- portabilidade;
- governança e operabilidade.

## RNF-001 — Manutenibilidade arquitetural

O sistema deve preservar a separação formal entre View, Service, Repository, Driver, SSH, Parser e Domain Objects. A manutenibilidade é um requisito explícito porque a complexidade de múltiplos vendors cresce mais por variação estrutural do que por volume bruto de código.

## RNF-002 — Extensibilidade multi-vendor

A adição de um novo vendor deve ser alcançável por adição incremental de componentes específicos, com impacto mínimo fora das camadas de driver, parser, fixtures e registry.

## RNF-003 — Testabilidade alta

As camadas centrais devem ser projetadas para testes unitários e de integração com dependências substituíveis. Dependência rígida em rede real, ORM global ou estado implícito viola este requisito.

## RNF-004 — Segurança por padrão

A aplicação deve adotar defaults seguros para autenticação, sessão, proteção de segredos, sanitização de entradas e logging. Django inclui um conjunto amplo de controles e checklist de deploy que deve orientar a configuração de produção.[web:20]

## RNF-005 — Confidencialidade de credenciais

Segredos devem ser protegidos em repouso e mascarados em trânsito de apresentação. O sistema não pode depender da disciplina manual do operador para evitar exposição de credenciais.

## RNF-006 — Auditabilidade

A plataforma deve oferecer rastreabilidade mínima de operações sensíveis e de falhas relevantes, com registros suficientes para investigação técnica e operacional.

## RNF-007 — Disponibilidade operacional razoável

A Fase 0 não exige alta disponibilidade nativa, porém o sistema deve se comportar de forma estável diante de falhas de dispositivo, credencial ou rede, degradando de modo previsível.

## RNF-008 — Desempenho de leitura

Consultas de dashboard, inventário e histórico recente devem ser suficientemente rápidas para uso operacional normal. A UI não deve depender de SSH síncrono para renderizar páginas de consulta.

## RNF-009 — Desempenho de coleta controlado

Coletas devem ter limites explícitos de timeout, retries e escopo. A prioridade inicial é previsibilidade e segurança operacional, não throughput máximo.

## RNF-010 — Compatibilidade de ambientes

A aplicação deve rodar em desenvolvimento local com SQLite e em produção com PostgreSQL, mantendo consistência funcional básica entre os ambientes. Django 5.2 oferece suporte às duas bases dentro do perfil de stack definido.[page:2]

## RNF-011 — Portabilidade via container

O sistema deve ser empacotável em Docker para padronizar ambiente de execução, reduzir deriva operacional e simplificar onboarding.

## RNF-012 — Qualidade estática

O código deve ser continuamente avaliado por formatação, ordenação de imports, lint e tipagem estática gradual. Python 3.13 favorece um ecossistema moderno de tipagem e tooling, alinhado à estratégia do projeto.[web:3]

## RNF-013 — Observabilidade mínima

Logs estruturados, correlação básica e health checks devem existir desde cedo. Métricas sofisticadas podem evoluir depois, mas ausência total de observabilidade criaria alto custo de suporte.

## RNF-014 — Clareza documental

Toda decisão relevante de arquitetura, operação e contrato deve estar documentada em Markdown de forma suficiente para implementação sem dependência de conhecimento tácito do arquiteto.

## RNF-015 — Usabilidade administrativa

A UI inicial deve priorizar clareza, baixa surpresa e fluxos operacionais objetivos. A escolha por HTMX e Bootstrap 5 privilegia um dashboard server-driven simples e previsível, com menor sobrecarga estrutural inicial do que um SPA completo.

## RNF-016 — Consistência de API

A API deve ser versionada, previsível e coerente em payloads, erros e códigos HTTP. O Django REST Framework provê recursos nativos de versionamento, autenticação e permissões adequados a esse objetivo.[web:18][web:21][web:25]

## RNF-017 — Suporte à segurança de produção

A configuração de produção deve seguir o checklist de deploy seguro do Django, incluindo `check --deploy`, configuração apropriada de `DEBUG`, cookies seguros, host headers e HTTPS.[web:20]

## RNF-018 — Escalabilidade evolutiva

A arquitetura deve permitir a adoção futura de Redis, scheduler avançado e execução assíncrona sem reescrita drástica do núcleo.

## RNF-019 — Integridade dos dados históricos

Snapshots e entidades relacionadas devem preservar o contexto temporal da coleta. O sistema não deve sacrificar rastreabilidade histórica por conveniência de leitura imediata.

## RNF-020 — Contribuição Open Source sustentável

O repositório deve ser governável por regras claras de revisão, branch strategy, definição de pronto e templates de colaboração, reduzindo ruído para maintainers e contribuidores.

## Metas qualitativas recomendadas

| Área | Meta inicial |
|---|---|
| Cobertura de testes das camadas centrais | 80% ou mais nas áreas críticas |
| Tempo de resposta de páginas de leitura comuns | baixo o suficiente para navegação operacional fluida |
| Tempo máximo de handshake SSH | configurável e documentado |
| Densidade de logs sensíveis vazados | zero tolerado |
| Ambiguidade arquitetural remanescente | mínima e explicitamente documentada |

## Trade-offs explícitos

### Simplicidade operacional versus escalabilidade máxima inicial

A Fase 0 favorece um desenho simples de rodar e contribuir. Isso sacrifica alguma capacidade de paralelismo massivo no início, mas reduz custo cognitivo, acelera validação da base e evita dependências prematuras como Redis obrigatório.

### Qualidade formal versus velocidade ad hoc

A documentação, testes e padrões de camada tornam o início mais pesado do que um CRUD tradicional. Em contrapartida, reduzem retrabalho futuro num domínio em que parsing, SSH e multi-vendor tendem a punir atalhos.
