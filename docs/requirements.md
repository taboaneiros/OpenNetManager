# Requisitos do Projeto

## Objetivo

Este documento consolida a visão de requisitos de alto nível que orienta a Fase 0 e prepara o detalhamento posterior em requisitos funcionais e não funcionais.

## Requisitos de negócio

- O sistema deve centralizar informações de dispositivos de rede suportados.
- O sistema deve permitir operação inicial com AP130 via SSH.
- O sistema deve ser expandível para múltiplos fabricantes.
- O sistema deve manter histórico de coletas relevantes.
- O sistema deve expor informações por dashboard e API.
- O sistema deve ser adequado à publicação Open Source.

## Requisitos de arquitetura

- O sistema deve adotar camadas explícitas de View, Service, Repository, Driver, SSH, Parser e Domain Objects.
- A camada de apresentação não deve acessar ORM diretamente.
- O driver não deve persistir dados diretamente.
- O parser não deve abrir conexões remotas.
- O domínio deve ser modelado com abstrações reutilizáveis e independentes do AP130.

## Requisitos de dados

- O sistema deve modelar Device, Client, Snapshot, Interface, SystemInfo, Event, Credential e CollectionJob.
- O sistema deve suportar SQLite em desenvolvimento e PostgreSQL em produção.
- O sistema deve manter dados históricos suficientes para auditoria operacional.

## Requisitos de segurança

- O sistema deve proteger credenciais e segredos.
- O sistema deve auditar operações sensíveis.
- O sistema deve restringir acesso a funções administrativas.
- O sistema deve evitar vazamento de segredos por logs, erros ou API.

## Requisitos de qualidade

- O projeto deve ter testes unitários, de integração e E2E planejados.
- O projeto deve adotar lint, formatação, tipagem e pipeline automatizado.
- O projeto deve documentar critérios de pronto e de revisão.

## Requisitos de evolução

- O produto deve admitir novos vendors por adição incremental de drivers e parsers.
- O produto deve admitir scheduler e cache no futuro sem reestruturação radical.
- O produto deve admitir API versionada e superfície de integração estável.
