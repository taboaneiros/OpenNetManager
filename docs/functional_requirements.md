# Requisitos Funcionais

## Objetivo

Este documento detalha os requisitos funcionais do OpenNetManager para a Fase 0 e estabelece o contrato de comportamento esperado para a implementação inicial do produto. O objetivo é remover ambiguidades de escopo e transformar a visão de produto em capacidades observáveis, testáveis e rastreáveis.

## Convenções

- Cada requisito funcional possui um identificador estável.
- Requisitos são escritos do ponto de vista do sistema, não da implementação.
- Onde necessário, a motivação arquitetural e os trade-offs são explicitados.
- Requisitos futuros previstos são marcados como diferidos para fases posteriores, sem contaminar o escopo executável inicial.

## Escopo funcional da Fase 0

A Fase 0 define completamente o comportamento a ser implementado, ainda que nem todas as capacidades estejam prontas para execução automática em produção. O foco desta fase é especificar o núcleo funcional inicial do sistema e suas fronteiras.

## Catálogo de requisitos

### RF-001 — Autenticação de usuário

O sistema deve permitir autenticação de usuários da plataforma por meio da camada padrão de autenticação do Django, com fluxo de login, logout e manutenção de sessão autenticada. A solução inicial prioriza simplicidade, maturidade e segurança por padrão em vez de reinventar controle de identidade.

**Justificativa arquitetural:** usar o mecanismo nativo do Django reduz superfície de erro, integra-se ao ecossistema do framework e acelera a implementação da base de segurança.[page:2] O trade-off é menor liberdade para experimentar modelos exóticos de autenticação no início, o que é aceitável na Fase 0.

### RF-002 — Autorização por perfil funcional

O sistema deve restringir ações administrativas, operacionais e de leitura conforme perfil ou permissão atribuída ao usuário. Nem todo usuário autenticado poderá alterar inventário, credenciais ou jobs de coleta.

### RF-003 — Cadastro de dispositivo

O sistema deve permitir cadastrar dispositivos no inventário com, no mínimo:

- nome lógico;
- vendor;
- plataforma;
- hostname ou endereço IP;
- porta SSH;
- descrição opcional;
- status administrativo;
- credencial associada.

### RF-004 — Edição de dispositivo

O sistema deve permitir alterar metadados do dispositivo sem destruir seu histórico operacional. Mudanças cadastrais não podem apagar snapshots, eventos ou jobs relacionados, exceto por ações administrativas explícitas e controladas.

### RF-005 — Desativação lógica de dispositivo

O sistema deve permitir marcar um dispositivo como inativo ou desabilitado para impedir novas coletas operacionais normais sem remover seu histórico persistido.

**Trade-off:** exclusão física simplificaria algumas consultas, mas destruiria rastreabilidade e dificultaria auditoria. A desativação lógica preserva contexto histórico com custo pequeno de filtragem adicional.

### RF-006 — Cadastro de credencial

O sistema deve permitir cadastrar credenciais reutilizáveis com tipo de autenticação, nome descritivo, usuário e material secreto correspondente. O segredo deve ser protegido em repouso e nunca reexibido em claro após a criação.

### RF-007 — Associação de credencial a dispositivo

O sistema deve permitir associar uma credencial a um ou mais dispositivos conforme política definida, respeitando validações de compatibilidade do tipo de autenticação e estado da credencial.

### RF-008 — Rotação de credencial

O sistema deve permitir atualizar o segredo de uma credencial sem recriar o vínculo de todos os dispositivos associados. A operação deve ser auditável e minimizar alterações cascata no inventário.

### RF-009 — Teste de conectividade SSH

O sistema deve permitir que um usuário autorizado execute teste controlado de conectividade SSH para validar credencial, reachability e capacidade mínima de handshake com o dispositivo.

### RF-010 — Resolução de driver por vendor/plataforma

O sistema deve selecionar automaticamente o driver adequado com base nos metadados do dispositivo, sem lógica condicional distribuída por views ou templates. A resolução deve ocorrer em mecanismo centralizado de registry ou factory.

### RF-011 — Coleta manual de snapshot

O sistema deve permitir iniciar manualmente uma coleta de snapshot de um dispositivo elegível. Essa coleta deve acionar o fluxo arquitetural oficial:

View → Service → Driver → SSH → Parser → Domain Objects → Repository

### RF-012 — Coleta de informações de sistema

O sistema deve permitir coletar e persistir informações de sistema disponíveis no dispositivo, como hostname, modelo, plataforma observada, firmware, uptime e outros metadados suportados.

### RF-013 — Coleta de interfaces

O sistema deve permitir coletar, normalizar e persistir informações de interfaces do dispositivo. Essa coleta deve gerar registros vinculados a um snapshot específico, sem sobrescrever diretamente o histórico anterior.

### RF-014 — Coleta de clientes suportados

