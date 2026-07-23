#!/usr/bin/env python3
import argparse, html, json, os
from collections import defaultdict
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--queue", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--max-per-group", type=int, default=3)
    p.add_argument("--hide-job", action="append", default=[])
    a = p.parse_args()
    data = json.loads(Path(a.queue).read_text(encoding="utf-8-sig"))
    records = data.get("records", data if isinstance(data, list) else [])
    out = Path(a.output); hidden = set(a.hide_job)
    visible = [r for r in records if r.get("target_path") and Path(r["target_path"]).is_file()
               and (r.get("combo_job_id") or r.get("job_id")) not in hidden]
    groups = defaultdict(list)
    for r in visible: groups[str(r.get("outfit_master_id") or r.get("group_id") or "其他")].append(r)
    ordered = []
    while any(groups.values()):
        for group in sorted(groups, key=lambda x: (-len(groups[x]), x)):
            ordered.extend(groups[group][:a.max_per_group]); del groups[group][:a.max_per_group]
    cards = []
    for i, r in enumerate(ordered, 1):
        job = r.get("combo_job_id") or r.get("job_id")
        src = Path(os.path.relpath(r["target_path"], out.parent)).as_posix()
        label = r.get("outfit_master_id") or r.get("group_id") or ""
        cards.append(f'<article><img src="{html.escape(src)}" loading="lazy" onerror="this.closest(\'article\').classList.add(\'broken\')"><b>第{i}张</b><span>{html.escape(str(label))}</span><small>{html.escape(str(job))}</small></article>')
    page = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>批量图片检查页</title>
<style>body{{margin:20px;background:#111;color:#eee;font-family:system-ui}}main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px}}article{{background:#222;padding:10px;border-radius:10px}}img{{width:100%;aspect-ratio:3/4;object-fit:contain;background:#333}}b,span,small{{display:block;margin-top:6px}}small{{color:#999;word-break:break-all}}.broken{{outline:3px solid #f44}}.broken:after{{content:'图片加载失败';color:#f66}}</style></head>
<body><h1>批量图片检查页</h1><p>当前显示 {len(cards)} 张；默认隐藏 {len(hidden)} 项。</p><main>{''.join(cards)}</main></body></html>"""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(json.dumps({"output": str(out.resolve()), "visible": len(cards), "hidden": len(hidden)}, ensure_ascii=False))
if __name__ == "__main__": main()
