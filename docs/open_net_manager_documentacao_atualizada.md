# OpenNetManager — Documentação Atualizada do Produto

## 1. Nova definição do produto

O OpenNetManager é uma plataforma Open Source, multi-vendor, para gerenciamento operacional de access points e dispositivos de rede. A plataforma centraliza inventário, coleta, configuração, manutenção, diagnóstico, histórico, auditoria e visualização operacional, mantendo separação rigorosa entre apresentação, aplicação, domínio, persistência, transporte e integração específica de fabricante.

O produto deve permitir que operadores consultem o estado dos dispositivos, executem coletas, configurem Wi-Fi e rede, realizem ações de manutenção, diagnostiquem conectividade, analisem clientes conectados e acompanhem métricas históricas por dispositivo, SSID, rádio e cliente.

O AP130 da Extreme Networks permanece como primeiro driver estratégico. O Grandstream GWN7600 também deve ser tratado como implementação concreta suportada, sem alterar o princípio de que novos vendors sejam adicionados por drivers, parsers, capabilities, fixtures e testes.

## 2. Proposta de valor

O OpenNetManager deve:

- reduzir a dependência de acesso manual e fragmentado por CLI;
- oferecer uma experiência operacional consistente entre fabricantes;
- normalizar informações heterogêneas de dispositivos em objetos de domínio;
- permitir configuração segura e auditável;
- preservar snapshots, configuração bruta, logs e eventos para histórico;
- oferecer diagnóstico a partir do dispositivo e da plataforma;
- facilitar expansão para novos vendors sem reescrever o núcleo.

## 3. Capacidades do produto

### 3.1 Inventário

- Cadastro e edição de dispositivos.
- Vendor, plataforma, modelo, firmware e capacidades.
- Endereço de gerenciamento, porta e credencial associada.
- Ativação e desativação lógica.
- Último estado conhecido e última coleta.

### 3.2 Coleta e observabilidade

- Coleta manual e futura coleta agendada.
- Informações de sistema.
- Interfaces e rádios.
- SSIDs e perfis publicados.
- Clientes conectados.
- Eventos operacionais.
- Snapshots históricos.
- Comparação entre snapshots.
- Preservação opcional da saída bruta.

### 3.3 Configuração de Wi-Fi

A plataforma deve permitir configurar, quando suportado pelo driver:

- SSID;
- ativação ou desativação do perfil;
- segurança e modo de autenticação;
- senha ou referência protegida a segredo;
- SSID oculto;
- VLAN associada;
- bandas habilitadas;
- isolamento de clientes;
- limite de clientes;
- parâmetros específicos do vendor.

A configuração de rádio deve contemplar:

- banda;
- habilitação;
- canal automático ou fixo;
- largura de canal;
- potência de transmissão;
- modo de operação;
- minimum RSSI;
- airtime fairness;
- band steering;
- parâmetros específicos do vendor.

Toda alteração deve possuir preview/diff, validação, confirmação, execução pelo driver, pós-validação, evento de auditoria e snapshot de configuração quando aplicável.

### 3.4 Manutenção

Operações de manutenção:

- reboot;
- reset de serviço;
- reset de configuração;
- factory reset;
- exportação de configuração;
- importação de configuração;
- backup automático antes de operações destrutivas;
- verificação de retorno após reboot ou alteração de rede.

Factory reset exige autorização administrativa forte, confirmação explícita do hostname, aviso de perda de conectividade e auditoria completa.

### 3.5 Rede

A plataforma deve suportar, quando o driver possuir capability:

- DHCP;
- IP fixo;
- prefixo de rede;
- gateway;
- DNS;
- hostname;
- VLAN de gerenciamento;
- VLAN associada ao SSID;
- VLAN nativa ou trunk;
- tagging e untagging;
- VLANs permitidas.

Alterações de endereço ou VLAN devem possuir tratamento especial para perda de SSH, reconexão, validação do novo endereço e atualização segura do inventário.

### 3.6 Diagnóstico

A plataforma deve permitir:

- ping originado no servidor;
- ping originado no dispositivo;
- traceroute originado no servidor;
- traceroute originado no dispositivo;
- visualização de logs do device;
- filtros por período e severidade;
- exportação de logs;
- visualização da configuração completa;
- exportação da configuração completa;
- preservação da saída bruta;
- consulta de status de interfaces, rádios, clientes e rotas;
- console CLI controlado e auditado.

A origem do diagnóstico deve ser sempre apresentada ao operador.

### 3.7 Dashboard

O dashboard deve apresentar dados persistidos e indicar o horário da última atualização. Ele não deve abrir SSH diretamente.

Indicadores principais:

- access points online e offline;
- clientes conectados;
- SSIDs ativos;
- taxa total de upload;
- taxa total de download;
- coletas com falha;
- interfaces ou rádios degradados;
- clientes com sinal ruim;
- última coleta por dispositivo.

Visualizações recomendadas:

- clientes por SSID;
- tráfego por SSID;
- clientes por banda;
- upload e download ao longo do tempo;
- top 5 clientes por download;
- top 5 clientes por upload;
- top 5 clientes por tráfego total;
- top 5 SSIDs por quantidade de clientes;
- top 5 SSIDs por tráfego total;
- top 5 APs por quantidade de clientes;
- top 5 APs por tráfego;
- top 5 clientes com pior sinal;
- eventos recentes;
- falhas de coleta;
- APs sem atualização recente.

