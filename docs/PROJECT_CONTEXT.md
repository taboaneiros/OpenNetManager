# Contexto do Projeto OpenNetManager

## Problema de negócio

Ambientes de rede combinam equipamentos de fabricantes distintos, interfaces administrativas incompatíveis e baixo grau de padronização. A operação exige acesso manual, dificulta diagnóstico e aumenta o risco de alterações sem rastreabilidade.

O OpenNetManager centraliza inventário, coleta, configuração, manutenção, diagnóstico, histórico e auditoria em uma plataforma multi-vendor. O AP130 da Extreme Networks é um caso de integração mais complexo por depender de fluxos CLI específicos; essa complexidade deve ser encapsulada sem contaminar o núcleo.

## Estado funcional

A plataforma já possui base operacional com inventário, coleta SSH, parsers, snapshots, eventos, clientes, interfaces e dashboard. O suporte ao AP130 e ao GWN7600 demonstra a necessidade de manter capabilities explícitas por vendor, plataforma e firmware.

## Escopo do produto

O produto cobre:

- inventário e credenciais;
- coleta e observabilidade;
- SSID e rádio;
- IP, DHCP e VLAN;
- reboot, reset, export e import;
- ping, traceroute, logs e configuração completa;
- dashboard de clientes, SSIDs, rádios e tráfego;
- desautenticação temporária;
- CLI controlada.

## Premissas

- O núcleo não depende de um vendor específico.
- Nem todos os dispositivos suportam todas as operações.
- Capabilities devem ser declaradas pelo driver.
- Alterações precisam ser autorizadas, confirmadas, verificadas e auditadas.
- Dashboard usa dados persistidos e não abre SSH.
- Raw output pode ser preservado com acesso protegido.
- SQLite serve ao desenvolvimento e PostgreSQL à produção.
- Redis, scheduler distribuído e execução massiva permanecem evoluções posteriores.

## Riscos adicionais

### Perda de conectividade

Alterar IP, DHCP ou VLAN pode interromper SSH. O fluxo precisa controlar reconexão e somente confirmar a alteração após validar o novo estado.

### Aplicação parcial

APs podem aplicar parte de uma configuração. O sistema deve registrar estado parcial, preservar backup e verificar cada etapa possível.

### Operações destrutivas

Reboot, reset, import e factory reset exigem autorização, confirmação e auditoria. Factory reset deve ter confirmação reforçada.

### Vazamento de segredos

Senhas de SSH e Wi-Fi não podem aparecer em logs, raw output, snapshots, exports comuns, templates ou API.

### Comandos arbitrários

Entrada livre de comandos amplia o risco. A plataforma deve começar com comandos versionados e permitidos pelos drivers.

### Métricas incorretas

Taxas de tráfego e estado de clientes dependem da janela de coleta. Todo dado deve carregar timestamp, origem e indicação de disponibilidade.

## Restrições arquiteturais

- Views não acessam ORM.
- Services coordenam casos de uso.
- Repositories isolam persistência.
- Drivers encapsulam vendor.
- Parsers interpretam texto e não conhecem transporte.
- SSH executa somente comandos controlados.
- Dashboard não faz coleta em tempo real diretamente.
- API e UI reutilizam os mesmos services.

## Critérios de sucesso

- Operador consegue consultar e diagnosticar dispositivos sem acessar manualmente cada CLI.
- Configurações suportadas podem ser aplicadas com preview, confirmação e auditoria.
- Falhas de capability são explícitas.
- Adição de vendor não exige alteração estrutural do núcleo.
- Snapshots e eventos permitem explicar o estado histórico.
- Testes detectam regressões de parser, driver, segurança e arquitetura.
