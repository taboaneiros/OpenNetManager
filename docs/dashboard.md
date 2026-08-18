# Dashboard Operacional

## Objetivo

O dashboard oferece visão rápida e acionável do ambiente de access points. Ele consulta dados persistidos e não acessa SSH diretamente.

## Indicadores principais

- APs online e offline.
- Total de clientes.
- SSIDs ativos.
- Taxa total de upload.
- Taxa total de download.
- Rádios degradados.
- Interfaces down.
- Falhas de coleta.
- APs sem atualização recente.
- Última coleta e timestamp da informação.

## Visões recomendadas

### Clientes

- Clientes por AP.
- Clientes por SSID.
- Clientes por banda.
- Clientes com pior sinal.
- Clientes com maior tráfego.
- Entradas, saídas e alterações recentes.

### SSIDs

- Top 5 por quantidade de clientes.
- Top 5 por download.
- Top 5 por upload.
- Top 5 por tráfego total.
- Evolução de clientes por período.

### Access points

- Top APs por clientes.
- Top APs por tráfego.
- APs com maior número de eventos.
- APs com falha de coleta.
- APs sem atualização.

### Saúde

- Sinal médio e distribuição de RSSI.
- Rádios down.
- Interfaces down.
- Falhas de autenticação quando disponíveis.
- Crescimento de desconexões.
- Dispositivos em reconexão.

## Taxas e janelas

Upload e download devem indicar a janela de coleta, por exemplo taxa instantânea reportada pelo device, média da última coleta ou agregação de cinco minutos. Não misturar métricas com janelas diferentes sem indicação visual.

## Atualidade

Cada card ou gráfico deve possuir timestamp ou referência ao horário da última coleta. O dashboard não deve representar dados históricos como telemetria em tempo real.

## Ações

O dashboard pode direcionar para:

- detalhe do dispositivo;
- executar coleta manual;
- diagnóstico;
- logs;
- configuração;
- clientes;
- eventos;
- histórico de snapshots.

A execução efetiva deve passar por services e políticas de autorização.

## UX

- Destacar falhas e itens que exigem ação.
- Diferenciar leitura de alteração.
- Mostrar capability ausente de forma clara.
- Não expor segredos.
- Exibir origem servidor/device em diagnósticos.
- Confirmar operações destrutivas antes da execução.
