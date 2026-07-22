# Exceções

## Objetivo

Definir a estratégia de tratamento e modelagem de exceções do OpenNetManager para garantir previsibilidade de falhas, clareza semântica e mapeamento consistente para UI, API e logs.

## Princípios

- exceções devem comunicar intenção semântica;
- exceções de infraestrutura não devem vazar diretamente à camada de apresentação;
- mensagens ao usuário devem ser seguras e acionáveis;
- detalhes técnicos profundos devem ir para logs, não necessariamente para a resposta final;
- cada camada deve capturar e remapear apenas quando acrescentar contexto útil.

## Hierarquia recomendada

```text
OpenNetManagerError
├── DomainError
│   ├── ValidationError
│   ├── BusinessRuleError
│   ├── UnsupportedCapabilityError
│   └── InvalidStateError
├── SecurityError
│   ├── AuthenticationError
│   ├── AuthorizationError
│   └── CredentialProtectionError
├── InfrastructureError
│   ├── RepositoryError
│   ├── DatabaseError
│   ├── DriverError
│   ├── SSHError
│   │   ├── SSHConnectionError
│   │   ├── SSHAuthenticationError
│   │   └── SSHCommandTimeoutError
│   └── ParserError
│       ├── ParserFormatError
│       ├── ParserSemanticError
│       └── ParserIncompleteDataError
└── ApplicationError
    ├── SnapshotCollectionError
    ├── JobExecutionError
    └── ExternalIntegrationError
```

## Responsabilidade por camada

### View / API

- capturar exceções já semanticamente úteis;
- converter em resposta HTML/JSON adequada;
- nunca expor stack trace ao usuário;
- preservar correlation id para suporte.

### Service

- consolidar falhas de camadas inferiores em exceções de caso de uso quando fizer sentido;
- acrescentar contexto de domínio;
- decidir quando falha parcial ainda permite persistir snapshot parcial.

### Repository

- encapsular exceções de ORM/DB em `RepositoryError` ou subclasses relevantes;
- não vazar detalhes de engine para camadas superiores sem necessidade.

### Driver

- traduzir exceções de SSH/parsing em erros semânticos de coleta quando necessário;
- não mascarar indiscriminadamente a causa raiz.

### Parser

- falhar explicitamente quando o formato não puder ser interpretado com segurança;
- diferenciar ausência esperada de dado, dado parcial e formato inválido.

## Mapeamento sugerido para API

| Exceção | HTTP | Observação |
|---|---|---|
| ValidationError | 400 | Entrada inválida |
| AuthenticationError | 401 | Não autenticado |
| AuthorizationError | 403 | Sem permissão |
| UnsupportedCapabilityError | 422 | Capability não suportada para o device |
| InvalidStateError | 409 | Conflito de estado |
| ResourceNotFound equivalente | 404 | Recurso inexistente |
| SSHAuthenticationError | 502 ou 422 | Conforme política de exposição do erro |
| SSHConnectionError | 502 | Falha em integração externa/dispositivo |
| ParserError | 502 ou 500 | Preferir 502 quando falha vier do sistema externo |
| RepositoryError | 500 | Falha interna persistente |

## Mensagens ao usuário

Mensagens visíveis ao usuário devem:

- ser compreensíveis;
- evitar jargão excessivo quando não ajudar;
- não expor credenciais, queries, stack traces ou detalhes inseguros;
- indicar próxima ação quando possível.

Exemplo adequado: “Não foi possível conectar ao dispositivo com a credencial informada.”

Exemplo inadequado: “Paramiko AuthenticationException in ssh/client.py line 183”.

## Falha parcial de snapshot

Uma coleta pode falhar parcialmente quando, por exemplo:

- `SystemInfo` é coletado com sucesso;
- `Interface` é coletado parcialmente;
- `Client` não é suportado ou falha por parser;
- persistência do snapshot principal ainda é viável.

Nesses casos, o sistema deve preservar status semântico de `partial_success`, registrar eventos e expor o problema com clareza.

## Trade-offs

### Muitas subclasses versus erro genérico único

Uma hierarquia rica aumenta clareza, roteamento de resposta e qualidade de logs, mas exige disciplina. Em um sistema com SSH, parsing e múltiplas fronteiras técnicas, o benefício supera o custo.

### Remapeamento excessivo versus vazamento bruto

Traduzir toda exceção para um erro genérico destrói capacidade diagnóstica. Deixar tudo vazar para cima acopla camadas. O equilíbrio correto é remapear quando a camada consegue enriquecer o contexto ou proteger a fronteira externa.
