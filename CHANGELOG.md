# Changelog

Este projeto segue versionamento semântico e registro explícito de mudanças relevantes em formato inspirado em Keep a Changelog.

## [0.2.0-dev] — Evolução para gerenciamento operacional

### Added

- Redefinição do OpenNetManager como plataforma multi-vendor de gerenciamento operacional.
- Inclusão de configuração de SSID, rádio, rede e VLAN no escopo do produto.
- Inclusão de operações de reboot, reset, export e import de configuração.
- Inclusão de diagnóstico por ping, traceroute, logs e configuração completa.
- Definição de CLI controlada e auditada.
- Evolução do dashboard para clientes, SSIDs, rádios e tráfego.
- Definição da tela operacional de clientes.
- Definição de desautenticação temporária.
- Definição do modelo de capabilities por vendor, plataforma e firmware.
- ADR da plataforma de gerenciamento operacional multi-vendor.

### Supported devices

- Extreme Networks AP130 via SSH.
- Grandstream GWN7600 via SSH.

### Notes

Esta versão representa a evolução do escopo e dos contratos do produto. As capacidades de configuração e manutenção devem ser implementadas progressivamente, sempre condicionadas às capabilities reais de cada driver.

## [0.1.0] — Fase 0

### Added

- Contexto de produto e engenharia.
- Arquitetura em camadas orientada a services, repositories, drivers e parsers.
- Stack base com Python 3.13 e Django 5.2.
- Roadmap macro.
- Diretrizes de contribuição, segurança e conduta.
- Estrutura inicial de documentação.
