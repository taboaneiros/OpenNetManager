# Services Atualizados

## Papel

Services coordenam casos de uso, regras de negócio, autorização, capabilities, validação, transações, estados de operação, persistência e auditoria.

## Services

### DeviceService

Cadastro, atualização, ativação, desativação e composição de detalhes do dispositivo.

### CredentialService

Criação, rotação, associação, validação e proteção de credenciais.

### SnapshotService

Teste de conectividade, coleta manual, resolução de driver, persistência e classificação do snapshot.

### WifiConfigurationService

Preview, diff, validação, confirmação e aplicação de SSID e rádio.

### NetworkConfigurationService

DHCP, IP fixo, gateway, DNS, VLAN e reconexão após alteração.

### ConfigurationService

Leitura de configuração, exportação versionada, validação e importação com backup.

### MaintenanceService

Reboot, reset de serviço, reset de configuração e factory reset protegido.

### DiagnosticService

Ping, traceroute, logs, configuração completa e CLI controlada.

### ClientOperationService

Desautenticação temporária e futuras ações sobre clientes.

### DashboardMetricsService

Agregação de dados persistidos para cards, rankings, gráficos e alertas operacionais.

### AuditService

Registro imutável de ações sensíveis, ator, alvo, capability, resultado e correlação.

## Fluxo comum

1. Receber intenção de aplicação.
2. Validar usuário e autorização.
3. Carregar device e credencial pelo repository.
4. Resolver driver.
5. Verificar capability.
6. Validar entrada e estado.
7. Construir diff quando alteração.
8. Solicitar ou verificar confirmação.
9. Executar driver.
10. Controlar reconexão quando necessário.
11. Verificar resultado.
12. Persistir snapshot, resultado e evento.
13. Devolver contrato de aplicação.

## Estados

```text
pending
validating
awaiting_confirmation
executing
reconnecting
verifying
succeeded
partially_succeeded
failed
timeout
cancelled
```

## Injeção de dependências

Services devem receber registry, gateway SSH, repositories, clock e auditoria por injeção sempre que esses componentes forem críticos para teste ou composição.

## Falhas

Converter erros de transporte, autenticação, capability, parsing, validação e reconexão para exceções semânticas da aplicação. Não esconder falhas retornando listas vazias ou sucesso genérico.
