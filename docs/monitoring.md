# Monitoramento

## Objetivo

Definir a estratégia de monitoramento do OpenNetManager para acompanhar saúde da aplicação, execução de coletas e sinais operacionais relevantes.

## Escopo inicial

A Fase 0 não exige plataforma completa de observabilidade, porém já exige visibilidade mínima suficiente para operação segura:

- health/status da aplicação;
- logs estruturados;
- eventos persistidos relevantes;
- indicadores básicos de falha de coleta.

## O que monitorar

### Saúde da aplicação

- disponibilidade do processo web;
- conectividade com banco;
- resposta do endpoint de health;
- erros internos recorrentes.

### Saúde operacional de coleta

- taxa de sucesso de snapshots;
- taxa de falha por dispositivo;
- timeout de coleta;
- falhas de autenticação SSH;
- falhas de parsing por parser/vendor.

### Saúde de dados

- jobs presos em estado inconsistente;
- snapshots sem entidades relacionadas quando deveriam existir;
- eventos de erro em alta frequência;
- anomalias de crescimento de volume persistido.

## Fontes de sinal

- endpoint de health;
- logging estruturado;
- tabela de eventos;
- banco de dados;
- métricas futuras.

## Métricas recomendadas para evolução

- `snapshot_success_total`
- `snapshot_failure_total`
- `snapshot_duration_ms`
- `ssh_connection_failure_total`
- `parser_failure_total`
- `collection_job_scheduled_total`
- `collection_job_lag_seconds`

## Alertas futuros prioritários

- taxa anormal de falha de coleta;
- falha geral de login ou autenticação;
- indisponibilidade do banco;
- health endpoint degradado;
- crescimento acentuado de timeouts SSH.

## Trade-offs

### Instrumentação mínima versus telemetria pesada

Começar com health, logs e eventos reduz custo e acelera a adoção. O custo é menor granularidade analítica inicial. Isso é aceitável desde que a arquitetura mantenha pontos claros para futura instrumentação métrica.
