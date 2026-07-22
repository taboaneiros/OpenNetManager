# Visão do Produto

## Declaração de visão

OpenNetManager existe para fornecer uma plataforma Open Source de gerenciamento de dispositivos de rede orientada a múltiplos fabricantes, capaz de transformar acesso operacional fragmentado em uma experiência consistente de inventário, coleta, histórico e observabilidade básica.

## Problema que o produto resolve

Equipes de rede frequentemente dependem de acesso manual via CLI, documentação informal de credenciais, ferramentas isoladas por fabricante e baixa padronização de coleta. Esse contexto eleva o tempo de diagnóstico, reduz rastreabilidade e dificulta a construção de visão centralizada do ambiente.

## Proposta de valor

O OpenNetManager entrega valor por meio de cinco promessas fundamentais:

1. inventário centralizado de dispositivos;
2. coleta remota controlada via SSH;
3. normalização de dados operacionais em estruturas coesas;
4. histórico de snapshots para auditoria e comparação;
5. expansão multi-vendor sem reescrita do núcleo.

## Usuários-alvo

- administradores de rede;
- operadores NOC ou suporte técnico;
- equipes de infraestrutura com ambientes heterogêneos;
- contribuidores Open Source que desejem ampliar suporte a novos vendors.

## Escopo inicial do produto

O escopo inicial cobre o suporte ao AP130 via SSH como primeira implementação concreta da plataforma. O produto deve permitir cadastro de dispositivo, vinculação de credenciais, coleta operacional, persistência dos resultados e visualização via dashboard e API.

## Posição estratégica

O OpenNetManager não pretende nascer como suíte completa de automação de rede, orquestração massiva ou monitoramento em tempo real. O posicionamento inicial é ser uma fundação confiável e extensível para gerenciamento operacional estruturado.

## Diferenciais pretendidos

- arquitetura orientada a vendor abstraction desde o início;
- separação rígida entre transporte, parsing e persistência;
- dashboard server-driven simples de evoluir;
- documentação de engenharia equivalente a projeto Open Source maduro;
- caminho explícito para expansão futura.

## Restrições de visão

- nunca acoplar o núcleo ao AP130;
- nunca permitir lógica de coleta em dashboard;
- nunca misturar parsing com transporte;
- nunca tratar documentação como artefato secundário.

## Métricas de sucesso iniciais

- tempo de onboarding de desenvolvedor senior;
- quantidade de ambiguidades de implementação remanescentes;
- facilidade de adicionar um segundo vendor sem refatoração estrutural;
- confiabilidade dos snapshots persistidos;
- clareza de uso para operador técnico.
