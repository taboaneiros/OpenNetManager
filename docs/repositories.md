# Repositórios

## Objetivo

Definir responsabilidades, limites e contratos da camada de repositórios do OpenNetManager.

## Papel do repository

Repository é a fronteira de persistência do domínio de aplicação. Seu objetivo é encapsular leitura, escrita, filtros, ordenação, paginação, carregamento relacionado e detalhes de ORM necessários aos casos de uso.

## Regras mandatórias

- views não acessam ORM diretamente;
- services preferem repositories em vez de querysets brutos;
- drivers e parsers não acessam repositories;
- repository não deve conter regra de UI nem integração remota.

## Tipos iniciais sugeridos

- `DeviceRepository`
- `CredentialRepository`
- `SnapshotRepository`
- `EventRepository`
- `CollectionJobRepository`

## Responsabilidades comuns

- obter entidades por identificador;
- aplicar filtros de consulta;
- persistir criação e atualização;
- lidar com paginação e ordenação;
- encapsular eager loading apropriado;
- mapear erros de infraestrutura para exceções do projeto.

## Design guidelines

### Granularidade

Repositories devem ser específicos o bastante para o domínio e não apenas wrappers mecânicos de `Model.objects`. Se um repository existir, ele deve agregar valor em consistência, legibilidade e encapsulamento.

### Coesão

Cada repository deve concentrar operações da entidade ou agregado correspondente. Consultas compostas podem exigir query services específicos quando ficarem grandes demais para um único repository.

### Transações

O controle transacional principal deve ser orquestrado no service layer, não escondido arbitrariamente dentro de repositories, exceto em operações locais claramente encapsuladas.

## Trade-offs

### Repository formal versus uso direto do ORM

Uso direto do ORM parece mais idiomático em projetos Django pequenos, mas se torna difícil de sustentar quando múltiplos fluxos de coleta, histórico, filtros e regras de autorização crescem em paralelo. O repository formal melhora disciplina e desacoplamento ao custo de mais uma camada.
