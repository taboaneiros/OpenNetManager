# Estratégia de Testes

## Objetivo

Definir a estratégia completa de testes do OpenNetManager para garantir correção funcional, preservação arquitetural, confiança em refatorações e segurança das integrações com dispositivos.

## Princípios

- testes devem refletir a arquitetura;
- cada camada deve ser testada no nível de isolamento apropriado;
- parsers devem ser validados com fixtures reais de CLI;
- integração com SSH real deve ser limitada e controlada;
- regressões arquiteturais e semânticas devem ser detectadas cedo;
- qualidade de testes é mais importante que volume cego de casos.

## Pirâmide de testes

### 1. Testes unitários

Cobrem funções, classes e comportamentos isolados, com forte uso de mocks e fixtures. Devem compor a maior parte da suíte.

### 2. Testes de integração

Validam interação entre camadas internas e banco de dados, inclusive repositories, services com persistência real e wiring de components.

### 3. Testes E2E

Validam fluxos críticos completos via HTTP/UI/API, com foco em autenticação, cadastro, coleta manual e visualização de resultados.

## Cobertura por camada

### Parsers

Parsers exigem cobertura profunda porque são uma das áreas mais frágeis do sistema.

Devem existir testes para:

- parsing feliz com fixture real;
- whitespace e pequenas variações de formatação;
- saída incompleta;
- campos inesperados;
- firmware divergente quando conhecido;
- sinalização correta de erro semântico.

### Drivers

Drivers devem ser testados com:

- mocks do SSH gateway;
- validação de seleção de comandos;
- roteamento correto para parsers;
- tratamento de capability não suportada;
- conversão de falhas de SSH para exceções do projeto.

### Services

Services devem validar:

- orquestração correta;
- resolução de driver;
- persistência esperada;
- transição de status do snapshot;
- emissão de eventos;
- comportamento diante de falha parcial.

### Repositories

Repositories devem usar testes de integração com banco, não apenas mocks. O objetivo é validar queries, constraints, transações, filtros, paginação e ordenação real.

### Views e API

Devem ser testadas autenticação, autorização, validação, mapeamento de serviço para resposta, templates ou payloads e códigos HTTP.

## Fixtures

### Fixtures de domínio

Devem existir factories/fixtures para:

- usuários com perfis distintos;
- dispositivos ativos e inativos;
- credenciais válidas e inválidas;
- snapshots em estados diferentes;
- collection jobs habilitados e desabilitados.

### Fixtures de CLI

Fixtures reais de saídas SSH/CLI devem ser armazenadas por vendor, plataforma, comando e variação conhecida. Isso é crucial para reproduzibilidade dos parsers.

Estrutura sugerida:

```text
tests/fixtures/
├── ap130/
│   ├── system_info/
│   │   ├── happy_path.txt
│   │   ├── missing_field.txt
│   │   └── malformed.txt
│   ├── interfaces/
│   └── clients/
```

## Mocks e monkeypatch

`pytest` fornece fixtures e mecanismos como `monkeypatch` para substituir atributos, ambiente e comportamentos dependentes de rede ou sistema externo, o que é especialmente útil para testes de SSH, configuração e isolamento de efeitos colaterais.[web:17][web:19]

Usos recomendados:

- substituir gateway SSH;
- mockar resolução de driver;
- controlar variáveis de ambiente;
- evitar chamadas reais de rede;
- simular timeouts e erros de autenticação.

## Cobertura mínima recomendada

- services centrais: alta cobertura;
- parsers: cobertura muito alta;
- drivers: alta cobertura;
- repositories: cobertura por integração das queries críticas;
- views/API: cobertura dos fluxos sensíveis.

Meta inicial recomendada: 80% nas áreas críticas, com tolerância menor para parser e segurança.

## Estratégia de banco para testes

- testes rápidos locais podem usar SQLite quando apropriado;
- repositories e cenários críticos devem rodar também contra PostgreSQL em CI;
- diferenças entre engines não podem ser ignoradas em validação final.

## Testes E2E prioritários

1. Login e logout.
2. Cadastro de dispositivo.
3. Cadastro e associação de credencial.
4. Teste de conectividade SSH com mock controlado.
5. Coleta manual de snapshot.
6. Visualização de snapshot e histórico.
7. Restrições de autorização.

## Regressões arquiteturais

Além de testes funcionais, é recomendável criar verificações que impeçam:

- import indevido entre camadas;
- uso do ORM em views;
- uso de SSH fora da camada apropriada;
- parser importando componentes de transporte.

## Trade-offs

### Mock intenso versus confiança real

Mocks aceleram e isolam testes, mas podem mascarar integração quebrada. Por isso o projeto exige combinação de unitários e integrações reais com banco e fluxos completos controlados.

### E2E amplo versus custo de manutenção

E2E em excesso torna a suíte lenta e frágil. O foco deve estar em poucos fluxos de alto valor, deixando detalhes combinatórios para unitários e integrações.
