# Plano de dados e deep learning para educação

**Data da pesquisa:** 18 de novembro de 2026  
**Referência:** [ODS 4 — ONU Brasil](https://brasil.un.org/pt-br/sdgs/4), especialmente as metas 4.1 (aprendizagem e conclusão), 4.5 (equidade), 4.a (ambiente escolar) e 4.c (docentes).

## Decisão inicial

A opção mais útil para **propor uma ação no Brasil** é prever quais municípios têm maior risco de piora ou de baixo desempenho nos anos iniciais do ensino fundamental, usando a série histórica do **Ideb do Inep**. A base **UNESCO/UIS**, órgão da ONU, dá o enquadramento oficial do ODS 4 e permite comparar o Brasil com outros países. Se o requisito central for demonstrar uma arquitetura de deep learning sequencial com muitos registros, o **OULAD** é tecnicamente mais adequado, mas retrata ensino superior a distância no Reino Unido e não deve ser usado para inferir resultados brasileiros.

## Possibilidades encontradas

| Caminho | Fonte e dados | Unidade / uso em modelo | Ação educacional possível | Situação e limite principal |
| --- | --- | --- | --- | --- |
| **1. ODS 4 internacional** | [UNESCO/UIS, pacote oficial de indicadores](https://databrowser.uis.unesco.org/resources/bulk) | País × ano × indicador; previsão de exclusão escolar, conclusão ou lacunas de aprendizagem | Priorizar cooperação, formação docente ou conectividade nos países com maiores lacunas verificadas | **Baixado.** Comparável internacionalmente, mas agregado demais para escolher escolas; proficiência de leitura e matemática tem menos observações que matrícula/conclusão. |
| **2. Ideb municipal, Brasil** | [Inep, resultados Ideb 2005–2025](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb/resultados/2005-2025) | Município × rede × edição bienal; prever Ideb ou queda na edição seguinte | Priorizar diagnóstico e apoio pedagógico em municípios com risco alto e resultados persistentemente baixos | **Baixado e convertido para CSV.** Não traz, por si só, as causas nem o efeito de uma intervenção. |
| **3. Escola e infraestrutura, Brasil** | [Censo Escolar do Inep](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar), [Ideb por escola](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb/resultados/2005-2025), [indicadores educacionais](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais) | Escola × ano; combinar estrutura, docentes, fluxo e aprendizagem | Encaminhar apoio pedagógico, melhorias de infraestrutura ou formação docente conforme a necessidade observada | **Catalogado para a próxima etapa.** Exige integração por código de escola, conferência de cobertura e arquivos maiores. |
| **4. Alerta precoce de evasão em curso on-line** | [OULAD, Open University / UCI](https://archive.ics.uci.edu/dataset/349/open+university+learning+analytics+dataset) | Estudante × sequência diária/semanal de interações; prever desistência durante o curso | Oferecer tutoria e contato humano a estudantes com risco de desistir | **Baixado.** É um cenário internacional, antigo e de ensino superior on-line; requer cuidado com privacidade e com informações posteriores ao alerta. |
| **5. Equidade educacional global** | [UNICEF, educação primária](https://data.unicef.org/resources/dataset/primary-education-data/) e [secundária](https://data.unicef.org/resources/dataset/secondary-education-data/) | País / grupo social × ano; disparidades de frequência, conclusão e acesso digital | Direcionar busca ativa e inclusão para grupos com pior cobertura | **Catalogado.** Indicadores agregados; deve-se medir disponibilidade por país/grupo antes de treinar. |
| **6. Base global de indicadores da ONU** | [UN Statistics Division, indicadores ODS](https://unstats.un.org/sdgs/indicators/en/) | País × ano × série ODS; alternativa para harmonizar metas 4.1–4.c | Monitorar progresso e comparar prioridades nacionais | **Catalogado.** Há sobreposição com UIS; usar uma única definição de indicador por análise. |

**Kaggle:** não foi necessário, pois há dados oficiais da UNESCO/ONU e do Inep. Uma cópia de Kaggle só faria sentido após conferir versão, origem e licença contra a fonte primária.

## Arquivos já salvos

- `datasets/unesco_uis/SDG_202611.zip`: pacote oficial completo do ODS 4 da UIS, edição de novembro de 2026.
- `datasets/unesco_uis/ods4_indicadores_selecionados.csv`: recorte legível com **29.004 observações**, **221 países** e **17 indicadores** de acesso, conclusão, aprendizagem, infraestrutura e formação docente. Mantém as marcações de estimativa e de qualidade.
- `datasets/inep_ideb/divulgacao_anos_iniciais_municipios_2025.zip`: planilha oficial do Ideb municipal dos anos iniciais.
- `datasets/inep_ideb/ideb_anos_iniciais_municipios_2005_2025.csv`: série em formato longo com **159.687 linhas**, **5.569 municípios** e edições bienais de 2005 a 2025. Inclui aprovação, rendimento, notas do Saeb e Ideb observado, para redes municipal, estadual, federal e pública.
- `datasets/oulad/oulad_uci.zip`: dataset completo com registros de interação no ambiente virtual. Tabelas menores já extraídas em `datasets/oulad/`; `studentVle.csv` (cerca de 454 MB descompactado) permanece dentro do ZIP.

Detalhes de origem, campos e integridade estão em [`datasets/README.md`](datasets/README.md). O script [`scripts/preparar_datasets.py`](scripts/preparar_datasets.py) reproduz os dois CSVs preparados.

## Projeto recomendado: priorização de apoio pedagógico municipal

1. **Pergunta:** quais municípios da rede municipal têm maior risco de Ideb baixo ou de queda na próxima edição, com base apenas em dados disponíveis antes dessa edição?
2. **Desfecho:** Ideb observado na edição seguinte; analisar também queda relevante e distância para municípios comparáveis. Definir limiar de ação com gestores, antes do treino.
3. **Entradas:** histórico de Ideb, aprovação e notas do Saeb até a edição anterior; município e rede. Para recomendações específicas, acrescentar Censo Escolar, indicadores de docentes, infraestrutura e contexto socioeconômico, sempre de anos anteriores ao desfecho.
4. **Modelos:** começar com persistência histórica, regressão e árvores de decisão como referências; comparar uma rede neural para dados tabulares ou temporais. Com somente 11 edições por município, deep learning pode não superar modelos simples. Documentar esse resultado se ocorrer.
5. **Validação:** separar edições posteriores para teste, evitar informação futura, avaliar erro de previsão e calibração do risco, e comparar desempenho por região e perfil municipal. Repetir a avaliação apenas nos municípios com dados observados, reportando a cobertura e as ausências.
6. **Ação:** entregar uma lista auditável de municípios para diagnóstico local, com indicadores que motivaram a prioridade. Selecionar reforço em leitura/matemática, formação docente ou melhoria da estrutura somente após confirmar a necessidade nos dados adicionais e com os gestores. Medir depois se a ação melhorou resultados; previsão isolada não prova causalidade.

## Alternativa se o foco do trabalho for a arquitetura de deep learning

No OULAD, agregar `studentVle.csv` por semana e combinar com avaliações já concluídas até a **semana 4**. Treinar uma rede temporal para prever desistência posterior; comparar com regressão logística e árvore/boosting; testar em apresentações de curso não usadas no treino. A saída acionável seria uma oferta de tutoria, com revisão humana, não uma decisão automática sobre o estudante. Esse estudo demonstra melhor o uso de deep learning, porém sua aplicação direta ao ODS 4 no Brasil é limitada.

## Próximas entregas após escolher a trilha

1. Dicionário de dados e análise de lacunas, duplicatas e representatividade.
2. Definição do desfecho, do momento de previsão e da intervenção que a instituição conseguiria executar.
3. Base de treino sem vazamento temporal, modelos de referência e modelo de deep learning.
4. Avaliação em período posterior, explicação dos resultados e proposta de ação com critérios transparentes.

**Observação metodológica:** indicadores da UIS incluem estimativas (`NAT_EST`, `UIS_EST`) e podem ter anos recentes incompletos; o recorte preserva essas marcações. O Ideb é composto por aprendizagem e fluxo escolar, portanto usar notas do Saeb ou aprovação do **mesmo ano** para prever o Ideb daquele ano produziria vazamento de informação. Para decisões sobre 2027, usar somente informações que já estavam disponíveis até o momento da decisão.
