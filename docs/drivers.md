# Drivers e Capabilities

## Objetivo

Drivers encapsulam diferenças de vendor, plataforma, modelo, firmware, comandos, menus, sessões e seleção de parsers.

## Contrato

Um driver pode oferecer operações como:

```python
get_capabilities()
collect_snapshot()
read_ssids()
read_radios()
read_logs()
read_full_config()
configure_ssid(profile)
configure_radio(config)
configure_network(config)
configure_vlan(config)
reboot()
reset_config()
factory_reset()
export_config()
import_config(payload)
ping(target)
traceroute(target)
disconnect_client(client)
```

Operações não suportadas devem retornar erro semântico explícito, não sucesso vazio.

## Capabilities

Capabilities podem variar por vendor, plataforma, modelo e firmware. A resolução deve ser centralizada no registry/factory.

## Responsabilidades do driver

- selecionar comandos permitidos;
- abrir ou utilizar sessão pelo SSH gateway;
- executar menus e sequências específicas;
- escolher parser;
- devolver dados normalizados ao service;
- preservar raw output permitido;
- classificar capability ausente;
- executar verificação específica do device.

## O que o driver não faz

- não implementa autorização;
- não decide se o usuário pode executar uma operação;
- não persiste dados;
- não renderiza UI;
- não contém regra geral de negócio;
- não recebe comando arbitrário sem validação.

## AP130 Extreme Networks

O AP130 deve encapsular no driver toda complexidade de CLI, menus, prompts, confirmações, sequência de configuração e reconexão. Services devem trabalhar com operações de alto nível como `configure_ssid`, `configure_radio` e `reboot`, sem conhecer comandos específicos.

Cada operação precisa de fixtures reais, testes de parser, teste de sucesso, falha parcial, timeout e alteração de firmware quando conhecida.

## GWN7600 Grandstream

O GWN7600 deve utilizar driver e parsers próprios para dados de sistema, clientes, rádios, interfaces e operações suportadas. Capacidades não expostas pelo dispositivo devem permanecer explicitamente desabilitadas.

## Fixtures

Fixtures devem ser organizadas por:

```text
tests/fixtures/<vendor>/<platform>/<command>/<variation>.txt
```

Exemplos de variação:

- happy path;
- campo ausente;
- saída incompleta;
- firmware divergente;
- timeout;
- erro de permissão;
- operação parcialmente aplicada.

## Verificação pós-operação

Após configuração ou manutenção, o driver deve fornecer dados suficientes para o service validar estado final, conectividade e resultado real.
