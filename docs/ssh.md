# SSH

## Objetivo

Definir como a camada SSH do OpenNetManager deve operar para garantir integração segura, previsível e desacoplada com dispositivos gerenciados.

## Papel da camada SSH

A camada SSH é um adaptador de transporte. Sua função é conectar, autenticar, executar comandos e devolver saídas brutas ou falhas técnicas normalizadas. Ela não interpreta semântica do dispositivo, não persiste dados e não conhece regras de negócio.

## Tecnologia base

A stack definida adota Paramiko como biblioteca SSH principal. A escolha decorre de maturidade do ecossistema Python e adequação a um backend Django que precisa estabelecer sessões remotas controladas.

## Responsabilidades

- abrir e encerrar sessão SSH;
- aplicar timeouts e política de retry definidos;
- executar comandos permitidos pelo driver;
- retornar stdout/stderr e metadados úteis;
- mapear erros de biblioteca para exceções do projeto.

## Políticas recomendadas

### Timeouts

Devem existir timeouts explícitos para:

- conexão;
- autenticação;
- execução de comando;
- operação total da coleta, quando aplicável.

### Retries

Retries devem ser limitados, conscientes e preferencialmente centralizados. Retry indiscriminado pode piorar indisponibilidade e mascarar problemas reais.

### Host key verification

Deve haver política documentada por ambiente. Em produção, a validação de host key deve ser tratada com rigor significativamente maior do que em ambientes de desenvolvimento controlado.

## Comandos

Comandos não devem ser montados a partir de entrada arbitrária do usuário final. O conjunto de comandos executáveis deve ser controlado pelos drivers e versionado como parte da integração suportada.

## Trade-offs

### SSH genérico livre versus comando controlado

Permitir comandos arbitrários parece útil para troubleshooting, mas amplia superfície de risco, mistura responsabilidades e compromete previsibilidade. O OpenNetManager deve começar com escopo estritamente controlado por driver.
