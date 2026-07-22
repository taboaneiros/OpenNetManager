# Dashboard

## Objetivo

Definir o papel do dashboard do OpenNetManager e suas fronteiras técnicas e funcionais.

## Papel do dashboard

O dashboard é a superfície de consulta e navegação operacional da plataforma. Ele não é a camada de integração com dispositivos, nem o lugar onde lógica de coleta deve ser implementada.

## Regra arquitetural central

Dashboard nunca acessa SSH diretamente. Toda informação apresentada deve vir de dados persistidos e serviços de aplicação. Essa regra é fundamental para previsibilidade, desempenho e separação de responsabilidades.

## Conteúdo inicial sugerido

- total de dispositivos cadastrados;
- total por vendor/plataforma;
- dispositivos ativos versus inativos;
- últimos snapshots executados;
- falhas recentes de coleta;
- eventos operacionais recentes.

## Objetivos de UX

- permitir leitura rápida do estado geral;
- destacar falhas e itens que exigem ação;
- reduzir cliques para chegar ao detalhe do dispositivo;
- não confundir dados históricos com estado “ao vivo” sem indicação explícita.

## Trade-offs

### Dashboard rico em tempo real versus dashboard persistido

Um dashboard em tempo real exigiria polling agressivo, filas e acoplamento maior com infraestrutura. Um dashboard baseado em estado persistido é mais simples, previsível e coerente com o estágio do produto.
