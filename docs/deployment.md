# Deployment

## Objetivo

Definir a estratégia de deployment do OpenNetManager para ambientes de desenvolvimento, homologação e produção, preservando segurança, previsibilidade e simplicidade operacional.

## Filosofia de deploy

A Fase 0 adota um modelo de deploy simples e controlado, adequado a um monólito modular Django. A prioridade é reprodutibilidade e segurança básica, não alta disponibilidade completa desde o primeiro ciclo.

## Ambientes previstos

- local development;
- CI/test;
- staging ou homologação;
- production.

## Requisitos por ambiente

### Desenvolvimento local

- setup simples;
- SQLite permitido;
- `DEBUG=True` apenas localmente;
- variáveis de ambiente locais;
- dados fictícios ou controlados.

### CI/Test

- execução automatizada;
- `DEBUG=False` preferencialmente em checks próximos de produção;
- PostgreSQL nos testes principais de integração;
- sem dependência de SSH real.

### Staging

- configuração próxima da produção;
- PostgreSQL obrigatório;
- `DEBUG=False`;
- secrets reais de staging segregados;
- smoke tests pós-deploy.

### Produção

- `DEBUG=False` obrigatório;
- HTTPS obrigatório;
- PostgreSQL obrigatório;
- segredos por ambiente;
- logs estruturados;
- política explícita de backup e rollback.

## Checklist de segurança de deploy

O Django mantém um checklist oficial para produção e recomenda o uso de `manage.py check --deploy` para validar itens como `DEBUG`, `ALLOWED_HOSTS`, cookies seguros e outras configurações sensíveis.[web:20] O OpenNetManager deve incorporar esse checklist como gate obrigatório do processo de release.[web:20]

## Estratégia de rollout

### Inicial

- deploy manual assistido ou pipeline controlado;
- migrações executadas com supervisão;
- validação de health endpoint e login básico;
- verificação de acesso ao banco.

### Evolução futura

- publicação automatizada de imagem;
- deploy em staging por tag/branch;
- promoção controlada para produção;
- smoke tests e rollback assistido.

## Migrações

Migrações devem ser:

- revisadas em PR;
- executadas de forma determinística;
- compatíveis com rollback quando possível;
- acompanhadas de plano de contingência quando destrutivas.

## Variáveis de ambiente mínimas

- secret key da aplicação;
- modo de ambiente;
- parâmetros de banco;
- política de segurança de cookies;
- chaves e parâmetros de criptografia de credenciais;
- opções de logging;
- feature flags futuras quando aplicável.

## Trade-offs

### Deploy simples versus orquestração avançada

A Fase 0 não precisa nascer com Kubernetes, service mesh ou topologias sofisticadas. Essa ausência reduz complexidade operacional e facilita adoção. O custo é menor elasticidade automática, o que é aceitável no estágio atual.

### SQLite local versus fidelidade total de ambiente

Permitir SQLite local reduz barreira de entrada. O risco é divergência de comportamento em relação ao PostgreSQL, mitigada por testes de integração em CI e staging.
