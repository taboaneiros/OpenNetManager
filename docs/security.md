# Segurança Operacional

## Princípios

O OpenNetManager manipula credenciais privilegiadas e pode executar alterações destrutivas em equipamentos de rede. Segurança deve ser aplicada no fluxo de aplicação, no driver, no transporte, na persistência, na UI e na auditoria.

## Autorização

Separar permissões de:

- leitura de inventário;
- leitura de clientes e logs;
- diagnóstico;
- configuração de Wi-Fi;
- configuração de rede/VLAN;
- reboot;
- reset;
- factory reset;
- import/export;
- desautenticação;
- CLI.

Não considerar usuário autenticado automaticamente autorizado a alterar dispositivo.

## Confirmação

Devem exigir confirmação:

- reboot;
- reset;
- factory reset;
- import;
- mudança de IP;
- mudança de VLAN de gerenciamento;
- alteração de SSID ou rádio;
- desautenticação de cliente;
- comandos CLI administrativos.

Factory reset deve exigir confirmação textual do dispositivo e permissão administrativa forte.

## Segredos

- Armazenar credenciais protegidas.
- Nunca reexibir segredo após criação.
- Mascarar senhas SSH e Wi-Fi em logs, snapshots, raw output, exports, templates e APIs.
- Exportar configuração redacted por padrão.
- Evitar valores padrão inseguros em produção.

## SSH

- Validar host key conforme ambiente.
- Aplicar timeout de conexão, autenticação, comando e operação total.
- Limitar retries.
- Restringir comandos ao driver.
- Não montar comando diretamente com input arbitrário.
- Registrar falhas sem expor segredo.

## Configuração de rede

Mudanças de IP, DHCP ou VLAN podem derrubar a sessão. O sistema deve:

- alertar o operador;
- manter estado de reconexão;
- tentar validar endpoint novo;
- atualizar inventário somente após confirmação;
- registrar perda de conexão e resultado.

## Backup, import e reset

- Oferecer backup antes de reset/import.
- Validar schema e compatibilidade.
- Exibir diff.
- Rejeitar campos perigosos ou desconhecidos quando necessário.
- Registrar checksum, usuário e timestamp.
- Implementar rollback somente quando suportado e testado.

## CLI

A primeira versão deve ser controlada por capability e lista de comandos. Sessões devem possuir usuário, device, início, fim, timeout, comandos executados e auditoria. Shell livre exige análise de segurança própria.

## Auditoria

Registrar:

- usuário;
- device;
- operação;
- capability;
- estado anterior;
- estado posterior;
- sucesso ou falha;
- erro normalizado;
- timestamp;
- correlation id;
- backup ou snapshot relacionado.

Eventos de auditoria não devem ser apagados por rotinas comuns de limpeza.

## Diagnóstico

Logs e configuração completa podem conter dados sensíveis. Controlar leitura, exportação, retenção e acesso administrativo. Informar sempre origem do diagnóstico: servidor ou dispositivo.

## Clientes

MAC, IP, hostname, SSID e dados de tráfego são informações operacionais potencialmente sensíveis. Restringir acesso conforme perfil e evitar exportação desnecessária.
