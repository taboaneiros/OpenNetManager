# Visão do Produto

## Declaração

O OpenNetManager é uma plataforma Open Source, multi-vendor, para gerenciamento operacional de access points e dispositivos de rede. Seu objetivo é transformar operações fragmentadas por CLI e fabricante em uma experiência consistente de inventário, coleta, configuração, manutenção, diagnóstico, histórico e auditoria.

## Problema

Equipes de rede normalmente precisam alternar entre interfaces, comandos, credenciais e formatos de saída diferentes para operar equipamentos heterogêneos. Isso dificulta diagnóstico, aumenta o risco de alterações manuais, reduz rastreabilidade e torna comparações históricas pouco confiáveis.

## Proposta de valor

- Inventário centralizado.
- Coleta SSH controlada.
- Normalização de dados.
- Configuração segura e auditável.
- Diagnóstico a partir do dispositivo e da plataforma.
- Histórico de snapshots, eventos e configurações.
- Dashboard operacional com clientes, SSIDs, rádios e tráfego.
- Expansão para novos vendors sem reescrever o núcleo.

## Usuários-alvo

- Administradores de rede.
- Operadores NOC.
- Suporte técnico.
- Equipes de infraestrutura.
- Desenvolvedores de integrações para novos vendors.

## Capacidades do produto

### Operação

- Cadastro e consulta de dispositivos.
- Coleta manual e agendada.
- Snapshots e comparação histórica.
- Eventos operacionais e auditoria.

### Configuração

- SSID e segurança.
- Rádio, canal, largura e potência.
- DHCP e IP fixo.
- VLAN de gerenciamento e VLAN de SSID.

### Manutenção

- Reboot.
- Reset de configuração.
- Factory reset protegido.
- Export e import versionados.

### Diagnóstico

- Ping e traceroute a partir do servidor ou do dispositivo.
- Logs filtráveis e exportáveis.
- Configuração completa protegida.
- CLI controlada.

### Clientes e dashboard

- Clientes por SSID, rádio e AP.
- Sinal, banda, taxa de upload e download.
- OS conhecido, inferido ou desconhecido.
- Desautenticação temporária.
- Top clientes e SSIDs por quantidade e tráfego.

## Suporte inicial

O AP130 da Extreme Networks é o primeiro driver estratégico. O Grandstream GWN7600 também é uma integração concreta do sistema. A diferença de complexidade entre os equipamentos, especialmente nos fluxos CLI do AP130, deve permanecer isolada em drivers e parsers.

## Limitações intencionais

- O produto não começa como controlador universal de todos os fabricantes.
- Nem todo vendor oferecerá todas as capabilities.
- Monitoramento em tempo real contínuo depende de evolução de coleta e escala.
- CLI livre não é requisito inicial; a primeira implementação deve ser controlada.
- Rollback depende do suporte concreto de cada equipamento.

## Métricas de sucesso

- Tempo para cadastrar e operar um novo dispositivo.
- Tempo para adicionar um novo vendor.
- Percentual de operações com auditoria completa.
- Taxa de sucesso das coletas.
- Correção dos dados normalizados.
- Tempo de diagnóstico de falhas.
- Clareza do dashboard para operadores.
