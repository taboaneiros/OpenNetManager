# Roadmap do OpenNetManager

## Objetivo do roadmap

Este roadmap define a evolução planejada do OpenNetManager a partir da Fase 0, priorizando maturidade arquitetural antes de escala funcional. Ele não é um compromisso rígido de datas, mas uma referência estratégica para ordenação de entregas, gestão de escopo e comunicação com a comunidade.

## Princípios de priorização

- Primeiro estabilizar fundamentos.
- Depois entregar valor operacional mínimo.
- Só então expandir vendors, automação e escala.
- Nunca trocar velocidade de curto prazo por erosão da arquitetura multi-vendor.

## Fase 0 — Fundação documental e arquitetural

### Objetivos

- Consolidar contexto, visão e requisitos.
- Definir arquitetura, camadas, contratos e ADRs.
- Modelar domínio, banco e estratégia de testes.
- Estabelecer segurança, qualidade, CI/CD e governança Open Source.

### Entregáveis-chave

- documentação completa de engenharia;
- diretrizes de contribuição;
- decisões arquiteturais registradas;
- estratégia de implementação pronta para equipe senior.

### Critério de saída

A equipe consegue iniciar implementação sem ambiguidade estrutural relevante.

## Fase 1 — Núcleo funcional inicial

### Objetivos

- Implementar autenticação e autorização básicas.
- Implementar cadastro de dispositivos e credenciais.
- Implementar driver AP130 via SSH.
- Implementar parsers iniciais para informações de sistema e interfaces.
- Implementar snapshots manuais e dashboard básico.
- Publicar API REST mínima versionada.

### Resultado esperado

A plataforma já oferece gerenciamento inicial de inventário e coleta básica funcional para AP130, preservando a arquitetura multi-vendor.

### Riscos aceitos

- cobertura funcional ainda limitada;
- UX operacional ainda simples;
- ausência de scheduler avançado;
- ausência de cache distribuído.

## Fase 2 — Consolidação operacional

### Objetivos

- Adicionar coleta de clientes e eventos suportados.
- Implementar histórico e comparação de snapshots.
- Expandir testes de integração e E2E.
- Melhorar dashboard, filtros, paginação e rastreabilidade.
- Endurecer políticas de segurança e auditoria.

### Resultado esperado

O produto passa de protótipo funcional para ferramenta operacional inicial confiável.

## Fase 3 — Escalabilidade controlada

### Objetivos

- Introduzir scheduler persistido.
- Planejar ou introduzir Redis para cache e coordenação futura.
- Evoluir execução assíncrona de coletas.
- Implementar limites de concorrência e backoff por dispositivo.
- Aumentar observabilidade operacional.

### Resultado esperado

O sistema passa a suportar volume maior de coletas, melhor previsibilidade operacional e menor latência percebida.

## Fase 4 — Expansão multi-vendor

### Objetivos

- Adicionar novos drivers e parsers para Cisco, Huawei, Juniper, Mikrotik, Aruba e Ubiquiti.
- Criar matriz de capabilities por fabricante/plataforma.
- Expandir modelo de comandos suportados por feature.
- Validar o desenho arquitetural sob diversidade real de vendors.

### Resultado esperado

O OpenNetManager se consolida como plataforma multi-vendor, não apenas como integração AP130.

## Fase 5 — Ecossistema e extensibilidade

### Objetivos

- Melhorar API pública e documentação OpenAPI.
- Explorar mecanismos de plugin/extensão.
- Adicionar webhooks, exportações e integrações externas.
- Fortalecer governança de releases e comunidade.

### Resultado esperado

O projeto amadurece como produto Open Source com potencial de ecossistema.

## Itens explicitamente fora da Fase 0

- suporte multi-vendor implementado em código;
- filas distribuídas completas;
- auto-discovery em rede;
- execução massiva em paralelo;
- RBAC avançado granular por objeto;
- alta disponibilidade nativa;
- suporte SNMP/NETCONF/gNMI na primeira iteração.

## Critérios de priorização contínua

Quando houver disputa de backlog, a ordem de preferência é:

1. Segurança.
2. Correção dos dados.
3. Preservação da arquitetura.
4. Testabilidade e observabilidade.
5. Valor operacional para o usuário.
6. Conveniência de UX.
7. Otimizações prematuras.
