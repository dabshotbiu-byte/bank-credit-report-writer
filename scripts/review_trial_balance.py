#!/usr/bin/env python3
"""Rank trial-balance accounts and produce top-five child-account workpapers."""

import argparse
from pathlib import Path

import pandas as pd


ALIASES = {
    "code": ["科目编码", "科目代码", "会计科目编码", "编码"],
    "name": ["科目名称", "会计科目", "账户名称", "名称"],
    "opening_debit": ["期初借方余额", "期初借方"],
    "opening_credit": ["期初贷方余额", "期初贷方"],
    "closing_debit": ["期末借方余额", "期末借方"],
    "closing_credit": ["期末贷方余额", "期末贷方"],
    "period_debit": ["本期借方发生额", "本期借方", "借方发生额"],
    "period_credit": ["本期贷方发生额", "本期贷方", "贷方发生额"],
}
CLASSES = {"1": "资产", "2": "负债", "3": "共同", "4": "所有者权益", "5": "成本", "6": "损益"}


def pick(columns, key, explicit=None, required=True):
    if explicit:
        if explicit not in columns:
            raise SystemExit(f"column not found: {explicit}")
        return explicit
    normalized = {str(c).strip(): c for c in columns}
    for alias in ALIASES[key]:
        if alias in normalized:
            return normalized[alias]
    if required:
        raise SystemExit(f"could not detect {key} column; pass the matching --*-col option")
    return None


def numeric(df, col):
    if not col:
        return pd.Series(0.0, index=df.index)
    return pd.to_numeric(df[col].astype(str).str.replace(",", "", regex=False), errors="coerce").fillna(0.0)


def read_input(path, sheet):
    if path.suffix.lower() == ".csv":
        for encoding in ("utf-8-sig", "gb18030", "utf-8"):
            try:
                return pd.read_csv(path, encoding=encoding)
            except UnicodeDecodeError:
                pass
        raise SystemExit("unable to decode CSV")
    return pd.read_excel(path, sheet_name=sheet)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--sheet", default=0)
    p.add_argument("--parent-digits", type=int, default=4)
    for key in ALIASES:
        p.add_argument(f"--{key.replace('_', '-')}-col")
    args = p.parse_args()
    df = read_input(args.input, args.sheet)
    cols = {key: pick(df.columns, key, getattr(args, f"{key}_col"), required=key in {"code", "name"}) for key in ALIASES}
    code = df[cols["code"]].astype(str).str.replace(r"\.0$", "", regex=True).str.strip()
    out = df.copy()
    out.insert(0, "科目大类", code.str[:1].map(CLASSES).fillna("其他"))
    out.insert(1, "父级科目编码", code.str[:args.parent_digits])
    out.insert(2, "标准科目编码", code)
    opening = numeric(df, cols["opening_debit"]) - numeric(df, cols["opening_credit"])
    closing = numeric(df, cols["closing_debit"]) - numeric(df, cols["closing_credit"])
    out["期初净额"] = opening.round(2)
    out["本期借方发生额_标准"] = numeric(df, cols["period_debit"]).round(2)
    out["本期贷方发生额_标准"] = numeric(df, cols["period_credit"]).round(2)
    out["期末净额"] = closing.round(2)
    out["期末绝对额"] = closing.abs().round(2)
    out["变动额"] = (closing - opening).round(2)
    out["变动率"] = ((closing - opening) / opening.abs().replace(0, pd.NA)).astype("Float64")
    leaf = out.loc[code.str.len() > args.parent_digits].copy()
    leaf["父级内排名"] = leaf.groupby("父级科目编码")["期末绝对额"].rank(method="first", ascending=False)
    top_children = leaf.loc[leaf["父级内排名"] <= 5].sort_values(["父级科目编码", "父级内排名"])
    top_accounts = out.sort_values(["科目大类", "期末绝对额"], ascending=[True, False]).groupby("科目大类", group_keys=False).head(5)
    movements = out.reindex(out["变动额"].abs().sort_values(ascending=False).index).head(30)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(args.output, engine="xlsxwriter") as writer:
        top_accounts.to_excel(writer, sheet_name="各类前五大科目", index=False)
        top_children.to_excel(writer, sheet_name="重大科目前五明细", index=False)
        movements.to_excel(writer, sheet_name="重大变动", index=False)
        out.to_excel(writer, sheet_name="标准化科目余额表", index=False)
        pd.DataFrame({"使用说明": [
            "按科目编码首位划分大类，使用前确认企业科目编码体系。",
            "父级科目默认取前4位；如企业编码层级不同，使用 --parent-digits 调整。",
            "期末绝对额和变动排名只用于筛选，报告仍需结合总资产/收入占比、关联方、账龄、受限和异常交易判断重大性。",
            "前五明细应与总账、明细账、账龄表、合同、发票及期后收付交叉验证。",
        ]}).to_excel(writer, sheet_name="说明", index=False)


if __name__ == "__main__":
    main()
