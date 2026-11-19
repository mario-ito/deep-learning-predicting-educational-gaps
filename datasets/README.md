# Inventário dos datasets

Downloads e preparação realizados em **18 de novembro de 2026**. Os arquivos ZIP originais foram preservados; os CSVs de exploração são derivados desses arquivos e não alteram o conteúdo das fontes.

| Pasta | Fonte primária / versão | Conteúdo local | Licença informada pela fonte |
| --- | --- | --- | --- |
| `unesco_uis/` | [UIS Bulk Data Download](https://databrowser.uis.unesco.org/resources/bulk), `SDG.zip`, edição 2026-11 | ZIP completo; CSVs nacionais, países e rótulos extraídos; recorte de 17 indicadores | [CC BY-SA 3.0 IGO](https://creativecommons.org/licenses/by-sa/3.0/igo/) no README do pacote |
| `inep_ideb/` | [Inep, Ideb 2005–2025, anos iniciais por município](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb/resultados/2005-2025) | ZIP original, XLSX original e CSV em formato longo | Consultar condições da fonte original |
| `oulad/` | [UCI, Open University Learning Analytics Dataset](https://archive.ics.uci.edu/dataset/349/open+university+learning+analytics+dataset), DOI `10.24432/C5KK69` | ZIP completo, seis CSVs menores e dicionário extraídos; a tabela grande `studentVle.csv` está no ZIP | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

## Estrutura dos arquivos preparados

### UIS — `ods4_indicadores_selecionados.csv`

29.004 linhas; 221 países; 17 indicadores; anos presentes de 1970 a 2026. Uma linha representa país, ano e indicador. Campos: `country_id`, `country_name`, `year`, `indicator_id`, `indicator_label_en`, `value`, `magnitude`, `qualifier`. Indicadores selecionados: `ROFST.1.CP`, `ROFST.2.CP`, `ROFST.3.CP`, `CR.1`, `CR.2`, `CR.3`, `READ.PRIMARY`, `MATH.PRIMARY`, `READ.LOWERSEC`, `MATH.LOWERSEC`, `SCHBSP.1.WELEC`, `SCHBSP.1.WINTERN`, `SCHBSP.1.WWATA`, `SCHBSP.1.WWASH`, `SCHBSP.1.WINFSTUDIS`, `TRTP.1`, `TRTP.2`. Foram excluídos somente registros sem valor numérico ou marcados como não aplicáveis/suprimidos/incluídos em outra série. `LOWREL`, `NIL`, `NAT_EST` e `UIS_EST` permanecem identificáveis. Não há duplicatas de país–ano–indicador.

O arquivo `SDG_202611.zip` contém também dados regionais e metadados completos. Para uma análise, conferir definições, cobertura por indicador e a natureza de cada estimativa. A presença de 2026 no pacote não implica cobertura completa de 2026.

### Ideb — `ideb_anos_iniciais_municipios_2005_2025.csv`

159.687 linhas; 5.569 municípios; 11 edições bienais de 2005 a 2025. Uma linha representa município, rede e edição. Campos: `uf`, `codigo_municipio`, `municipio`, `rede`, `ano`, `taxa_aprovacao_1a5_pct`, `indicador_rendimento`, `nota_saeb_matematica`, `nota_saeb_portugues`, `nota_saeb_media_padronizada`, `ideb_observado`. O símbolo `-` da planilha original virou célula vazia. Há 135.332 Ideb observados; 5.196 municípios da rede municipal possuem Ideb observado em **ambas** as edições 2023 e 2025. Não há duplicatas de município–rede–ano. A planilha original contém outras taxas por série e metas, disponíveis para uma análise posterior.

### OULAD — `oulad_uci.zip`

Contém `assessments.csv`, `courses.csv`, `studentAssessment.csv`, `studentInfo.csv`, `studentRegistration.csv`, `studentVle.csv`, `vle.csv` e `OULAD.names`. `studentInfo.csv` tem 32.593 registros de participação em cursos, correspondentes a 28.785 identificadores distintos de estudante. Para uso sequencial, extrair `studentVle.csv` do ZIP quando necessário; o arquivo descompactado tem cerca de 454 MB. Os dados descrevem cursos de 2013–2014, não escolas brasileiras.

## Integridade

Os três ZIPs passaram em `unzip -tq`. A soma MD5 do XLSX do Inep corresponde à soma informada dentro do ZIP oficial.

| Arquivo original | SHA-256 |
| --- | --- |
| `unesco_uis/SDG_202611.zip` | `cb74bb6a8d81f4aed1a173732545954a1ddd09008dbd55a4a14a4036723b0fea` |
| `inep_ideb/divulgacao_anos_iniciais_municipios_2025.zip` | `89100286327ab07a4b1318ba51974d62da90af334f663bedf6374cb67298a3e7` |
| `oulad/oulad_uci.zip` | `f2ed1902616c1fe8d2824d872c0b7d2d72be435bf0124d077044fe4be2c6d3e4` |

## Reprodução dos CSVs

Executar `python scripts/preparar_datasets.py` na raiz da pasta, com `pandas` e um leitor de XLSX instalados. O script lê somente os arquivos oficiais preservados nas respectivas pastas.
