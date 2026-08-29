#!/usr/bin/env python3
"""Set editable Word text to KaiTi/楷体 without altering document content."""

import argparse
import io
import shutil
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{W_NS}}}"
ET.register_namespace("w", W_NS)


def set_rfonts(rpr):
    rfonts = rpr.find(f"{W}rFonts")
    if rfonts is None:
        rfonts = ET.Element(f"{W}rFonts")
        rpr.insert(0, rfonts)
    rfonts.set(f"{W}ascii", "KaiTi")
    rfonts.set(f"{W}hAnsi", "KaiTi")
    rfonts.set(f"{W}eastAsia", "楷体")
    rfonts.set(f"{W}cs", "KaiTi")


def patch_xml(data):
    for _, namespace in ET.iterparse(io.BytesIO(data), events=("start-ns",)):
        prefix, uri = namespace
        if prefix not in {"xml", "xmlns"}:
            try:
                ET.register_namespace(prefix, uri)
            except ValueError:
                pass
    root = ET.fromstring(data)
    changed = False

    for rpr in root.iter(f"{W}rPr"):
        set_rfonts(rpr)
        changed = True

    for run in root.iter(f"{W}r"):
        if run.find(f"{W}sym") is not None:
            continue
        rpr = run.find(f"{W}rPr")
        if rpr is None:
            rpr = ET.Element(f"{W}rPr")
            run.insert(0, rpr)
        set_rfonts(rpr)
        changed = True

    return ET.tostring(root, encoding="utf-8", xml_declaration=True) if changed else data


def main():
    parser = argparse.ArgumentParser(description="Apply KaiTi/楷体 to editable DOCX text.")
    parser.add_argument("input_docx", type=Path)
    parser.add_argument("output_docx", type=Path)
    args = parser.parse_args()

    if args.input_docx.resolve() == args.output_docx.resolve():
        raise SystemExit("input_docx and output_docx must be different files")
    if not args.input_docx.is_file():
        raise SystemExit(f"input file not found: {args.input_docx}")

    args.output_docx.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as handle:
        temp_path = Path(handle.name)

    try:
        with zipfile.ZipFile(args.input_docx, "r") as source, zipfile.ZipFile(
            temp_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as target:
            for item in source.infolist():
                data = source.read(item.filename)
                if item.filename.startswith("word/") and item.filename.endswith(".xml"):
                    try:
                        data = patch_xml(data)
                    except ET.ParseError:
                        pass
                target.writestr(item, data)
        shutil.move(temp_path, args.output_docx)
    finally:
        temp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
