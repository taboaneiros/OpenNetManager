# Parsers

## Objetivo

Definir a estratégia de parsing do OpenNetManager para transformar saídas textuais heterogêneas de dispositivos em objetos de domínio consistentes, rastreáveis e testáveis.

## Papel do parser

O parser recebe saída textual bruta e contexto do comando e devolve estruturas de domínio ou falhas semânticas explícitas. Ele não abre conexão, não consulta banco, não acessa request HTTP e não toma decisões de autorização.

## Princípios

- parser faz uma coisa: interpretar texto em estrutura;
- parsing deve ser determinístico para uma mesma entrada;
- falhas devem ser explícitas, não silenciosas;
- fixtures reais de CLI são parte obrigatória da estratégia de manutenção;
- diferenças por firmware ou command flavor devem ser tratadas de forma consciente.

## Tipos de parser sugeridos

- `SystemInfoParser`
- `InterfaceParser`
- `ClientParser`
- `EventParser` futuro

## Contrato conceitual

Entrada:

- texto bruto;
- metadados do contexto (vendor, plataforma, comando, versão quando conhecida).

Saída:

- objeto de domínio;
- coleção de objetos;
- exceção de parsing semanticamente útil.

## Estratégias recomendadas

- preferir parsing orientado a estrutura previsível e tokens estáveis;
- usar regex com parcimônia e documentação quando necessária;
- validar campos críticos;
- normalizar formatos antes de construir objetos finais;
- registrar parsing parcial quando o dado permitir uso seguro limitado.

## Parser e qualidade de dados

O parser é a principal barreira entre texto externo não confiável e o modelo interno do sistema. Por isso ele deve ser conservador: melhor sinalizar dado inválido do que popular a base com informações incorretas e aparentemente válidas.

## Trade-offs

### Parsing tolerante versus parsing estrito

Parsing tolerante reduz falhas imediatas, mas pode mascarar mudanças silenciosas de firmware e corromper a qualidade dos dados. Parsing estrito aumenta barulho operacional no curto prazo, porém protege a integridade semântica do sistema. O OpenNetManager deve preferir estrito com fallback consciente para casos explicitamente suportados.

### Normalização precoce versus preservação total do raw

Normalizar cedo ajuda services e API, mas pode perder nuances de debug. Por isso recomenda-se estratégia controlada para retenção opcional de raw output em contexto técnico protegido.
