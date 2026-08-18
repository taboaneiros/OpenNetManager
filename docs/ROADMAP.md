# Roadmap do OpenNetManager

## Princípios

- Segurança antes de conveniência.
- Correção dos dados antes de volume de features.
- Capability real antes de abstração fictícia.
- Configuração com preview, confirmação e auditoria.
- Novos vendors sem contaminar o núcleo.
- Escala somente depois da estabilização operacional.

## Fase 0 — Fundação

### Objetivos

- Consolidar visão multi-vendor de gerenciamento operacional.
- Documentar requisitos de coleta, configuração, manutenção e diagnóstico.
- Definir domínio de capabilities, operações e auditoria.
- Registrar ADRs.
- Garantir estratégia de segurança e testes.

### Critério de saída

Documentação, contratos e riscos permitem implementação sem ambiguidade estrutural relevante.

## Fase 1 — Núcleo funcional

### Entregas

- Autenticação e autorização básicas.
- Inventário.
- Credenciais.
- Coleta SSH.
- AP130 e GWN7600.
- Parsers de sistema, interfaces e clientes.
- Snapshots.
- Eventos.
- Dashboard inicial.
- API mínima.

### Estado

Majoritariamente implementada, em consolidação e validação.

## Fase 2 — Consolidação operacional

### Entregas

- Dashboard avançado.
- SSIDs e rádios.
- Métricas de upload/download.
- Ranking de clientes e SSIDs.
- Histórico de clientes.
- Logs.
- Configuração completa.
- Ping e traceroute.
- Comparação de snapshots.
- Auditoria completa.
- Tela detalhada de clientes.

### Critério de saída

Operador consegue observar e diagnosticar o ambiente sem depender da CLI manual para tarefas comuns.

## Fase 3 — Configuração segura

### Entregas

- Configuração de SSID.
- Configuração de rádio.
- DHCP.
- IP fixo.
- VLAN de gerenciamento.
- VLAN de SSID.
- Preview e diff.
- Backup automático.
- Reconexão.
- Verificação pós-aplicação.

### Critério de saída

Alterações suportadas podem ser aplicadas com autorização, confirmação, auditoria e resultado verificável.

## Fase 4 — Manutenção e operações de clientes

### Entregas

- Reboot.
- Reset de serviço e configuração.
- Export/import versionados.
- Factory reset protegido.
- Desautenticação temporária.
- CLI controlada.

### Critério de saída

Ações operacionais sensíveis estão protegidas, auditadas e testadas por driver.

## Fase 5 — Escala e ecossistema

### Entregas

- Scheduler persistido.
- Execução assíncrona.
- Redis.
- Limites de concorrência.
- Backoff por dispositivo.
- Plugins.
- API pública ampliada.
- Novos vendors: Cisco, Huawei, Juniper, Mikrotik, Aruba e Ubiquiti.

## Fora do escopo imediato

- Shell SSH totalmente livre.
- Auto-discovery amplo.
- Alta disponibilidade nativa.
- Rollback universal entre vendors.
- Monitoramento em tempo real sem janela de coleta definida.
- Configuração de capabilities sem validação em equipamento real.
