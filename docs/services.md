# Services

## Objetivo

Definir o service layer do OpenNetManager como a principal camada de orquestração de casos de uso, regras de negócio e coordenação transacional.

## Papel do service layer

Services existem para impedir que lógica de negócio se disperse por views, serializers, signal handlers, repositories e drivers. Eles recebem intenção de negócio, coordenam dependências e devolvem resultados coerentes para a apresentação ou API.

## Responsabilidades

- orquestrar casos de uso;
- aplicar regras de negócio;
- validar estado e elegibilidade;
- coordenar repositories e drivers;
- controlar transações;
- registrar eventos e logs relevantes;
- converter falhas técnicas em semântica de aplicação quando necessário.

## Services iniciais sugeridos

- `AuthService` quando houver regras além do padrão Django;
- `DeviceService`;
- `CredentialService`;
- `SnapshotService`;
- `EventService`;
- `CollectionJobService`;
- `DashboardService`;
- `HealthService`.

## Exemplo de responsabilidades por serviço

### DeviceService

- criar e atualizar dispositivos;
- validar consistência de vendor/plataforma;
- ativar/desativar device;
- compor detalhes para a UI.

### CredentialService

- criar credencial;
- rotacionar segredo;
- associar a dispositivos;
- validar elegibilidade e estado.

### SnapshotService

- testar conectividade;
- disparar coleta manual;
- resolver driver;
- persistir snapshot e objetos relacionados;
- classificar sucesso, parcial ou falha.

### CollectionJobService

- criar e alterar jobs;
- habilitar/desabilitar;
- preparar integração futura com scheduler.

## Dependency Injection

A documentação do projeto exige injeção de dependências explícita nas fronteiras centrais. Em termos práticos, isso significa que services não devem criar internamente suas dependências críticas sem necessidade. Mesmo em um monólito Django, é desejável poder substituir driver registry, gateway SSH e repositories para testes e composição controlada.

## Trade-offs

### Service layer formal versus lógica em views/serializers

A abordagem formal exige mais disciplina e algum boilerplate. Em compensação, deixa a aplicação menos acoplada a HTTP e mais reutilizável por dashboard, API, scheduler e automações futuras.