O termo “mais usado” deve ser separado em quantidade de clientes e volume de tráfego.

### 3.8 Clientes

A tela de clientes deve listar:

- hostname;
- MAC;
- IP;
- SSID conectado;
- access point;
- banda e rádio;
- canal;
- sinal/RSSI;
- taxa de upload;
- taxa de download;
- tempo conectado;
- última atividade;
- status;
- sistema operacional, quando fornecido ou inferido;
- origem e timestamp da informação.

O sistema deve distinguir OS conhecido, inferido, desconhecido e não suportado.

A ação inicial de operação de cliente será desautenticação temporária. Bloqueio permanente e políticas de deny list são capacidades diferentes e devem ser tratadas separadamente.

## 4. Modelo de capabilities

Cada driver deve informar explicitamente suas capacidades:

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

A interface deve mostrar somente ações suportadas ou informar claramente quando uma capability não estiver disponível. Nunca deve haver sucesso simulado ou resposta vazia que pareça uma operação concluída.

## 5. Contratos de operações

Operações de leitura podem retornar dados normalizados e raw opcional.

Operações de alteração devem retornar:

- identificador da operação;
- dispositivo;
- usuário executor;
- capability utilizada;
- estado inicial;
- estado final, quando validado;
- sucesso, sucesso parcial, timeout ou falha;
- mensagem operacional;
- evento de auditoria;
- referência a backup ou snapshot, quando aplicável.

Estados recomendados:

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

## 6. Regras de segurança

- Segredos nunca aparecem em claro após criação.
- Senhas de Wi-Fi não aparecem em snapshots comuns, logs ou respostas de API.
- Operações destrutivas exigem autorização específica.
- Reboot, reset, import, mudança de IP, mudança de VLAN e desautenticação exigem confirmação.
- Configuração completa e raw output devem possuir controle de acesso.
- Toda alteração deve gerar auditoria.
- Comandos SSH são definidos pelos drivers, nunca montados livremente com entrada do usuário.
- O terminal CLI deve ser controlado, temporizado e auditado.
- Factory reset deve exigir proteção reforçada.
- Exportação deve mascarar segredos por padrão.

## 7. Arquitetura obrigatória

Fluxo de leitura:

```text
View/API
→ Service
→ Repository/Driver
→ SSH
→ Parser
→ Domain Objects
→ Repository
```

Fluxo de alteração:

```text
View/API
→ Service
→ Capability Check
→ Validation/Diff
→ Confirmation
→ Driver
→ SSH
→ Parser/Verification
→ Repository
→ Audit Event
```

Restrições:

- Views não acessam ORM diretamente.
- Dashboard não acessa SSH.
- Parsers não abrem conexão e não persistem.
- Drivers não implementam regra de negócio geral.
- Repositories isolam persistência.
- Services coordenam casos de uso, transações, estados e auditoria.
- Nenhuma camada central contém comandos específicos de AP130 ou GWN7600.

## 8. Roadmap atualizado

### Fase 0 — Fundação

- Documentação, arquitetura, domínio, segurança, testes e governança.
- ADR de plataforma de gerenciamento operacional.
- ADR de capabilities por vendor.
- ADR de operações destrutivas e auditoria.
- ADR de configuração versionada e export/import.

### Fase 1 — Núcleo funcional

- Inventário.
- Autenticação e autorização.
- Coleta SSH.
- AP130 e GWN7600.
- Parsers de sistema, interfaces e clientes.
- Snapshots.
- Dashboard inicial.
- API mínima.

### Fase 2 — Consolidação operacional

- Dashboard avançado.
- SSIDs, rádios e métricas de tráfego.
- Histórico de clientes.
- Logs e configuração completa.
- Ping e traceroute.
- Comparação de snapshots.
- Auditoria completa.
- Tela de clientes.

### Fase 3 — Configuração segura

- Configuração de SSID.
- Configuração de rádio.
- DHCP e IP fixo.
- VLANs.
- Preview/diff.
- Backup automático.
- Reconexão após alteração de endereço.
- Validação pós-aplicação.

### Fase 4 — Manutenção e ações operacionais

- Reboot.
- Reset de serviço e configuração.
- Export/import.
- Factory reset protegido.
- Desautenticação temporária de clientes.
- Terminal CLI controlado.

### Fase 5 — Escala e ecossistema

- Scheduler persistido.
- Execução assíncrona.
- Redis.
- Limites de concorrência.
- Backoff por dispositivo.
- Plugins e novos vendors.
- API pública ampliada.

## 9. Critérios de aceite da nova definição

A nova definição será considerada implementada por capacidade quando:

- a capability estiver declarada no driver;
- a operação possuir service dedicado;
- a UI/API verificar autorização e capability;
- o driver executar comandos controlados;
- o resultado for normalizado;
- falhas forem classificadas;
- ações de alteração forem auditadas;
- existirem testes unitários e de integração;
- houver fixture real ou evidência controlada do equipamento;
- a documentação do vendor indicar limitações conhecidas.

## 10. Decisões em aberto

- estratégia definitiva de armazenamento de segredos;
- formato canônico de export/import;
- política de retenção de raw output e logs;
- suporte a terminal livre ou somente terminal controlado;
- fonte de identificação do sistema operacional dos clientes;
- janela de coleta para métricas de tráfego;
- política de rollback por vendor;
- primeiro conjunto de capabilities implementadas em cada driver.
