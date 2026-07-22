# Docker

## Objetivo

Definir como o OpenNetManager deve ser empacotado e executado com Docker para garantir consistência de ambiente, onboarding simples e base reprodutível para CI e deployment.

## Papel do Docker no projeto

Docker não é apenas conveniência local; ele é mecanismo de padronização operacional. Em um projeto com Python, Django, banco relacional e futura evolução para componentes adicionais, containerizar cedo reduz drift entre estações, CI e servidores.

## Escopo do empacotamento inicial

O escopo mínimo de containerização deve contemplar:

- aplicação Django;
- banco PostgreSQL para ambientes não locais simplificados;
- volumes necessários;
- variáveis de ambiente externas;
- comando claro de startup.

## Imagem da aplicação

A imagem deve:

- usar base oficial e estável de Python 3.13;
- instalar dependências de forma cacheável;
- separar dependências de sistema das de aplicação;
- rodar processo com usuário não privilegiado quando viável;
- minimizar artefatos desnecessários.

## Estratégia de build

Recomenda-se multi-stage build quando fizer sentido para reduzir tamanho final e separar fases de compilação, testes e runtime. O trade-off é um Dockerfile mais sofisticado, porém com imagem final menor e mais segura.

## Docker Compose

Para desenvolvimento e homologação simples, `docker compose` é adequado para subir:

- app web;
- PostgreSQL;
- componentes futuros opcionais como Redis.

## Volumes e persistência

- banco precisa de volume persistente em ambientes duráveis;
- código fonte pode ser montado em desenvolvimento local;
- arquivos temporários e estáticos devem ter política clara por ambiente.

## Segurança do container

- não embutir segredos na imagem;
- usar variáveis de ambiente ou mecanismo de secrets por ambiente;
- reduzir privilégios do usuário de runtime;
- manter imagem base atualizada;
- evitar ferramentas desnecessárias no runtime final.

## Health checks

A imagem ou composição de serviço deve prever health check da aplicação para apoiar CI e deploy mais confiável.

## Trade-offs

### Compose simples versus orquestração complexa

`docker compose` atende bem a Fase 0 porque o sistema é um monólito modular com poucos componentes. Adotar orquestração pesada cedo aumentaria custo operacional sem benefício proporcional imediato.

### Imagem única versus perfis múltiplos

Uma imagem única simplifica o pipeline inicial. Perfis separados para web, worker e scheduler só fazem mais sentido quando as funções realmente se descolarem em fases futuras.
