"""Prepara recortes de exploração a partir dos arquivos oficiais preservados em datasets/."""

from __future__ import annotations

import csv
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
UIS = ROOT / "datasets" / "unesco_uis"
INEP = ROOT / "datasets" / "inep_ideb"

INDICATORS = [
    "ROFST.1.CP", "ROFST.2.CP", "ROFST.3.CP",
    "CR.1", "CR.2", "CR.3",
    "READ.PRIMARY", "MATH.PRIMARY", "READ.LOWERSEC", "MATH.LOWERSEC",
    "SCHBSP.1.WELEC", "SCHBSP.1.WINTERN", "SCHBSP.1.WWATA",
    "SCHBSP.1.WWASH", "SCHBSP.1.WINFSTUDIS",
    "TRTP.1", "TRTP.2",
]


def prepare_uis() -> None:
    with (UIS / "SDG_COUNTRY.csv").open(encoding="utf-8-sig", newline="") as f:
        countries = {r["COUNTRY_ID"]: r["COUNTRY_NAME_EN"] for r in csv.DictReader(f)}
    with (UIS / "SDG_LABEL.csv").open(encoding="utf-8-sig", newline="") as f:
        labels = {r["INDICATOR_ID"]: r["INDICATOR_LABEL_EN"].strip() for r in csv.DictReader(f)}

    out = UIS / "ods4_indicadores_selecionados.csv"
    fields = ["country_id", "country_name", "year", "indicator_id", "indicator_label_en",
              "value", "magnitude", "qualifier"]
    count = 0
    with (UIS / "SDG_DATA_NATIONAL.csv").open(encoding="utf-8-sig", newline="") as src, \
         out.open("w", encoding="utf-8", newline="") as dst:
        writer = csv.DictWriter(dst, fieldnames=fields)
        writer.writeheader()
        for r in csv.DictReader(src):
            if r["INDICATOR_ID"] not in INDICATORS or not r["VALUE"]:
                continue
            # No arquivo UIS, NA pode vir como zero, mas significa "não aplicável".
            if r["MAGNITUDE"] in {"NA", "SUPP", "INCLUDED"}:
                continue
            writer.writerow({
                "country_id": r["COUNTRY_ID"],
                "country_name": countries.get(r["COUNTRY_ID"], ""),
                "year": r["YEAR"],
                "indicator_id": r["INDICATOR_ID"],
                "indicator_label_en": labels[r["INDICATOR_ID"]],
                "value": r["VALUE"],
                "magnitude": r["MAGNITUDE"],
                "qualifier": r["QUALIFIER"],
            })
            count += 1
    print(f"UIS: {count:,} observações -> {out}")


def prepare_ideb() -> None:
    src = INEP / "divulgacao_anos_iniciais_municipios_2025" / "divulgacao_anos_iniciais_municipios_2025.xlsx"
    wide = pd.read_excel(src, header=9, dtype={"CO_MUNICIPIO": "string"})
    wide = wide[wide["CO_MUNICIPIO"].str.fullmatch(r"\d{7}", na=False)].copy()
    wide["CO_MUNICIPIO"] = wide["CO_MUNICIPIO"].astype(str)

    base_cols = ["SG_UF", "CO_MUNICIPIO", "NO_MUNICIPIO", "REDE"]
    metrics = {
        "VL_APROVACAO_{year}_SI_4": "taxa_aprovacao_1a5_pct",
        "VL_INDICADOR_REND_{year}": "indicador_rendimento",
        "VL_NOTA_MATEMATICA_{year}": "nota_saeb_matematica",
        "VL_NOTA_PORTUGUES_{year}": "nota_saeb_portugues",
        "VL_NOTA_MEDIA_{year}": "nota_saeb_media_padronizada",
        "VL_OBSERVADO_{year}": "ideb_observado",
    }
    frames = []
    for year in range(2005, 2026, 2):
        cols = {template.format(year=year): name for template, name in metrics.items()}
        frame = wide[base_cols + list(cols)].rename(columns=cols).copy()
        frame.insert(4, "ano", year)
        for col in cols.values():
            frame[col] = pd.to_numeric(frame[col].replace("-", pd.NA), errors="coerce")
        frames.append(frame)

    tidy = pd.concat(frames, ignore_index=True)
    tidy = tidy.rename(columns={
        "SG_UF": "uf", "CO_MUNICIPIO": "codigo_municipio",
        "NO_MUNICIPIO": "municipio", "REDE": "rede",
    })
    out = INEP / "ideb_anos_iniciais_municipios_2005_2025.csv"
    tidy.to_csv(out, index=False, encoding="utf-8", float_format="%.9g")
    print(f"Ideb: {len(tidy):,} linhas, {tidy['codigo_municipio'].nunique():,} municípios -> {out}")


if __name__ == "__main__":
    prepare_uis()
    prepare_ideb()
