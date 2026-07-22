# UI

## Objetivo

Definir diretrizes da interface do OpenNetManager para a Fase 0, com foco em clareza operacional, previsibilidade e baixo acoplamento com a lógica de backend.

## Estratégia de interface

A UI inicial será server-driven com Django Templates, Bootstrap 5 e HTMX. Essa abordagem favorece simplicidade de implementação, onboarding mais rápido e menor duplicação de lógica entre frontend e backend.

## Justificativa arquitetural

HTMX permite interações incrementais sem exigir um SPA completo, enquanto Bootstrap 5 acelera consistência visual e ergonomia administrativa. O trade-off é menor flexibilidade para interações extremamente ricas no cliente, mas esse custo é aceitável e desejável na fase de fundação.

## Princípios de UI

- telas operacionais devem ser objetivas;
- feedback de sucesso e erro deve ser claro;
- a UI não deve conter regra de negócio profunda;
- dados exibidos devem vir de serviços e view models adequados;
- segredos devem ser mascarados por padrão.

## Componentes principais previstos

- login;
- dashboard;
- lista e detalhe de dispositivos;
- cadastro e edição de credenciais;
- histórico de snapshots;
- visualização de eventos;
- gestão de jobs de coleta.

## Acessibilidade e ergonomia

Mesmo em uma UI administrativa, acessibilidade é requisito de qualidade. Formulários devem ter labels claros, mensagens de erro explícitas e hierarquia visual previsível.

## Trade-offs

### UI server-driven versus frontend SPA

A UI server-driven reduz duplicação de contratos, centraliza regras na aplicação Django e acelera a entrega de valor. Em troca, perde alguma liberdade de estado client-side avançado. Para este projeto e fase, a troca é favorável.
