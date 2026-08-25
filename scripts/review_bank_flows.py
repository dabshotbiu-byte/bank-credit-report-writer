#!/usr/bin/env python3
"""Create a conservative bank-receipt review workbook from CSV/XLSX exports."""

import argparse
import re
from pathlib import Path

import pandas as pd


ALIASES = {
    "date": ["交易日期", "交易时间", "记账日期", "日期"],
    "credit": ["贷方发生额", "收入金额", "贷方金额", "收入", "转入金额"],
    "amount": ["交易金额", "金额", "发生额"],
    "direction": ["借贷标志", "收支方向", "交易方向", "借贷"],
    "counterparty": ["对方户名", "对手名称", "交易对手", "对方账户名称", "对方名称"],
    "counterparty_account": ["对方账号", "对手账号", "对方账户"],
    "purpose": ["用途", "摘要", "交易摘要", "附言", "备注", "交易用途"],
    "account": ["本方账号", "账号", "银行账号"],
}

RULES = [
    ("内部账户划转", r"内部转账|内部划转|同名划转|资金归集|账户归集|下拨|上划"),
    ("融资款", r"贷款发放|借款|融资款|贴现|保理|票据融资|信用证融资"),
    ("股权或关联方资金", r"投资款|增资|资本金|股东借款|关联方往来|往来款"),
    ("理财赎回", r"理财赎回|理财本金|结构性存款到期|定期存款到期"),
    ("利息", r"结息|存款利息|利息收入"),
    ("退税补贴", r"退税|补贴|补助|政府奖励|财政拨款"),
    ("退款冲正", r"退款|退汇|冲正|撤销|退回"),
    ("保证金及其他非收入", r"保证金|押金|定金退回|保险赔款|赔偿款|代收代付"),
]
SALES = re.compile(r"货款|销售款|服务费|项目款|合同款|结算款|工程款|软件款|运维费|技术服务|产品款")


def pick(columns, key, explicit=None):
    if explicit:
        if explicit not in columns:
            raise SystemExit(f"column not found: {explicit}")
        return explicit
    normalized = {str(c).strip(): c for c in columns}
    for alias in ALIASES[key]:
        if alias in normalized:
            return normalized[alias]
    return None


def amount_series(df, args):
    credit_col = pick(df.columns, "credit", args.credit_col)
    if credit_col:
        return pd.to_numeric(df[credit_col].astype(str).str.replace(",", "", regex=False), errors="coerce").fillna(0)
    amount_col = pick(df.columns, "amount", args.amount_col)
    if not amount_col:
        raise SystemExit("could not detect credit or amount column; pass --credit-col or --amount-col")
    values = pd.to_numeric(df[amount_col].astype(str).str.replace(",", "", regex=False), errors="coerce").fillna(0)
    direction_col = pick(df.columns, "direction", args.direction_col)
    if direction_col:
        direction = df[direction_col].astype(str)
        incoming = direction.str.contains(r"贷|收|入|转入|credit", case=False, regex=True, na=False)
        values = values.where(incoming, 0)
    else:
        values = values.clip(lower=0)
    return values


def classify(text):
    for category, pattern in RULES:
        if re.search(pattern, text, flags=re.I):
            return category, "剔除", f"关键词规则：{category}"
    if SALES.search(text):
        return "销售回款候选", "复核", "需以合同/发票/交付及客户身份交叉验证"
    return "未分类收款", "复核", "摘要不足，逐笔判断"


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
    p.add_argument("--credit-col")
    p.add_argument("--amount-col")
    p.add_argument("--direction-col")
    p.add_argument("--counterparty-col")
    p.add_argument("--purpose-col")
    args = p.parse_args()
    df = read_input(args.input, args.sheet)
    receipts = amount_series(df, args)
    cp_col = pick(df.columns, "counterparty", args.counterparty_col)
    purpose_col = pick(df.columns, "purpose", args.purpose_col)
    combined = (df[cp_col].fillna("").astype(str) if cp_col else pd.Series("", index=df.index)) + " " + (df[purpose_col].fillna("").astype(str) if purpose_col else pd.Series("", index=df.index))
    work = df.loc[receipts > 0].copy()
    work.insert(0, "核查收款金额", receipts.loc[work.index].round(2))
    results = [classify(combined.loc[i]) for i in work.index]
    work.insert(1, "初步分类", [x[0] for x in results])
    work.insert(2, "自动处理建议", [x[1] for x in results])
    work.insert(3, "分类依据", [x[2] for x in results])
    work.insert(4, "复核结论", "")
    work.insert(5, "支持凭证/说明", "")
    summary = work.groupby(["初步分类", "自动处理建议"], dropna=False).agg(笔数=("核查收款金额", "size"), 金额=("核查收款金额", "sum")).reset_index()
    summary.loc[len(summary)] = ["全部收款", "起始总体", len(work), work["核查收款金额"].sum()]
    if cp_col:
        counterparties = work.groupby(cp_col, dropna=False).agg(笔数=("核查收款金额", "size"), 收款金额=("核查收款金额", "sum")).reset_index().sort_values("收款金额", ascending=False)
    else:
        counterparties = pd.DataFrame(columns=["交易对手", "笔数", "收款金额"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(args.output, engine="xlsxwriter") as writer:
        summary.to_excel(writer, sheet_name="分类汇总", index=False)
        work.to_excel(writer, sheet_name="逐笔复核", index=False)
        counterparties.to_excel(writer, sheet_name="交易对手汇总", index=False)
        notes = pd.DataFrame({"使用说明": [
            "自动分类仅用于初筛，不能直接作为授信报告证据。",
            "仅在合同、发票、交付/验收和客户身份相互印证后，将复核结论填写为销售回款。",
            "融资、股东/关联方资金、内部划转、理财赎回、利息、退税补贴、退款及保证金等不计入真实销售回款。",
            "检查重复导入、冲正、支付平台二次结算、跨账户归集和统计期间/主体口径。",
        ]})
        notes.to_excel(writer, sheet_name="说明", index=False)


if __name__ == "__main__":
    main()
