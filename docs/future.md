# Evolução Futura

## Objetivo

Registrar direções de evolução arquitetural e funcional já previstas, para que a implementação da Fase 0 não bloqueie capacidades futuras.

## Eixos de evolução

### Multi-vendor real

Após o AP130, o projeto deverá incorporar Cisco, Huawei, Juniper, Mikrotik, Aruba e Ubiquiti por meio de novos drivers, parsers e mapeamentos de capabilities. A regra central é evoluir por adição, não por refatorações que quebrem o núcleo a cada novo vendor.

### Scheduler e execução assíncrona

Jobs persistidos devem evoluir para execução automática com políticas de concorrência, retries, backoff e isolamento por dispositivo. Essa evolução deve manter o request/response web desacoplado da execução operacional longa.

### Redis

Redis é previsto para cache, coordenação leve e possíveis filas auxiliares futuras. A arquitetura atual não deve exigir Redis para funcionar, mas deve evitar acoplamentos que tornem sua adoção posterior dolorosa.

### Observabilidade

No futuro, o projeto deve ampliar métricas, correlação de eventos, health checks, dashboards internos e rastreamento mais fino de execução de coletas.

### Extensibilidade

É desejável evoluir para uma forma de registro extensível de drivers, potencialmente próxima de plugin architecture. Entretanto, isso só deve ser formalizado após o segundo ou terceiro vendor, quando os pontos reais de variação estiverem comprovados.

## Antipadrões a evitar desde já

- regras de vendor espalhadas por services;
- schema de banco fortemente moldado ao AP130;
- UI acoplada a payloads brutos de parser;
- scheduler implementado dentro de views;
- cache antes da definição dos pontos de leitura críticos.
