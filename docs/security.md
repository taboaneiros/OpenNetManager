# Segurança Técnica

## Objetivo

Aprofundar as diretrizes de segurança do OpenNetManager em nível de arquitetura e implementação.

## Superfícies de ataque relevantes

- login web e gestão de sessão;
- endpoints de API;
- armazenamento e uso de credenciais de dispositivos;
- conexão SSH com hosts remotos;
- upload futuro de chaves/arquivos;
- logs e mensagens de erro;
- pipeline CI/CD e segredos de ambiente;
- dependências do projeto.

## Controles mínimos

### Aplicação web

- CSRF habilitado em fluxos de formulário.
- Cookies com flags seguras por ambiente.
- Sessões com políticas explícitas de expiração.
- Proteção a brute force planejada para autenticação.
- Validação server-side obrigatória em toda entrada.

### API

- autenticação obrigatória por padrão, exceto endpoints públicos estritamente necessários;
- autorização por ação e recurso;
- respostas sem vazamento de internals;
- rate limiting planejado para fases seguintes.

### Credenciais

- segredo protegido em repouso;
- rotação suportada;
- visualização posterior mascarada;
- auditoria para criação, atualização, associação e desativação.

### SSH

- comandos permitidos controlados pelo driver;
- timeout explícito;
- tratamento de erro categorizado;
- política documentada de validação de host key.

## Logging seguro

Logs devem ser suficientes para depuração sem comprometer segredo. Isso significa registrar contexto técnico, correlação, dispositivo, operação e categoria de erro, mas nunca senha, chave privada ou segredo descriptografado.

## Dependências

Django 5.2 recebe manutenção de segurança de longo prazo por ser LTS, o que favorece a escolha para uma base Open Source que precisa de previsibilidade.[page:2][web:12] Ainda assim, releases corretivas do framework devem ser monitoradas continuamente, pois houve correções de segurança relevantes dentro da série 5.2.[web:5][web:13]

## Hardening futuro prioritário

- criptografia detalhada de credenciais;
- rotação de chaves de aplicação;
- secrets management por ambiente;
- rate limit e proteção a abuso de API;
- análise automatizada de dependências no CI;
- resposta a incidentes e playbooks operacionais.
