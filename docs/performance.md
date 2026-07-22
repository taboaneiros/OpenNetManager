# Performance

## Objetivo

Definir diretrizes de desempenho do OpenNetManager para a Fase 0, priorizando previsibilidade e saúde arquitetural em vez de micro-otimizações prematuras.

## Princípios

- não sacrificar correção por velocidade aparente;
- separar desempenho de leitura de desempenho de coleta;
- medir antes de otimizar;
- preferir eliminar gargalos arquiteturais a aplicar hacks localizados.

## Áreas críticas

### Leitura de dashboard e inventário

Consultas frequentes devem ser paginadas, indexadas e baseadas em dados persistidos. Evitar N+1 e consultas redundantes é mais importante que qualquer solução de cache prematura.

### Coleta SSH

A coleta é naturalmente mais lenta do que leitura local e depende de rede, firmware e dispositivo. O objetivo inicial deve ser controlar timeout, concorrência e escopo da operação, não “forçar” performance por risco de instabilidade.

### Parsing

Parsers devem ser eficientes, mas a prioridade é precisão semântica. Processamento de texto simples geralmente não será o maior gargalo; retrabalho por dado incorreto é muito mais caro do que custo computacional marginal.

## Estratégias recomendadas

- índices adequados em snapshots e eventos;
- paginação consistente;
- eager loading criterioso em repositories;
- limites de timeout em SSH;
- eventual cache apenas após observação real de hotspots.

## Trade-offs

### Otimização antecipada versus legibilidade

Em um projeto jovem, otimização prematura tende a obscurecer o código e congelar decisões erradas. A Fase 0 deve privilegiar um desenho claro e mensurável, com pontos evidentes para evolução posterior.
