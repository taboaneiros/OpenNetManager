# Política de Segurança

## Objetivo

Este documento estabelece expectativas de segurança para desenvolvimento, operação e reporte de vulnerabilidades no OpenNetManager. Como o sistema lida com credenciais de dispositivos e acesso administrativo a infraestrutura de rede, segurança deve ser tratada como requisito estrutural desde a Fase 0.

## Escopo de segurança

O escopo inclui:

- autenticação de usuários da plataforma;
- autorização de acesso a funcionalidades e dados;
- armazenamento e uso de credenciais de dispositivos;
- transporte SSH para dispositivos gerenciados;
- persistência de snapshots, eventos e dados de inventário;
- logs, auditoria e rastreabilidade;
- dependências, pipeline de CI/CD e imagens Docker.

## Princípios

- Segredo mínimo necessário.
- Menor privilégio possível.
- Segregação de responsabilidades.
- Falha segura por padrão.
- Auditoria suficiente para rastrear ações sensíveis.
- Redação e mascaramento obrigatórios em logs.

## Reporte de vulnerabilidades

Vulnerabilidades não devem ser publicadas inicialmente em issues abertas. O projeto deve manter um canal privado de reporte definido pelos maintainers antes da primeira release pública operacional. Até a formalização do canal, toda divulgação deve ser tratada como privada pelos responsáveis do repositório.

O fluxo recomendado é:

1. Recebimento privado.
2. Validação e classificação de severidade.
3. Reprodução controlada.
4. Definição de correção e mitigação.
5. Publicação coordenada após remediação.

## Requisitos mínimos para credenciais

- Credenciais nunca devem ser armazenadas em texto puro quando houver alternativa viável.
- Campos sensíveis devem ser criptografados em repouso ou protegidos por mecanismo equivalente definido na arquitetura de segurança.
- Senhas, chaves privadas e passphrases nunca podem aparecer em logs, traces, mensagens de erro de usuário ou respostas de API.
- UI deve mascarar segredos após criação e permitir rotação controlada.

## Requisitos mínimos para SSH

- Host key verification deve ser planejada, documentada e controlável por ambiente.
- Timeouts de conexão, autenticação e comando devem ser explícitos.
- Retries devem ser limitados e previsíveis.
- Comandos executados devem ser controlados por driver, nunca por entrada arbitrária do usuário final.

## Dependências e manutenção

Django 5.2 é LTS e recebe suporte de segurança por período prolongado, o que influencia positivamente a postura de manutenção do projeto.[web:1][web:12] Ao mesmo tempo, a equipe deve acompanhar releases corretivas do framework e de bibliotecas críticas, pois o uso de versões suportadas não substitui disciplina de atualização.[web:5][web:13]

## Itens sensíveis a revisão contínua

- política de criptografia de credenciais;
- modelo de permissões;
- hardening de sessão Django;
- CSRF, headers e cookies;
- sanitização de payloads de API;
- supply chain de dependências;
- segurança de imagens Docker;
- vazamento de dados por logging.

## Não objetivos desta versão do documento

Este documento não define ainda o desenho criptográfico detalhado nem o fluxo operacional completo de resposta a incidentes. Esses itens serão aprofundados na documentação interna de `docs/security.md` nas próximas entregas da Fase 0.
