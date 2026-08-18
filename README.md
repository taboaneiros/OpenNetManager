# OpenNetManager

OpenNetManager é uma plataforma Open Source, multi-vendor, para gerenciamento operacional de access points e dispositivos de rede. O sistema centraliza inventário, coleta, configuração, manutenção, diagnóstico, histórico, auditoria e visualização operacional sem acoplar o núcleo a um fabricante específico.

O projeto possui suporte funcional inicial para o Extreme Networks AP130 via SSH e para o Grandstream GWN7600. Novos vendors devem ser incorporados por drivers, parsers, capabilities, fixtures e testes, sem espalhar comandos ou semânticas específicas pelo núcleo.

## Capacidades

- Inventário de dispositivos e credenciais.
- Coleta SSH e snapshots históricos.
- Informações de sistema, interfaces, rádios, SSIDs e clientes.
- Dashboard operacional com eventos e métricas.
- Configuração de SSID e rádio, quando suportada pelo driver.
- DHCP, IP fixo e VLAN, quando suportados pelo driver.
- Reboot, reset, export e import de configuração.
- Ping, traceroute, logs e configuração completa.
- CLI controlada para diagnóstico.
- Listagem de clientes com sinal, banda, SSID, taxas e status.
- Desautenticação temporária de clientes.
- Auditoria e confirmação para ações sensíveis.

## Arquitetura

```text
View/API
→ Service
→ Authorization/Capability Check
→ Repository ou Driver
→ SSH
→ Parser/Verification
→ Domain Objects
→ Repository/Audit Event
```

Princípios obrigatórios:

- Views não acessam ORM diretamente.
- Dashboard nunca abre SSH.
- Parsers não abrem conexão nem persistem dados.
- Drivers encapsulam comandos e diferenças de vendor.
- Services coordenam regras de negócio, autorização e transações.
- Repositories isolam persistência.
- Comandos SSH são controlados pelos drivers.
- Operações destrutivas exigem confirmação e auditoria.

## Stack

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.13 |
| Framework | Django 5.2 |
| API | Django REST Framework |
| UI | Bootstrap 5 + HTMX |
| SSH | Paramiko |
| Desenvolvimento | SQLite |
| Produção | PostgreSQL |
| Qualidade | pytest, Black, isort, Flake8, mypy |
| Entrega | GitHub Actions e Docker |

## Estado do projeto

O projeto está na transição entre a conclusão do núcleo funcional e a consolidação operacional. Já existem inventário, coleta SSH, parsing, snapshots, clientes, eventos, dashboard e suporte a mais de um equipamento. A próxima evolução prioriza capabilities, configuração segura, diagnóstico, manutenção, auditoria e métricas operacionais.

## Documentação

- [Visão do produto](docs/vision.md)
- [Contexto do projeto](docs/PROJECT_CONTEXT.md)
- [Requisitos funcionais](docs/functional_requirements.md)
- [Modelo de domínio](docs/domain_model.md)
- [Arquitetura](docs/architecture.md)
- [Dashboard](docs/dashboard.md)
- [Drivers](docs/drivers.md)
- [Services](docs/services.md)
- [Segurança](docs/security.md)
- [Roadmap](docs/ROADMAP.md)
- [ADRs](docs/adr/)

## Contribuição

Consulte [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md) e [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) antes de abrir uma contribuição.