O sistema deve permitir coletar clientes conectados quando a plataforma suportar essa semântica. Caso a capability não exista no driver, o sistema deve responder de forma explícita e previsível, sem simular sucesso vazio indevido.

### RF-015 — Persistência histórica de snapshot

O sistema deve persistir cada coleta como uma entidade de snapshot independente, registrando pelo menos status, timestamps relevantes, origem do acionamento e duração da operação.

### RF-016 — Registro de status da coleta

O sistema deve classificar a coleta com estados como pendente, executando, sucesso, sucesso parcial, timeout ou falha, conforme taxonomia padronizada do projeto.

### RF-017 — Registro de eventos operacionais

O sistema deve registrar eventos operacionais ou técnicos importantes, incluindo falhas de conexão, falhas de parsing, snapshot concluído, credencial alterada e ações administrativas sensíveis.

### RF-018 — Listagem de dispositivos

O sistema deve oferecer listagem paginada e filtrável de dispositivos, permitindo ao usuário localizar ativos por nome, vendor, plataforma, status ou outros filtros definidos.

### RF-019 — Visualização de detalhe do dispositivo

O sistema deve exibir página de detalhe com visão consolidada do dispositivo, último snapshot, dados de sistema, interfaces, clientes suportados e eventos recentes relevantes.

### RF-020 — Histórico de snapshots

O sistema deve permitir visualizar o histórico de snapshots de um dispositivo, ordenado temporalmente e acessível por filtros básicos.

### RF-021 — Visualização de snapshot individual

O sistema deve permitir abrir um snapshot específico e inspecionar seus dados persistidos de forma isolada do estado atual do dispositivo.

### RF-022 — Dashboard operacional inicial

O sistema deve oferecer dashboard inicial com métricas básicas de inventário e estado operacional agregado, sem acessar SSH diretamente. Toda informação exibida deve vir de serviços e repositórios sobre dados persistidos.

**Justificativa arquitetural:** impedir coleta em tempo real a partir do dashboard reduz acoplamento entre UI e infraestrutura e evita comportamentos imprevisíveis na camada de apresentação.

### RF-023 — API REST versionada

O sistema deve expor uma API REST versionada para leitura e, quando aplicável, escrita controlada sobre recursos centrais como dispositivos, snapshots, eventos, credenciais e jobs.

### RF-024 — Contratos de erro padronizados

A API e os serviços devem operar com taxonomia consistente de erros, permitindo distinguir validação, autorização, conectividade, parsing, conflito de estado e falhas internas.

### RF-025 — Criação de CollectionJob

O sistema deve permitir criar definições persistidas de coleta futura, mesmo que o scheduler automático evolua em fase posterior. Essa modelagem antecipada é necessária para preservar coerência do domínio e evitar remodelagem posterior do fluxo de coleta.

### RF-026 — Habilitação/desabilitação de CollectionJob

O sistema deve permitir ativar e desativar jobs de coleta sem removê-los da base histórica.

### RF-027 — Registro de auditoria mínima

O sistema deve registrar quem executou ações sensíveis como criação de dispositivo, alteração de credencial, teste de conexão e disparo manual de coleta, quando aplicável.

### RF-028 — Máscara de segredos na UI e API

O sistema nunca deve retornar segredo em claro em interfaces humanas ou programáticas após a persistência inicial.

### RF-029 — Extensibilidade multi-vendor

O sistema deve permitir adicionar novos vendors por meio da introdução de drivers, parsers, fixtures e registro de capabilities, sem necessidade de alterar a arquitetura base.

### RF-030 — Health/status endpoint interno

O sistema deve disponibilizar ao menos uma capacidade de health/status para inspeção operacional da aplicação, separada de endpoints de negócio.

## Requisitos explicitamente fora do comportamento executável inicial

Os itens abaixo podem estar modelados, mas não precisam ter implementação operacional completa na primeira etapa funcional do produto:

- scheduler distribuído completo;
- filas assíncronas com Redis;
- auto-discovery de dispositivos;
- suporte multi-vendor implementado além do AP130;
- monitoração em tempo real contínua.

## Matriz resumida de rastreabilidade

| Requisito | Entidade principal | Camadas impactadas |
|---|---|---|
| RF-003 a RF-005 | Device | View, Service, Repository |
| RF-006 a RF-008 | Credential | View, Service, Repository, Security |
| RF-009 a RF-016 | Snapshot / Driver | Service, Driver, SSH, Parser, Repository |
| RF-017 | Event | Service, Repository, Logging |
| RF-018 a RF-022 | Device / Snapshot | View, Service, Repository |
| RF-023 e RF-024 | API | API, Service, Exceptions |
| RF-025 e RF-026 | CollectionJob | View, Service, Repository, Scheduler |
| RF-027 e RF-028 | Audit / Security | Service, Logging, Security |
| RF-029 | Driver ecosystem | Driver, Parser, Tests, ADR |
