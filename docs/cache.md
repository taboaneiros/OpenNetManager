# Cache

## Objetivo

Definir a postura arquitetural do OpenNetManager em relação a cache e orientar sua adoção futura sem introduzir acoplamento prematuro.

## Princípio central

Cache é uma otimização, não a fonte da verdade. O sistema deve funcionar corretamente sem cache na Fase 0.

## Motivações futuras para cache

- acelerar leituras repetitivas do dashboard;
- reduzir custo de agregações frequentes;
- armazenar resultados transitórios de baixo risco;
- apoiar coordenação leve com Redis em fases posteriores.

## O que não deve ser cacheado inicialmente

- segredos de credenciais em formato utilizável;
- estados cuja invalidação ainda não esteja claramente definida;
- resultados de coleta que precisem de forte consistência sem estratégia robusta.

## Estratégia da Fase 0

- criar abstrações e pontos de extensão mínimos quando necessário;
- evitar dependência operacional obrigatória de Redis;
- documentar candidatos a cache, não implementá-los prematuramente.

## Trade-offs

### Cache cedo versus simplicidade

Cache prematuro pode esconder consultas ruins, introduzir inconsistência e dificultar debugging. Na Fase 0, é melhor entender o perfil real de acesso antes de otimizar com uma camada extra.
