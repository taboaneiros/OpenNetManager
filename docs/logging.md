# Logging

## Objetivo

Definir a estratégia de logging do OpenNetManager para suportar diagnóstico técnico, auditoria mínima, troubleshooting operacional e evolução futura para observabilidade mais madura.

## Princípios

- logs devem ser estruturados e consistentes;
- logs devem ser úteis para investigação sem expor segredos;
- eventos de negócio e eventos técnicos devem ser distinguíveis;
- toda operação crítica deve ser correlacionável;
- logging não substitui a modelagem de `Event`, mas a complementa.

## Papel do logging na arquitetura

Logging é responsabilidade transversal, porém seu uso deve respeitar camadas:

- Views registram contexto de entrada, autorização e resultado de alto nível.
- Services registram início/fim de casos de uso, decisões relevantes e falhas categorizadas.
- Repositories registram falhas de persistência e consultas críticas quando necessário.
- Drivers registram escopo da coleta, comandos lógicos executados e falhas por capability.
- SSH registra métricas técnicas de conexão e execução, nunca segredo.
- Parsers registram sucesso, warning semântico e falhas de parsing.

## Formato recomendado

Adotar logging estruturado em JSON para produção e formato legível para desenvolvimento local. Campos recomendados:

- timestamp
- level
- logger
- message
- correlation_id
- request_id
- user_id quando aplicável
- device_id quando aplicável
- snapshot_id quando aplicável
- job_id quando aplicável
- vendor
- platform
- event_code
- exception_class
- duration_ms

## Níveis de log

### DEBUG

Usado apenas para desenvolvimento e troubleshooting controlado. Pode incluir detalhes adicionais de fluxo, porém nunca segredos.

### INFO

Usado para eventos normais importantes, como login bem-sucedido, criação de dispositivo, início e conclusão de coleta, job criado e credencial rotacionada.

### WARNING

Usado para situações anormais recuperáveis, como capability não suportada, parsing parcial, timeout controlado, dispositivo desabilitado para coleta ou configuração inconsistente não destrutiva.

### ERROR

Usado para falhas que impedem a conclusão correta de uma operação, como falha de persistência, autenticação SSH rejeitada, comando inválido no driver ou exceção de parser não recuperável.

### CRITICAL

Reservado para falhas sistêmicas graves, indisponibilidade ampla, corrupção potencial de dados ou condição de segurança relevante.

## Segredos e redaction

Nunca registrar:

- senha;
- chave privada;
- passphrase;
- token de sessão;
- conteúdo descriptografado de segredo;
- payload que inclua material secreto.

Redaction deve ser ativa e centralizada, não opcional. A aplicação deve assumir que qualquer string operacional pode acabar em log se não houver filtro apropriado.

## Correlação

Toda requisição HTTP e toda execução de coleta devem carregar identificadores de correlação. Isso permite reconstruir o caminho entre request, serviço, driver, SSH, parser e persistência.

## Taxonomia sugerida de event_code

- `auth.login.success`
- `auth.login.failed`
- `device.create.success`
- `device.update.success`
- `credential.rotate.success`
- `snapshot.collect.started`
- `snapshot.collect.succeeded`
- `snapshot.collect.partial`
- `snapshot.collect.failed`
- `ssh.connect.failed`
- `ssh.command.timeout`
- `parser.system_info.failed`
- `repository.snapshot.save.failed`

## Relação entre log e Event

Nem todo log vira `Event`, e nem todo `Event` precisa ser emitido em todos os sinks de log da mesma maneira. `Event` é dado de domínio/auditoria persistível; log é trilha operacional de diagnóstico. Misturar ambos sem critério gera ruído ou duplicidade problemática.

## Configuração por ambiente

### Desenvolvimento

- nível default: DEBUG ou INFO;
- saída legível em console;
- stack traces completos localmente;
- dados sensíveis ainda mascarados.

### Teste/CI

- nível default: INFO;
- logs suficientes para reproduzir falhas de teste;
- opção de aumentar verbosidade sob demanda.

### Produção

- nível default: INFO ou WARNING por logger;
- JSON estruturado;
- rotação/control de volume;
- integração futura com agregador central.

## Trade-offs

### Logging detalhado versus custo de ruído

Mais logs ajudam no troubleshooting, mas excesso degrada sinal, aumenta custo operacional e eleva risco de vazamento acidental. A estratégia correta é registrar decisões e falhas relevantes, não cada microetapa sem valor investigativo.

### Estruturado versus texto livre

Texto livre é mais rápido de escrever, mas pior para busca, correlação e observabilidade futura. JSON estruturado exige mais disciplina inicial e entrega melhor capacidade operacional no médio prazo.
