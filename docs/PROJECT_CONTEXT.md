# Contexto do Projeto OpenNetManager

## Problema de negócio

Ambientes de rede frequentemente combinam equipamentos de diferentes fabricantes, interfaces administrativas distintas e baixo grau de padronização no acesso a informações operacionais. Isso aumenta custo de operação, dificulta inventário confiável, fragmenta visibilidade e obriga equipes a depender de acesso manual por CLI para obter estado atual de dispositivos, interfaces, clientes conectados e eventos relevantes.

O OpenNetManager nasce para reduzir essa fragmentação por meio de uma plataforma Open Source com abstrações reutilizáveis de coleta, parsing, persistência e visualização. A premissa central é que o primeiro suporte concreto, AP130 via SSH, não deve contaminar a arquitetura com decisões específicas de fabricante.

## Contexto técnico

A solução será construída com Python 3.13 e Django 5.2, usando um monólito modular orientado a serviços, repositórios, drivers e parsers.[web:1][web:3] Django 5.2 é uma release LTS com suporte de longo prazo, o que a torna apropriada para uma base Open Source que precisa de previsibilidade de manutenção.[web:1]

A compatibilidade oficial do Django 5.2 com Python 3.13 reforça a aderência da stack definida para a Fase 0.[web:1] Python 3.13 também traz melhorias modernas em tipagem, experiência de desenvolvimento e evolução de performance da série, o que beneficia um projeto intensivo em integração e manutenção.[web:3]

## Escopo da Fase 0

A Fase 0 não é uma fase de entrega de produto completo para produção. Trata-se da fase de engenharia fundacional cujo objetivo é eliminar ambiguidades de implementação e consolidar decisões estruturais antes da construção das features iniciais.

Esta fase abrange:

- visão do produto;
- requisitos funcionais e não funcionais;
- arquitetura e ADRs;
- modelagem de domínio e banco;
- diretrizes de API;
- diretrizes de código e qualidade;
- estratégia de testes;
- segurança, deployment, Docker e CI/CD;
- monitoramento, logging, cache, scheduler e desempenho;
- governança de contribuição Open Source.

## Problemas que o sistema deve resolver

1. Centralizar inventário de dispositivos suportados.
2. Armazenar credenciais de forma segura e rastreável.
3. Executar coleta de dados via SSH de forma controlada.
4. Normalizar saídas textuais heterogêneas em objetos de domínio consistentes.
5. Persistir snapshots históricos para auditoria e comparação.
6. Expor dados operacionais via dashboard e API.
7. Permitir expansão para novos fabricantes sem refatoração estrutural do núcleo.

## Premissas de produto

- O produto será Open Source e precisa ser inteligível para contribuidores externos.
- O primeiro vendor suportado é um piloto técnico, não a modelagem definitiva do domínio.
- O dashboard é importante, mas não define o núcleo da solução.
- A persistência precisa funcionar com SQLite em desenvolvimento e PostgreSQL em produção.
- Redis é planejado como evolução futura, não dependência da Fase 0.
- Toda documentação deve ser suficiente para implementação por equipe senior sem contato adicional com o arquiteto.

## Restrições de negócio e engenharia

### Restrições de engenharia

- Python 3.13 é obrigatório como baseline da implementação.[web:3]
- Django 5.2 é obrigatório como framework central.[web:1][web:12]
- SSH é o mecanismo inicial de comunicação com dispositivos.
- O design da aplicação deve permanecer server-driven na Fase 0.
- SQLite e PostgreSQL devem ser ambos suportados.

### Restrições arquiteturais

- Arquitetura em camadas explícitas.
- Repositórios obrigatórios para persistência.
- Serviços obrigatórios para orquestração.
- Drivers obrigatórios para integração com vendors.
- Parsers obrigatórios para interpretação de CLI.
- Views sem acesso direto ao ORM.
- Parsers sem responsabilidades de transporte.

## Stakeholders

| Stakeholder | Interesse principal | Preocupações |
|---|---|---|
| Administrador de rede | Operar inventário, coletas e troubleshooting | Segurança, confiabilidade, clareza do dashboard |
| Operador técnico | Consultar estado e histórico | Usabilidade, velocidade, precisão dos dados |
| Desenvolvedor backend | Implementar domínio e integrações | Acoplamento, testabilidade, contratos claros |
| Contribuidor Open Source | Evoluir o projeto | Onboarding, documentação, padrões consistentes |
| Maintainer | Sustentabilidade do repositório | Qualidade, governança, segurança, CI |

## Critérios de sucesso da Fase 0

A Fase 0 será bem-sucedida quando:

- a equipe puder implementar o sistema sem depender de alinhamentos ad hoc;
- as responsabilidades de cada camada estiverem inequivocamente documentadas;
- os modelos de domínio estiverem definidos com clareza suficiente para banco, serviços e API;
- a estratégia de testes, segurança e qualidade estiver alinhada ao ciclo de contribuição Open Source;
- existir um caminho documentado de evolução para múltiplos vendors, cache e scheduler.

## Riscos principais

### 1. Acoplamento acidental ao AP130

Este é o maior risco técnico inicial. Se comandos, parsers ou semânticas específicas vazarem para serviços, repositórios ou views, a expansão multi-vendor ficará cara e instável.

### 2. Excesso de abstração prematura

Embora o sistema precise nascer desacoplado, abstrações excessivamente genéricas e não justificadas podem tornar a base opaca e lenta para evoluir. O equilíbrio correto é abstrair onde a variação futura é previsível e manter concreto onde o domínio ainda não provou necessidade adicional.

### 3. Segurança de credenciais

Como o sistema manipulará acesso privilegiado a dispositivos, falhas em criptografia, masking, auditoria ou autorização podem comprometer ambientes reais. Por isso segurança é tratada como parte central da arquitetura, não como requisito periférico.

### 4. Complexidade de parsing textual

CLI de dispositivos tende a mudar por firmware, idioma, flags de comando ou pequenas variações. Parsers frágeis geram dados incorretos silenciosamente; portanto o domínio deve preferir parsing explicitamente validado e testes com fixtures reais.
