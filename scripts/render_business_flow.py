#!/usr/bin/env python3
"""Render a simple SVG business flow with red fund arrows and black delivery arrows."""

import argparse
import html
import json
import math
from pathlib import Path


def esc(value):
    return html.escape(str(value), quote=True)


def wrap_label(text, limit=12):
    text = str(text)
    return [text[i:i + limit] for i in range(0, len(text), limit)] or [""]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_svg", type=Path)
    args = parser.parse_args()
    spec = json.loads(args.input_json.read_text(encoding="utf-8"))
    nodes = spec.get("nodes", [])
    edges = spec.get("edges", [])
    if not nodes:
        raise SystemExit("nodes must not be empty")
    ids = [n["id"] for n in nodes]
    if len(ids) != len(set(ids)):
        raise SystemExit("node ids must be unique")
    known = set(ids)
    for edge in edges:
        if edge.get("from") not in known or edge.get("to") not in known:
            raise SystemExit(f"edge references unknown node: {edge}")
        if edge.get("type") not in {"funds", "goods", "info"}:
            raise SystemExit(f"edge type must be funds, goods, or info: {edge}")

    width, height = 1100, 620
    cx, cy = width / 2, height / 2 + 20
    rx, ry = 390, 205
    positions = {}
    count = len(nodes)
    for i, node in enumerate(nodes):
        angle = -math.pi / 2 + 2 * math.pi * i / count
        positions[node["id"]] = (cx + rx * math.cos(angle), cy + ry * math.sin(angle))

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    svg.append('<rect width="100%" height="100%" fill="#ffffff"/>')
    svg.append('<defs><marker id="arrow-red" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#d7191c"/></marker><marker id="arrow-black" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#111111"/></marker><marker id="arrow-grey" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#777777"/></marker></defs>')
    svg.append(f'<text x="{width/2}" y="42" text-anchor="middle" font-family="KaiTi, STKaiti, 楷体, serif" font-size="25" font-weight="700" fill="#222">{esc(spec.get("title", "业务模式图"))}</text>')

    for index, edge in enumerate(edges):
        x1, y1 = positions[edge["from"]]
        x2, y2 = positions[edge["to"]]
        dx, dy = x2 - x1, y2 - y1
        dist = max(math.hypot(dx, dy), 1)
        ux, uy = dx / dist, dy / dist
        start_x, start_y = x1 + ux * 88, y1 + uy * 42
        end_x, end_y = x2 - ux * 88, y2 - uy * 42
        kind = edge["type"]
        color = {"funds": "#d7191c", "goods": "#111111", "info": "#777777"}[kind]
        marker = {"funds": "arrow-red", "goods": "arrow-black", "info": "arrow-grey"}[kind]
        dash = ' stroke-dasharray="7 5"' if kind == "info" else ""
        offset = ((index % 3) - 1) * 16
        mx, my = (start_x + end_x) / 2 - uy * offset, (start_y + end_y) / 2 + ux * offset
        svg.append(f'<line x1="{start_x:.1f}" y1="{start_y:.1f}" x2="{end_x:.1f}" y2="{end_y:.1f}" stroke="{color}" stroke-width="3"{dash} marker-end="url(#{marker})"/>')
        svg.append(f'<rect x="{mx-65:.1f}" y="{my-13:.1f}" width="130" height="24" rx="5" fill="#ffffff" fill-opacity="0.90"/>')
        svg.append(f'<text x="{mx:.1f}" y="{my+5:.1f}" text-anchor="middle" font-family="KaiTi, STKaiti, 楷体, serif" font-size="14" fill="{color}">{esc(edge.get("label", ""))}</text>')

    for node in nodes:
        x, y = positions[node["id"]]
        fill = node.get("fill", "#eef3f8")
        svg.append(f'<rect x="{x-90:.1f}" y="{y-43:.1f}" width="180" height="86" rx="13" fill="{esc(fill)}" stroke="#46637f" stroke-width="2"/>')
        lines = wrap_label(node.get("label", node["id"]))
        base = y - (len(lines) - 1) * 10
        for j, line in enumerate(lines):
            svg.append(f'<text x="{x:.1f}" y="{base + j*22:.1f}" text-anchor="middle" dominant-baseline="middle" font-family="KaiTi, STKaiti, 楷体, serif" font-size="17" font-weight="600" fill="#203040">{esc(line)}</text>')

    svg.append('<line x1="300" y1="586" x2="355" y2="586" stroke="#d7191c" stroke-width="3" marker-end="url(#arrow-red)"/><text x="370" y="591" font-family="KaiTi, STKaiti, 楷体, serif" font-size="14" fill="#d7191c">资金流</text>')
    svg.append('<line x1="520" y1="586" x2="575" y2="586" stroke="#111111" stroke-width="3" marker-end="url(#arrow-black)"/><text x="590" y="591" font-family="KaiTi, STKaiti, 楷体, serif" font-size="14" fill="#111111">货物/服务/数据流</text>')
    svg.append('</svg>')
    args.output_svg.parent.mkdir(parents=True, exist_ok=True)
    args.output_svg.write_text("\n".join(svg), encoding="utf-8")


if __name__ == "__main__":
    main()
