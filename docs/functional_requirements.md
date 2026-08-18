# Requisitos Funcionais

## Objetivo

Definir capacidades observáveis e testáveis do OpenNetManager como plataforma multi-vendor de gerenciamento operacional de access points e dispositivos de rede.

## Requisitos existentes

Os requisitos RF-001 a RF-030 permanecem válidos, incluindo autenticação, autorização, inventário, credenciais, SSH, drivers, coleta, snapshots, eventos, dashboard, API, jobs, auditoria, mascaramento de segredos, extensibilidade e health endpoint.

## Novos requisitos

### RF-031 — Configuração de SSID

O sistema deve permitir configurar SSID, habilitação, segurança, senha protegida, visibilidade, VLAN, bandas e opções suportadas pelo vendor. A operação deve apresentar diff, exigir confirmação e registrar auditoria.

### RF-032 — Configuração de rádio

O sistema deve permitir configurar banda, canal, largura, potência, modo, minimum RSSI, band steering, airtime fairness e opções específicas quando suportadas.

### RF-033 — Configuração DHCP

O sistema deve permitir ativar DHCP na interface de gerenciamento quando suportado, informando o risco de mudança de endereço e controlando reconexão.

### RF-034 — Configuração de IP fixo

O sistema deve permitir configurar endereço, prefixo, gateway e DNS. O novo endereço só deve substituir o endereço persistido após validação de conectividade, salvo política explicitamente documentada.

### RF-035 — Configuração de VLAN

O sistema deve permitir configurar VLAN de gerenciamento e VLAN associada a SSID, além de tagging, untagging, trunk e VLAN nativa quando suportados. O sistema deve alertar sobre risco de perda de acesso.

### RF-036 — Reboot

Usuário autorizado deve poder reiniciar um dispositivo suportado. A operação deve registrar usuário, dispositivo, início, resultado, indisponibilidade esperada e retorno verificado.

### RF-037 — Reset de configuração

Usuário com permissão específica deve poder solicitar reset de configuração suportado pelo device. O sistema deve distinguir reset de serviço, reset de configuração e factory reset.

### RF-038 — Factory reset

Factory reset deve exigir autorização administrativa forte, confirmação textual do dispositivo, aviso de perda de configuração e auditoria. Backup deve ser oferecido antes da execução.

### RF-039 — Exportação de configuração

O sistema deve exportar configuração em formato versionado, identificando vendor, plataforma, modelo e timestamp. Segredos devem ser mascarados por padrão.

### RF-040 — Importação de configuração

O sistema deve validar compatibilidade, schema, vendor, plataforma e campos perigosos antes de aplicar uma configuração. Deve apresentar diff, solicitar confirmação e preservar backup quando possível.

### RF-041 — Ping

O sistema deve executar ping a partir do servidor ou do dispositivo quando suportado, identificando claramente a origem e normalizando resultado, latência, perda e saída bruta.

### RF-042 — Traceroute

O sistema deve executar traceroute a partir do servidor ou do dispositivo quando suportado, identificando origem, destino, saltos, timeout e resultado.

### RF-043 — Logs do dispositivo

O sistema deve permitir consultar logs do device com filtros de período, severidade e texto quando suportado. Logs devem ter origem, timestamp e controle de acesso.

### RF-044 — Exportação de logs

O sistema deve exportar logs em formato seguro e auditável, sem incluir segredos conhecidos.

### RF-045 — Configuração completa

O sistema deve permitir visualizar e exportar a configuração completa ou o estado equivalente fornecido pelo device. Segredos devem ser mascarados por padrão.

### RF-046 — CLI controlada

O sistema deve oferecer uma interface de diagnóstico com comandos permitidos pelo driver, timeout, controle de sessão, registro de usuário e auditoria. Shell livre não é obrigatório.

### RF-047 — Dashboard operacional avançado

O dashboard deve apresentar APs online/offline, clientes, SSIDs, rádios, taxas totais, falhas de coleta, eventos e timestamp da última atualização.

### RF-048 — Métricas de SSID e tráfego

O sistema deve consolidar clientes e tráfego por SSID, distinguindo ranking por quantidade de clientes de ranking por volume de tráfego.

### RF-049 — Tela detalhada de clientes

O sistema deve listar hostname, MAC, IP, SSID, AP, banda, rádio, canal, sinal, upload, download, tempo conectado, última atividade, status e OS quando disponível.

### RF-050 — Sistema operacional do cliente

O sistema deve classificar o OS como conhecido, inferido, desconhecido ou não suportado. Informação inferida não deve ser apresentada como certeza.

### RF-051 — Desautenticação temporária

Usuário autorizado deve poder desautenticar temporariamente cliente suportado. A operação deve apresentar MAC, SSID e AP, exigir confirmação, executar capability do driver e registrar evento.

### RF-052 — Capabilities por vendor

O sistema deve resolver e expor capabilities por vendor, plataforma e, quando necessário, firmware. Capability não suportada deve retornar erro semântico explícito.

### RF-053 — Auditoria de alterações

Toda alteração de configuração, manutenção, diagnóstico sensível, import/export e operação de cliente deve registrar usuário, dispositivo, operação, resultado, timestamp e referência de backup ou snapshot quando aplicável.

### RF-054 — Verificação pós-operação

Operações de alteração devem verificar o estado final quando possível e classificar sucesso, sucesso parcial, falha, timeout ou necessidade de reconexão.

## Estados de operação

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

## Critérios gerais de aceite

- Capability é verificada antes da execução.
- A autorização é verificada antes da execução.
- Operação destrutiva exige confirmação.
- Segredos não são retornados.
- Falhas são classificadas.
- Resultado possui origem, timestamp e mensagem.
- Há auditoria para alterações.
- Há teste de sucesso, falha e capability ausente.
