# Casos de Uso

## Objetivo

Este documento descreve os casos de uso centrais do OpenNetManager na Fase 0, servindo como ponte entre a visão de produto e o desenho detalhado de serviços, API e UI.

## Atores

- Administrador
- Operador
- Sistema agendador futuro
- Dispositivo de rede gerenciado

## UC-01 — Autenticar usuário

### Objetivo

Permitir que um usuário autorizado acesse a plataforma conforme seu perfil.

### Fluxo principal

1. Usuário acessa a tela de login.
2. Informa credenciais da plataforma.
3. Sistema autentica e cria sessão.
4. Usuário é redirecionado ao dashboard autorizado.

### Pós-condições

- sessão autenticada criada;
- trilha de auditoria aplicável registrada.

## UC-02 — Cadastrar dispositivo

### Objetivo

Permitir que um administrador registre um dispositivo gerenciado no inventário.

### Fluxo principal

1. Administrador abre formulário de cadastro.
2. Informa nome, vendor, plataforma, host, porta, descrição e estado.
3. Associa ou cria credencial compatível.
4. Sistema valida unicidade e consistência.
5. Sistema persiste o dispositivo.

### Regras relevantes

- cadastro deve refletir vendor e plataforma explicitamente;
- AP130 é apenas um valor inicial possível de plataforma;
- dispositivo inativo não deve ser elegível para coleta operacional normal.

## UC-03 — Registrar credencial

### Objetivo

Permitir criação e associação segura de credenciais para acesso a dispositivos.

### Fluxo principal

1. Administrador abre cadastro de credencial.
2. Informa tipo de autenticação, usuário e segredo associado.
3. Sistema valida o formato mínimo.
4. Sistema protege o segredo e persiste o registro.
5. Credencial torna-se associável a dispositivos.

## UC-04 — Testar conectividade SSH

### Objetivo

Verificar se o sistema consegue estabelecer sessão SSH com um dispositivo usando a credencial associada.

### Fluxo principal

1. Administrador seleciona dispositivo.
2. Solicita teste de conectividade.
3. Serviço resolve dispositivo e credencial.
4. Driver ou gateway executa handshake controlado.
5. Sistema retorna status de sucesso ou falha categorizada.

### Pós-condições

- não há persistência de snapshot por padrão;
- pode haver registro de evento técnico/auditoria.

## UC-05 — Executar coleta manual de snapshot

### Objetivo

Permitir que um usuário autorizado inicie coleta manual de dados operacionais do dispositivo.

### Fluxo principal

1. Usuário solicita coleta.
2. Sistema valida autorização e elegibilidade do dispositivo.
3. Serviço invoca o driver adequado.
4. Driver executa comandos via SSH.
5. Parsers convertem as saídas em objetos estruturados.
6. Serviço persiste snapshot e objetos relacionados.
7. Sistema apresenta resultado ao usuário.

### Regras relevantes

- dashboard não executa SSH diretamente;
- driver não persiste dados;
- parser não conhece conexão;
- falhas parciais devem ser classificadas.

## UC-06 — Visualizar inventário de dispositivos

### Objetivo

Permitir consulta da lista de dispositivos cadastrados com estado e metadados úteis.

### Fluxo principal

1. Usuário acessa a área de dispositivos.
2. Sistema consulta repositório.
3. Lista paginada é apresentada.
4. Usuário pode filtrar e acessar detalhes.

## UC-07 — Visualizar detalhes do dispositivo

### Objetivo

Exibir visão consolidada de metadados, último snapshot, interfaces, clientes suportados e eventos recentes.

### Fluxo principal

1. Usuário acessa a tela de detalhes.
2. Sistema busca dados consolidados em serviços especializados.
3. Dados são organizados para UI.
4. Usuário consulta status e histórico recente.

## UC-08 — Consultar histórico de snapshots

### Objetivo

Permitir inspeção histórica de coletas para análise operacional e auditoria.

### Fluxo principal

1. Usuário abre histórico do dispositivo.
2. Sistema retorna snapshots ordenados.
3. Usuário acessa snapshot específico.
4. Sistema exibe metadados e objetos coletados daquela execução.

## UC-09 — Consumir dados via API

### Objetivo

Permitir acesso programático a inventário, snapshots e dados expostos pela plataforma.

### Fluxo principal

1. Cliente autenticado chama endpoint versionado.
2. Sistema valida autenticação/autorização.
3. Serviço consulta ou processa dados.
4. API retorna payload padronizado.

## UC-10 — Agendar coleta futura

### Objetivo

Criar job de coleta recorrente ou futura, mesmo que a execução completa do scheduler seja entregue em fase posterior.

### Fluxo principal

1. Administrador define dispositivo, tipo de coleta e periodicidade.
2. Sistema valida a configuração.
3. Job é persistido.
4. Mecanismo de scheduler futuro consumirá a configuração.

### Observação

Este caso de uso já orienta modelagem de `CollectionJob`, ainda que a execução automática evolua depois.
