# CI/CD

## Objetivo

Definir a linha mestra da integração contínua e entrega contínua do OpenNetManager na Fase 0.

## Princípios

- toda mudança relevante deve passar por validação automatizada;
- documentação e código são ambos parte do critério de qualidade;
- pipelines devem ser reprodutíveis e compreensíveis;
- a CI deve detectar regressão cedo, especialmente em arquitetura, testes e segurança.

## Etapas mínimas da pipeline

1. Checkout do repositório.
2. Setup da versão alvo do Python.
3. Instalação de dependências.
4. Verificação de formatação com Black.
5. Verificação de imports com isort.
6. Lint com Flake8.
7. Tipagem com mypy.
8. Testes unitários e integração com pytest.
9. Opcionalmente smoke de build Docker.

## Estratégia de banco na CI

- SQLite pode ser usado em checks rápidos locais.
- PostgreSQL deve existir ao menos em pipeline principal de integração.

## Matriz de versões

Django 5.2 suporta Python 3.10 a 3.14, incluindo 3.13, mas o baseline do projeto é Python 3.13.[page:2] Isso permite, no futuro, testar compatibilidade expandida, embora a Fase 0 deva priorizar estabilidade na versão oficial do projeto.[page:2][web:3]

## Gates mínimos para merge

- pipeline verde;
- revisão aprovada;
- documentação atualizada quando aplicável;
- sem vulnerabilidade crítica conhecida introduzida pela mudança.

## Artefatos futuros desejáveis

- relatórios de coverage;
- resultados de testes E2E;
- imagem Docker versionada;
- publicação de documentação estática;
- changelog e release notes automatizados.
