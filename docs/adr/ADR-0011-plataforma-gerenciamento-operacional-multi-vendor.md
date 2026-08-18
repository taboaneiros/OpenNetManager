# ADR-0011 — Plataforma de Gerenciamento Operacional Multi-Vendor

## Status

Accepted

## Data

2026-08-17

## Contexto

O OpenNetManager começou como uma plataforma de inventário, coleta SSH, parsing, persistência de snapshots e dashboard operacional. A evolução observada no produto e a necessidade operacional definem um escopo mais amplo: a plataforma também deve configurar Wi-Fi, administrar rede e VLAN, executar manutenção, diagnosticar dispositivos, apresentar métricas detalhadas e operar clientes conectados.

As novas necessidades incluem:

- configuração de SSID e rádio;
- DHCP e IP fixo;
- VLAN de gerenciamento e VLANs associadas a SSIDs;
- reboot, reset, export e import de configuração;
- ping, traceroute, logs e configuração completa;
- terminal CLI controlado;
- dashboard com métricas de SSID, clientes e tráfego;
- listagem detalhada de clientes;
- desautenticação temporária de clientes.

O AP130 da Extreme Networks possui fluxos CLI mais complexos e não pode ser tratado como um dispositivo genérico simples. O GWN7600 da Grandstream também representa uma implementação concreta de outro vendor. A solução precisa acomodar diferenças de comandos, menus, firmware, semântica, capabilities, reconexão e rollback sem espalhar condicionais pelo núcleo.

## Decisão

O OpenNetManager será evoluído como uma plataforma multi-vendor de gerenciamento operacional de access points e dispositivos de rede, baseada em capabilities explícitas e operações de alto nível coordenadas por services e implementadas por drivers.

A plataforma permanecerá um monólito modular com camadas explícitas:

```text
Presentation
→ Application Services
→ Domain Contracts
→ Vendor Drivers
→ SSH Transport
→ Parsers/Validators
→ Repositories
```

Operações de leitura e alteração compartilharão contratos de aplicação, mas terão políticas diferentes:

- leituras podem retornar dados normalizados e raw protegido;
- alterações exigem autorização, validação, confirmação, execução controlada, verificação e auditoria;
- operações destrutivas devem possuir estado explícito e, quando possível, backup e rollback.

Cada driver deverá declarar capabilities por vendor, plataforma e eventualmente firmware. A interface não deve oferecer uma operação como disponível quando o driver não a suporta.

## Capabilities mínimas

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

## Fluxo de leitura

```text
View/API
→ Service
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
```

## Regras específicas

### Configuração

Configuração de SSID, rádio, IP, DHCP e VLAN deve ser representada em objetos estruturados e versionados. A implementação não deve expor comandos específicos ao domínio ou à apresentação.

Antes de aplicar uma alteração, o sistema deve:

1. carregar o estado atual;
2. validar valores e capabilities;
3. construir diff;
4. exibir preview;
5. solicitar confirmação;
6. criar backup quando aplicável;
7. aplicar pelo driver;
8. reconectar se necessário;
9. verificar o estado final;
10. persistir snapshot e auditoria.

### Manutenção

Reboot, reset, import e factory reset são operações sensíveis. Factory reset deve exigir confirmação reforçada e deve ser separado de reboot e reset de configuração.

### Rede e reconexão

Mudanças de endereço IP ou VLAN podem interromper a sessão SSH. O service deve controlar estados como `reconnecting`, executar tentativa de reconexão e somente atualizar o inventário após verificação bem-sucedida.

### Diagnóstico

Ping e traceroute devem indicar se foram executados no servidor ou no dispositivo. Logs, configuração completa e raw output devem possuir controle de acesso e mascaramento de segredos.

### CLI

O produto deve começar com terminal controlado por comandos/capabilities do driver. Um shell livre não é requisito obrigatório e só poderá ser introduzido com auditoria, timeout, autorização e política de segurança próprias.

### Clientes

A plataforma deve armazenar SSID, rádio, banda, IP, MAC, sinal, taxas, tempo conectado, última atividade e sistema operacional quando disponível. O sistema deve marcar o OS como conhecido, inferido, desconhecido ou não suportado.

A primeira ação de cliente será desautenticação temporária. Bloqueio permanente e deny list não fazem parte automaticamente da mesma operação.

## Alternativas consideradas

### Comandos genéricos diretamente nas views

Rejeitada. A abordagem acoplaria a UI ao vendor, dificultaria testes e aumentaria o risco de execução arbitrária.

### Um grande serviço genérico de configuração

Rejeitada. Um serviço monolítico acumularia regras de Wi-Fi, rede, manutenção, diagnóstico e clientes, criando baixo coesão e alta complexidade condicional.

### Um driver por fabricante sem capabilities

Rejeitada. A existência do driver não garante que todos os modelos ou firmwares suportem todas as operações.

### Terminal SSH totalmente livre

Adiada. É útil para troubleshooting avançado, mas amplia a superfície de risco e dificulta auditoria e previsibilidade.

### Microserviços

Rejeitada nesta etapa. O domínio pode ser isolado em módulos e contratos dentro do monólito; a distribuição prematura aumentaria custo operacional.

## Consequências positivas

- O produto passa a representar corretamente seu objetivo operacional.
- AP130 e GWN7600 podem evoluir com semânticas próprias sem contaminar o núcleo.
- A UI pode adaptar-se às capacidades reais de cada dispositivo.
- Configuração e manutenção tornam-se auditáveis.
- A evolução futura para Cisco, Huawei, Juniper, Mikrotik, Aruba e Ubiquiti fica preservada.
- O dashboard pode crescer sem acessar diretamente os dispositivos.

## Consequências negativas

- O domínio terá mais entidades, estados e contratos.
- Operações de alteração exigirão mais testes e validações que simples coleta.
- Nem todos os vendors suportarão as mesmas funcionalidades.
- Import/export e rollback exigirão tratamento por plataforma.
- A retenção de raw output, logs e auditoria aumentará custo de armazenamento.

## Riscos e mitigação

| Risco | Mitigação |
|---|---|
| Perda de conectividade ao alterar IP/VLAN | Estado de reconexão, validação prévia e atualização somente após confirmação. |
| Comando perigoso ou arbitrário | Comandos definidos pelo driver e terminal controlado. |
| Configuração parcialmente aplicada | Backup, estados explícitos, verificação pós-aplicação e rollback quando suportado. |
| Divergência entre vendors | Capability matrix, drivers isolados e fixtures reais. |
| Vazamento de segredos | Mascaramento, armazenamento seguro e export redacted por padrão. |
| Métricas incorretas | Janela de coleta explícita, timestamp e origem sempre apresentados. |
| Dado de OS tratado como certeza | Classificação conhecido/inferido/desconhecido. |

## Impacto no roadmap

A Fase 2 passa a incluir observabilidade avançada, diagnóstico, clientes e dashboard. A Fase 3 passa a incluir configuração segura de Wi-Fi e rede. A Fase 4 passa a incluir manutenção, import/export, desautenticação e CLI controlada. Escala, scheduler, Redis e novos vendors permanecem posteriores à estabilização dos contratos.

## Critérios de revisão

Esta ADR deverá ser revisitada quando:

- houver necessidade de suportar outro transporte além de SSH;
- o primeiro vendor exigir rollback transacional real;
- o terminal livre se tornar requisito obrigatório;
- o modelo de capabilities precisar de versionamento por firmware;
- a escala exigir separação do monólito em serviços distribuídos.
