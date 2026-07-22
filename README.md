# OpenNetManager

OpenNetManager é uma plataforma Open Source para gerenciamento de dispositivos de rede com arquitetura orientada a múltiplos fabricantes, construída para abstrair coleta, normalização, persistência e exposição de dados operacionais sem acoplamento ao fornecedor inicial suportado. A Fase 0 define as bases de produto, arquitetura, qualidade, contribuição e segurança necessárias para que uma equipe senior implemente o sistema com previsibilidade, baixo acoplamento e elevada capacidade de evolução.[web:1][web:12][web:3]

O primeiro fabricante suportado será o AP130 via SSH, porém toda a solução deve ser desenhada como uma plataforma multi-vendor desde o primeiro commit, com drivers, parsers, serviços e repositórios desacoplados, permitindo a futura incorporação de Cisco, Huawei, Juniper, Mikrotik, Aruba e Ubiquiti sem reescrever o núcleo da aplicação.

## Objetivo

O objetivo do OpenNetManager é oferecer uma base de gerenciamento de rede centrada em inventário, coleta operacional, snapshots, leitura de interfaces, consolidação de eventos e exposição de dados por dashboard e API, mantendo separação estrita entre UI, regras de negócio, persistência, transporte SSH e parsing. O sistema deve permitir que funcionalidades futuras, como cache distribuído, agendamento avançado e integrações externas, sejam acrescentadas sem quebra estrutural significativa.

## Princípios arquiteturais

- SOLID em todos os níveis de desenho.
- Clean Architecture como referência de dependências internas.
- Repository Pattern para isolar persistência.
- Service Layer para orquestração de casos de uso.
- Driver Pattern para encapsular diferenças de fabricantes.
- Parser Pattern para transformar saída textual em objetos de domínio.
- Dependency Injection explícita nas fronteiras centrais.
- Separation of Concerns entre apresentação, aplicação, domínio e infraestrutura.
- DRY, KISS e YAGNI como filtros de decisão de escopo.
- DDD Lite para nomeação, agregados e responsabilidades.

## Stack base

| Camada | Tecnologia | Papel |
|---|---|---|
| Linguagem | Python 3.13 | Linguagem principal do backend e automação de domínio.[web:3] |
| Framework web | Django 5.2 | Base MVC, ORM, autenticação, admin e configuração principal.[web:1][web:12] |
| API | Django REST Framework | Exposição de endpoints REST, serialização e políticas de autenticação. |
| UI | Bootstrap 5 + HTMX | Interface server-driven com interações incrementais. |
| Transporte SSH | Paramiko | Execução controlada de comandos em dispositivos. |
| Configuração | django-environ | Gestão de variáveis de ambiente. |
| Banco local | SQLite | Desenvolvimento local e bootstrap inicial. |
| Banco principal | PostgreSQL | Persistência de produção. |
| Futuro cache/filas | Redis | Cache, coordenação e otimizações futuras. |
| Qualidade | pytest, Black, isort, Flake8, mypy | Testes, formatação, estilo e tipagem. |
| Entrega | GitHub Actions, Docker | CI/CD e empacotamento. |

## Estrutura alvo

```text
OpenNetManager/
├── apps/
│   ├── authentication/
│   ├── dashboard/
│   ├── devices/
│   ├── monitoring/
│   └── api/
├── core/
├── drivers/
├── services/
├── repositories/
├── parsers/
├── ssh/
├── exceptions/
├── constants/
├── utils/
├── cache/
├── logging/
├── config/
├── templates/
├── static/
├── media/
├── tests/
└── docs/
```

## Fluxo arquitetural obrigatório

```text
View
↓
Service
↓
Repository
↓
Driver
↓
SSH
↓
Parser
↓
Domain Objects
```

Restrições mandatórias:

- Views nunca acessam ORM diretamente.
- Dashboard nunca abre conexão SSH.
- Parsers nunca abrem conexão nem persistem dados.
- Drivers apenas orquestram comandos, sessão e seleção de parser.
- Repositories respondem exclusivamente pela persistência e consultas.
- Serviços coordenam regras de negócio, transações e contratos de aplicação.

## Entregas da Fase 0

A Fase 0 produz a documentação fundacional completa do projeto OpenNetManager, incluindo visão do produto, requisitos, arquitetura, modelo de domínio, decisões arquiteturais, padrões de implementação, estratégia de testes, segurança, pipeline de entrega, diretrizes de API e roadmap inicial. Esta fase não visa maximizar features, mas reduzir ambiguidade de implementação.

## Decisões iniciais relevantes

### Django 5.2 como base

Django 5.2 é uma escolha sólida para um projeto Open Source de gerenciamento de rede porque combina ecossistema maduro, ORM robusto, autenticação integrada e suporte LTS, reduzindo custo operacional de fundação.[web:1][web:12] O trade-off é uma base mais opinativa que frameworks minimalistas, mas essa opinião favorece consistência, onboarding e segurança por padrão em um produto colaborativo.[web:1]

### Python 3.13 como baseline

Python 3.13 oferece melhorias relevantes de experiência do desenvolvedor, evolução de tipagem e avanços de performance da série 3.13, o que beneficia manutenção, automação e qualidade de tooling do projeto.[web:3] O trade-off é exigir atenção a compatibilidade de dependências, mas a escolha mantém o projeto alinhado com versões atuais e práticas modernas do ecossistema.[web:1][web:3]

### HTMX + Bootstrap 5 para a UI

A decisão por HTMX e Bootstrap 5 prioriza um dashboard server-driven com menor complexidade operacional inicial, evitando a necessidade de um SPA completo na Fase 0. O trade-off é menor riqueza de interações client-heavy quando comparado a frameworks frontend dedicados, mas a abordagem acelera entrega, reduz sobrecarga cognitiva e preserva simplicidade arquitetural.

## Documentação

A documentação do projeto está organizada em dois níveis:

- Raiz do repositório: documentos institucionais, comunitários e macroarquiteturais.
- `docs/`: documentação profunda de engenharia, modelagem, operação e ADRs.

## Estado atual desta publicação

Esta entrega corresponde ao primeiro pacote incremental da Fase 0 e estabelece os documentos basilares do projeto, com foco em contexto, visão, arquitetura macro, contribuição, segurança, roadmap e governança técnica.
