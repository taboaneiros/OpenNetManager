# Diretrizes de API

## Objetivo

Definir os princípios de desenho da API REST do OpenNetManager para garantir consistência, previsibilidade, versionamento e segurança.

## Estilo geral

A API será RESTful pragmática, versionada e orientada a recursos. A implementação será baseada em Django REST Framework, aproveitando autenticação, serializers, validação e políticas de permissão do ecossistema.

## Princípios

- versionamento explícito no caminho;
- payloads previsíveis e autoconsistentes;
- mensagens de erro estruturadas;
- separação entre modelos internos e contratos externos;
- autenticação e autorização consistentes;
- ausência de vazamento de dados sensíveis.

## Versionamento

Versão inicial recomendada:

- `/api/v1/`

Mudanças breaking devem gerar nova versão principal de API. Mudanças compatíveis devem evoluir dentro da mesma versão por adição incremental de campos, filtros ou endpoints.

## Recursos iniciais previstos

- `devices`
- `credentials`
- `snapshots`
- `interfaces`
- `clients`
- `events`
- `collection-jobs`
- `health` ou `status`

## Convenções de payload

### Resposta de sucesso de recurso único

```json
{
  "data": {
    "id": "uuid",
    "type": "device",
    "attributes": {}
  },
  "meta": {}
}
```

### Resposta de coleção

```json
{
  "data": [],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total": 100
  }
}
```

### Resposta de erro

```json
{
  "error": {
    "code": "device_not_found",
    "message": "Device not found.",
    "details": {}
  }
}
```

## Códigos HTTP

- `200 OK` para leitura bem-sucedida.
- `201 Created` para criação.
- `202 Accepted` para operações assíncronas futuras.
- `400 Bad Request` para erro de validação sintática/contratual.
- `401 Unauthorized` para ausência de autenticação.
- `403 Forbidden` para falta de permissão.
- `404 Not Found` para recurso inexistente.
- `409 Conflict` para conflitos de estado ou unicidade.
- `422 Unprocessable Entity` quando a regra de negócio justificar distinção semântica.
- `500 Internal Server Error` apenas para falhas não tratadas.

## Segurança de contrato

- nunca expor segredos ou material criptográfico;
- mascarar campos sensíveis em payloads de leitura;
- limitar ações destrutivas por autorização forte;
- registrar operações sensíveis em trilha de auditoria.

## OpenAPI

A especificação OpenAPI formal será documentada em entrega posterior da Fase 0, com endpoints, schemas, exemplos e catálogo de erros. Esta diretriz prepara as decisões fundamentais antes da modelagem detalhada.

## Consistência entre dashboard e API

Dashboard e API devem consumir a mesma camada de serviços. A API não deve implementar regra de negócio divergente apenas por conveniência de endpoint.
