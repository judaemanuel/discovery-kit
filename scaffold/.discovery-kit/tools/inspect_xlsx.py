# -*- coding: utf-8 -*-
"""
Inspeciona com seguranca planilhas anexas a documentos de entrada do discovery.
NUNCA executa macros. NUNCA abre no Excel. Apenas leitura via openpyxl/zipfile.
Uso: python inspect_xlsx.py <caminho.xlsx|.xlsm> [--sample-rows N]
"""
import sys
import zipfile
import re
from collections import defaultdict

try:
    import openpyxl
except ImportError:
    print("openpyxl nao encontrado")
    sys.exit(1)


def safe_str(v, maxlen=80):
    s = str(v)
    if len(s) > maxlen:
        s = s[:maxlen] + "..."
    return s


def inspect_workbook(path, sample_rows=8, max_formula_cells=25):
    print("=" * 100)
    print(f"ARQUIVO: {path}")
    print("=" * 100)

    # --- estrutura do zip (procura vbaProject.bin) ---
    try:
        with zipfile.ZipFile(path, "r") as z:
            names = z.namelist()
            vba = [n for n in names if "vbaProject" in n]
            print(f"\n[ZIP] Total de entradas: {len(names)}")
            print(f"[ZIP] vbaProject.bin presente: {bool(vba)} -> {vba}")
            sheet_xmls = [n for n in names if n.startswith("xl/worksheets/sheet")]
            print(f"[ZIP] Entradas xl/worksheets/*: {len(sheet_xmls)}")
    except Exception as e:
        print(f"[ZIP] erro ao abrir como zip: {e}")

    # --- workbook com formulas (data_only=False) ---
    wb_f = openpyxl.load_workbook(path, data_only=False, read_only=True)
    print(f"\n[WB] Abas ({len(wb_f.sheetnames)}): {wb_f.sheetnames}")

    # defined names
    try:
        dn = wb_f.defined_names
        keys = list(dn.keys()) if hasattr(dn, "keys") else []
        print(f"\n[DEFINED NAMES] Total: {len(keys)}")
        for k in keys[:60]:
            try:
                dest = dn[k]
                print(f"  - {k} -> {dest.attr_text if hasattr(dest,'attr_text') else dest}")
            except Exception as e:
                print(f"  - {k} -> erro: {e}")
    except Exception as e:
        print(f"[DEFINED NAMES] erro: {e}")

    for sheet_name in wb_f.sheetnames:
        ws = wb_f[sheet_name]
        try:
            dims = ws.dimensions
        except Exception:
            dims = "?"
        print(f"\n--- ABA: {sheet_name} | dimensions={dims} | max_row={ws.max_row} max_col={ws.max_column} ---")

        # amostra: primeiras N linhas
        row_count = 0
        formula_cells = []
        header_row = None
        for row in ws.iter_rows():
            row_count += 1
            if row_count <= sample_rows:
                vals = [(c.coordinate, safe_str(c.value)) for c in row if c.value is not None]
                if vals:
                    print(f"  linha {row_count}: {vals[:15]}")
            # coleta celulas com formula (string comecando com '=')
            for c in row:
                if isinstance(c.value, str) and c.value.startswith("="):
                    if len(formula_cells) < max_formula_cells:
                        formula_cells.append((c.coordinate, c.value))
            if row_count > 3000:  # limite de seguranca por aba para nao explodir tempo
                break

        print(f"  [total linhas percorridas (limitado a 3000): {row_count}]")
        if formula_cells:
            print(f"  [FORMULAS] amostra ({len(formula_cells)} de possivelmente mais):")
            for coord, f in formula_cells:
                print(f"    {coord}: {f}")

    wb_f.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("uso: python inspect_xlsx.py <arquivo>")
        sys.exit(1)
    inspect_workbook(sys.argv[1])
