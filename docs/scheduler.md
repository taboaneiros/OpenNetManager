# Scheduler

## Objetivo

Definir a estratégia arquitetural para agendamento de coletas do OpenNetManager, preservando desacoplamento e preparando evolução futura.

## Princípio central

Agendamento é responsabilidade própria do domínio operacional e não deve ficar embutido em views, templates ou callbacks incidentais da UI.

## CollectionJob como base

A entidade `CollectionJob` existe para modelar intenção de coleta futura mesmo antes da entrega completa de um scheduler robusto. Isso permite estabilizar o domínio sem bloquear evolução posterior.

## Responsabilidades do scheduler futuro

- buscar jobs elegíveis;
- respeitar janela de execução;
- disparar services adequados;
- registrar resultado e próxima execução;
- aplicar retry e backoff controlados;
- evitar concorrência indevida sobre o mesmo device.

## Estratégia da Fase 0

- modelar jobs;
- definir contratos de execução;
- desacoplar lógica de agendamento da camada web;
- não tornar Redis obrigatório ainda.

## Trade-offs

### Scheduler simples inicial versus engine completa

Postergar a engine completa evita dependências pesadas prematuras e reduz complexidade. O custo é não ter automação operacional plena no início, compensado por uma modelagem correta desde já.
