# Arquitetura Técnica Atualizada

## Estilo

O OpenNetManager utiliza um monólito modular com Clean Architecture como referência, DDD Lite, Repository Pattern, Service Layer, Driver Pattern, Parser Pattern e Dependency Injection nas fronteiras centrais.

## Fluxo de leitura

```text
View/API
→ Service
→ Repository
→ Driver Registry
→ Driver
→ SSH Gateway
→ Parser
→ Domain Objects
→ Repository
→ View/API
```

## Fluxo de alteração

```text
View/API
→ Service
→ Authorization
→ Capability Check
→ Validation/Diff
→ Confirmation
→ Driver
→ SSH Gateway
→ Parser/Verification
→ Repository
→ Audit Event
→ View/API
```

## Camadas

### Presentation

Views, templates, forms, serializers e endpoints. Converte entrada em comandos de aplicação e não contém regra de vendor, ORM direto ou SSH.

### Application

Services que coordenam autorização, capabilities, validação, confirmação, execução, reconexão, transações, persistência e auditoria.

### Domain

Entidades, value objects, enums, contratos, estados de operação e regras estáveis, sem dependência de Django ou Paramiko.

### Infrastructure

ORM, repositories concretos, SSH, drivers, parsers, logs técnicos e adaptadores externos.

## Drivers e capabilities

O registry resolve driver por vendor, plataforma, modelo e eventualmente firmware. O driver deve fornecer capabilities e implementar apenas operações realmente suportadas.

```python
class DeviceCapabilities:
    read_system_info: bool
    read_interfaces: bool
    read_clients: bool
    read_ssids: bool
    read_radios: bool
    read_logs: bool
    read_full_config: bool
    configure_ssid: bool
    configure_radio: bool
    configure_network: bool
    configure_vlan: bool
    reboot: bool
    reset_config: bool
    factory_reset: bool
    export_config: bool
    import_config: bool
    ping: bool
    traceroute: bool
    disconnect_client: bool
    cli_session: bool
```

## Operações de configuração

Configuração deve ser estruturada, nunca implementada como texto livre no service. O driver traduz o modelo canônico para comandos, menus e etapas específicas do vendor.

Antes da aplicação:

1. carregar configuração atual;
2. validar schema e capability;
3. construir diff;
4. apresentar preview;
5. confirmar;
6. criar backup quando possível;
7. executar;
8. reconectar;
9. verificar estado final;
10. persistir snapshot e auditoria.

## Reconexão

Mudanças de IP, DHCP ou VLAN podem interromper SSH. O service deve persistir estado de execução, tentar reconexão conforme política, validar o novo endpoint e somente então concluir a operação.

## Diagnóstico e CLI

Ping e traceroute devem identificar origem servidor/device. Logs e configuração completa devem ser protegidos. CLI inicia como sessão controlada com comandos permitidos pelo driver, timeout e auditoria.

## Dashboard

O dashboard usa services e repositories sobre dados persistidos. Nunca abre SSH. Dados “atuais” devem indicar timestamp da última coleta.

## Observabilidade

Operações devem gerar logs estruturados e eventos com:

- actor;
- device;
- capability;
- operation;
- status;
- duration;
- error category;
- correlation id.

## Evolução

Redis, scheduler persistido, execução assíncrona e plugins permanecem desacoplados e posteriores à estabilização dos contratos de operação.
