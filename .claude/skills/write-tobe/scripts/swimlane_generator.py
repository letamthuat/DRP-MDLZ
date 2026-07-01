#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sinh sơ đồ swimlane phong cách Smartlog → HTML → PNG.

Dùng:
    python swimlane_generator.py <input.json> [-o output_dir]
    python swimlane_generator.py --capture-only <input.html> [-o output.png]

Logic cache:
    - Nếu <name>.png đã tồn tại VÀ <name>.html không thay đổi → dùng lại PNG, không render lại.
    - Chỉ render lại khi HTML mới hơn PNG.

Yêu cầu: pip install playwright && python -m playwright install chromium
"""

import sys, os, json, hashlib, re

# ---------- DATA STRUCTURES ----------
# Input JSON schema:
# {
#   "title": "Tên quy trình",
#   "lanes": ["Lane 1", "Lane 2", ...],
#   "nodes": [
#     {"id": "n1", "lane": 0, "type": "start|end|process|decision", "label": "...", "note": "..."},
#     ...
#   ],
#   "edges": [
#     {"from": "n1", "to": "n2", "label": ""},
#     ...
#   ]
# }

HEADER_COLOR = "#176bb4"
LANE_HEADER_FILL = "#eef1f5"   # nền header lane (đồng nhất mọi lane)
LANE_BODY_FILL = "#ffffff"     # nền thân lane (đồng nhất, trắng)
LANE_DIVIDER = "#9e9e9e"       # đường phân chia lane: xám mờ, đủ rõ nhưng không quá đậm
SHAPE_FILL = "#ffffff"
SHAPE_STROKE = "#333333"
DECISION_FILL = "#ffffff"
NOTE_COLOR = "#cc0000"
ARROW_COLOR = "#444444"
FONT = "Times New Roman, serif"


def build_html(data: dict) -> str:
    title = data.get("title", "Sơ đồ quy trình")
    lanes = data.get("lanes", [])
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    n_lanes = len(lanes)
    lane_w = data.get("lane_w", 305)   # cho phép override bề ngang lane theo từng sơ đồ (vd lane đơn cho rộng hơn)
    total_w = n_lanes * lane_w + 60
    row_h = data.get("row_h", 175)     # cao thoải mái (chiều cao không ảnh hưởng cỡ chữ vì ảnh vừa theo bề ngang)
    header_h = 56
    title_h = 48
    padding = 16

    # kích thước node (chữ lớn; auto-wrap nhiều dòng để không tràn khung)
    # process box nở theo bề ngang lane để không bị "ốm" trong lane rộng
    PROC_W, PROC_H  = lane_w - 35, 124  # process box
    DEC_HW, DEC_HH  = 118, 70   # decision half-width/height
    OVAL_RX, OVAL_RY = 112, 60  # start/end ellipse
    NODE_FONT = 20              # cỡ chữ trong node
    proc_mc = max(8, int((PROC_W - 18) / (NODE_FONT * 0.5)))  # số ký tự tối đa mỗi dòng (auto-wrap)
    dec_mc  = max(6, int((DEC_HW * 1.5) / (NODE_FONT * 0.5)))
    oval_mc = max(6, int((OVAL_RX * 1.5) / (NODE_FONT * 0.5)))

    # row: ưu tiên lấy từ JSON, fallback tính topological
    node_map = {n["id"]: n for n in nodes}
    row_assigned = {}

    # nếu node có field "row" → dùng thẳng
    has_explicit_rows = all("row" in n for n in nodes)
    if has_explicit_rows:
        for n in nodes:
            row_assigned[n["id"]] = n["row"]
    else:
        visited = set()
        def assign_rows(nid, row):
            if nid in visited:
                return
            visited.add(nid)
            if nid not in row_assigned or row_assigned[nid] < row:
                row_assigned[nid] = row
            children = [e["to"] for e in edges if e["from"] == nid]
            for c in children:
                assign_rows(c, row_assigned[nid] + 1)
        starts = [n["id"] for n in nodes if n.get("type") == "start"]
        if not starts:
            starts = [nodes[0]["id"]] if nodes else []
        for s in starts:
            assign_rows(s, 0)
        for n in nodes:
            if n["id"] not in row_assigned:
                row_assigned[n["id"]] = max(row_assigned.values(), default=0) + 1

    max_row = max(row_assigned.values(), default=0)
    svg_h = title_h + header_h + (max_row + 1) * row_h + padding * 2

    # node center positions
    def node_cx(n):
        lane = n.get("lane", 0)
        return 20 + lane * lane_w + lane_w // 2

    def node_cy(nid):
        return title_h + header_h + padding + row_assigned.get(nid, 0) * row_h + row_h // 2

    # --- SVG elements ---
    svgs = []

    # title bar
    svgs.append(f'<rect x="0" y="0" width="{total_w}" height="{title_h}" fill="{HEADER_COLOR}"/>')
    svgs.append(f'<text x="{total_w//2}" y="{title_h//2+6}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="24" font-weight="bold" fill="white">{_esc(title)}</text>')

    # lane headers
    for i, lane in enumerate(lanes):
        x = 20 + i * lane_w
        svgs.append(f'<rect x="{x}" y="{title_h}" width="{lane_w}" height="{header_h}" '
                    f'fill="{LANE_HEADER_FILL}" stroke="none"/>')
        svgs.append(f'<text x="{x + lane_w//2}" y="{title_h + header_h//2 + 5}" '
                    f'text-anchor="middle" font-family="{FONT}" font-size="18" '
                    f'font-weight="bold" fill="#222">{_esc(lane)}</text>')

    # nền thân lane (đồng nhất, trắng)
    for i in range(n_lanes):
        x = 20 + i * lane_w
        svgs.append(f'<rect x="{x}" y="{title_h + header_h}" width="{lane_w}" '
                    f'height="{svg_h - title_h - header_h}" fill="{LANE_BODY_FILL}" stroke="none"/>')

    # đường phân chia lane: kẻ dọc xám mờ từ dưới thanh tiêu đề xuống đáy + vạch ngang dưới header
    lane_x1 = 20 + n_lanes * lane_w
    svgs.append(f'<line x1="20" y1="{title_h + header_h}" x2="{lane_x1}" y2="{title_h + header_h}" '
                f'stroke="{LANE_DIVIDER}" stroke-width="1"/>')
    for i in range(n_lanes + 1):
        x = 20 + i * lane_w
        svgs.append(f'<line x1="{x}" y1="{title_h}" x2="{x}" y2="{svg_h}" '
                    f'stroke="{LANE_DIVIDER}" stroke-width="1"/>')

    # outer border
    svgs.append(f'<rect x="0" y="0" width="{total_w}" height="{svg_h}" '
                f'fill="none" stroke="#888" stroke-width="1.5"/>')

    # ---- helpers: connection points theo từng shape ----
    def conn_bottom(n, nid):
        """Điểm thoát ra ở đáy node."""
        cx, cy = node_cx(n), node_cy(nid)
        t = n.get("type", "process")
        if t in ("start", "end"):   return cx, cy + OVAL_RY
        if t == "decision":          return cx, cy + DEC_HH
        return cx, cy + PROC_H // 2

    def conn_top(n, nid):
        """Điểm vào ở đỉnh node."""
        cx, cy = node_cx(n), node_cy(nid)
        t = n.get("type", "process")
        if t in ("start", "end"):   return cx, cy - OVAL_RY
        if t == "decision":          return cx, cy - DEC_HH
        return cx, cy - PROC_H // 2

    def conn_right(n, nid):
        cx, cy = node_cx(n), node_cy(nid)
        t = n.get("type", "process")
        if t in ("start", "end"):   return cx + OVAL_RX, cy
        if t == "decision":          return cx + DEC_HW, cy
        return cx + PROC_W // 2, cy

    def conn_left(n, nid):
        cx, cy = node_cx(n), node_cy(nid)
        t = n.get("type", "process")
        if t in ("start", "end"):   return cx - OVAL_RX, cy
        if t == "decision":          return cx - DEC_HW, cy
        return cx - PROC_W // 2, cy

    # edges (draw before nodes so nodes are on top)
    for edge in edges:
        fid, tid = edge["from"], edge["to"]
        if fid not in node_map or tid not in node_map:
            continue
        fn, tn = node_map[fid], node_map[tid]
        lbl = _esc(edge.get("label", ""))

        r_from = row_assigned.get(fid, 0)
        r_to   = row_assigned.get(tid, 0)
        is_back = r_to < r_from

        cx_f, cy_f = node_cx(fn), node_cy(fid)
        cx_t, cy_t = node_cx(tn), node_cy(tid)
        same_lane = fn.get("lane") == tn.get("lane")
        # nét liền nếu trong cùng lane; nét đứt nếu mũi tên đi sang lane khác
        dash = "" if same_lane else ' stroke-dasharray="6,3"'

        # định tuyến theo mép trái: ra cạnh trái node nguồn → xuống lề trái → vào cạnh trái node đích
        if edge.get("route") == "left":
            sx, sy = conn_left(fn, fid)
            tex, tey = conn_left(tn, tid)
            ox = 30
            mk = '' if edge.get("no_arrow") else ' marker-end="url(#arrow)"'
            svgs.append(
                f'<polyline points="{sx},{sy} {ox},{sy} {ox},{tey} {tex},{tey}" '
                f'fill="none" stroke="{ARROW_COLOR}" stroke-width="1.5"{dash}{mk}/>'
            )
            if lbl:
                svgs.append(
                    f'<text x="{sx - 4}" y="{sy - 6}" text-anchor="end" '
                    f'font-family="{FONT}" font-size="14" fill="#555">{lbl}</text>'
                )
            continue

        if is_back:
            # vòng lặp: ra cạnh phải node nguồn → vòng bên phải → đi trong khoảng trống
            # PHÍA TRÊN node đích rồi VÀO ĐỈNH TRÊN (tránh chạy ngang tâm node, gây đè đường khác)
            sx, sy = conn_right(fn, fid)
            ttx, tty = conn_top(tn, tid)
            # node chữ nhật: vào lệch phải đỉnh trên để không trùng mũi tên vào sẵn có; hình thoi/oval: vào đúng đỉnh
            ent_x = (ttx + 35) if tn.get("type") not in ("decision", "start", "end") else ttx
            # đường vòng phải nằm ngoài mép phải hộp process của lane (hộp rộng → tránh đè)
            lane_box_right = max(node_cx(fn), node_cx(tn)) + PROC_W // 2
            ox = max(sx, ttx, ent_x, lane_box_right) + 30
            gap_y = tty - 24
            svgs.append(
                f'<polyline points="{sx},{sy} {ox},{sy} {ox},{gap_y} {ent_x},{gap_y} {ent_x},{tty}" '
                f'fill="none" stroke="{ARROW_COLOR}" stroke-width="1.5"{dash} '
                f'marker-end="url(#arrow)"/>'
            )
            if lbl:
                # đặt nhãn ngay tại điểm thoát của node nguồn (gần hình thoi), phía trên đoạn ngang
                svgs.append(
                    f'<text x="{sx + 6}" y="{sy - 6}" '
                    f'font-family="{FONT}" font-size="14" fill="#c00">{lbl}</text>'
                )

        elif same_lane:
            # cùng lane: bottom → top thẳng đứng
            bx, by = conn_bottom(fn, fid)
            tx, ty = conn_top(tn, tid)
            svgs.append(
                f'<line x1="{bx}" y1="{by}" x2="{tx}" y2="{ty}" '
                f'stroke="{ARROW_COLOR}" stroke-width="1.5" marker-end="url(#arrow)"/>'
            )
            if lbl:
                svgs.append(
                    f'<text x="{bx + 6}" y="{(by + ty) // 2}" '
                    f'font-family="{FONT}" font-size="14" fill="#555">{lbl}</text>'
                )

        else:
            # khác lane: luôn xuất phát từ góc ngang hình thoi (hoặc cạnh process)
            # sang phải nếu target lane > source lane, sang trái nếu ngược
            going_right = fn.get("lane", 0) < tn.get("lane", 0)

            if going_right:
                sx, sy = conn_right(fn, fid)
                ex, ey = conn_top(tn, tid) if r_to > r_from else conn_left(tn, tid)
            else:
                sx, sy = conn_left(fn, fid)
                ex, ey = conn_top(tn, tid) if r_to > r_from else conn_right(tn, tid)

            if r_from == r_to:
                # cùng row → đường thẳng ngang
                mk = '' if edge.get("no_arrow") else ' marker-end="url(#arrow)"'
                svgs.append(
                    f'<line x1="{sx}" y1="{sy}" x2="{ex}" y2="{ey}" '
                    f'stroke="{ARROW_COLOR}" stroke-width="1.5"{dash}{mk}/>'
                )
                if lbl:
                    mx = (sx + ex) // 2
                    my = (sy + ey) // 2
                    svgs.append(
                        f'<text x="{mx}" y="{my - 5}" text-anchor="middle" '
                        f'font-family="{FONT}" font-size="14" fill="#555">{lbl}</text>'
                    )
            else:
                # khác row → từ góc ngang → đi ngang tới cùng x đích → đi dọc xuống → vào top đích
                svgs.append(
                    f'<polyline points="{sx},{sy} {ex},{sy} {ex},{ey}" '
                    f'fill="none" stroke="{ARROW_COLOR}" stroke-width="1.5"{dash} marker-end="url(#arrow)"/>'
                )
                if lbl:
                    mx = (sx + ex) // 2
                    svgs.append(
                        f'<text x="{mx}" y="{sy - 5}" text-anchor="middle" '
                        f'font-family="{FONT}" font-size="14" fill="#555">{lbl}</text>'
                    )

    # nodes (vẽ sau edge để nằm trên)
    for n in nodes:
        nid = n["id"]
        cx, cy = node_cx(n), node_cy(nid)
        label = n.get("label", nid)
        note  = n.get("note", "")
        ntype = n.get("type", "process")

        if ntype in ("start", "end"):
            fill = HEADER_COLOR if ntype == "start" else "#444"
            svgs.append(
                f'<ellipse cx="{cx}" cy="{cy}" rx="{OVAL_RX}" ry="{OVAL_RY}" '
                f'fill="{fill}" stroke="{SHAPE_STROKE}" stroke-width="1.5"/>'
            )
            svgs.append(_svg_text(cx, cy, label, color="white", size=NODE_FONT, bold=True, max_chars=oval_mc))

        elif ntype == "decision":
            pts = f"{cx},{cy-DEC_HH} {cx+DEC_HW},{cy} {cx},{cy+DEC_HH} {cx-DEC_HW},{cy}"
            svgs.append(
                f'<polygon points="{pts}" fill="{DECISION_FILL}" '
                f'stroke="{SHAPE_STROKE}" stroke-width="1.5"/>'
            )
            svgs.append(_svg_text(cx, cy, label, size=NODE_FONT, max_chars=dec_mc))

        else:  # process
            svgs.append(
                f'<rect x="{cx - PROC_W//2}" y="{cy - PROC_H//2}" '
                f'width="{PROC_W}" height="{PROC_H}" rx="6" ry="6" '
                f'fill="{SHAPE_FILL}" stroke="{SHAPE_STROKE}" stroke-width="1.5"/>'
            )
            svgs.append(_svg_text(cx, cy, label, size=NODE_FONT, max_chars=proc_mc))

        if note:
            note_x = cx - PROC_W // 2 - 8
            for li, line in enumerate(note.split("\n")):
                ny = cy - 6 + li * 13
                svgs.append(
                    f'<text x="{note_x}" y="{ny}" text-anchor="end" '
                    f'font-family="{FONT}" font-size="9" fill="{NOTE_COLOR}">{_esc(line)}</text>'
                )

    # arrowhead marker
    defs = (
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
        f'<path d="M0,0 L0,6 L8,3 z" fill="{ARROW_COLOR}"/>'
        '</marker></defs>'
    )

    svg_body = "\n".join(svgs)
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>body{{margin:0;padding:0;background:#fff;}}</style>
</head><body>
<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{svg_h}"
     style="font-family:{FONT}">
{defs}
{svg_body}
</svg>
</body></html>"""
    return html


def _esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _wrap_line(s, max_chars):
    """Ngắt dòng theo từ để không vượt max_chars (giữ nguyên dấu xuống dòng có sẵn)."""
    words = s.split(" ")
    lines, cur = [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > max_chars:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines or [""]


def _svg_text(cx, cy, label, color="#222", size=13, bold=False, max_chars=None):
    segs = str(label).split("\n")
    if max_chars:
        lines = []
        for seg in segs:
            lines.extend(_wrap_line(seg, max_chars))
    else:
        lines = segs
    fw = "bold" if bold else "normal"
    out = []
    start_y = cy - (len(lines)-1) * (size+2) // 2
    for i, line in enumerate(lines):
        y = start_y + i * (size + 3)
        out.append(f'<text x="{cx}" y="{y+4}" text-anchor="middle" dominant-baseline="middle" '
                   f'font-family="{FONT}" font-size="{size}" font-weight="{fw}" fill="{_esc(color)}">'
                   f'{_esc(line)}</text>')
    return "\n".join(out)


# ---------- CAPTURE ----------
def capture_html_to_png(html_path: str, png_path: str):
    """Dùng playwright headless chromium để chụp HTML → PNG."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[LỖI] Thiếu playwright. Cài: pip install playwright && python -m playwright install chromium")
        return False

    abs_html = os.path.abspath(html_path)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file:///{abs_html.replace(chr(92), '/')}")
        page.wait_for_load_state("networkidle")
        # lấy kích thước SVG thực
        size = page.evaluate("""() => {
            const svg = document.querySelector('svg');
            return {w: svg.getAttribute('width'), h: svg.getAttribute('height')};
        }""")
        page.set_viewport_size({"width": int(size["w"]) + 4, "height": int(size["h"]) + 4})
        page.screenshot(path=png_path, full_page=True)
        browser.close()
    print(f"[OK] Đã tạo PNG: {png_path}")
    return True


# ---------- CACHE CHECK ----------
def is_png_fresh(html_path: str, png_path: str) -> bool:
    """True nếu PNG đã tồn tại và mới hơn HTML (không cần render lại)."""
    if not os.path.exists(png_path):
        return False
    if not os.path.exists(html_path):
        return False
    return os.path.getmtime(png_path) >= os.path.getmtime(html_path)


# ---------- MAIN PIPELINE ----------
def generate(json_path: str, out_dir: str = None) -> str:
    """Sinh HTML + PNG từ JSON. Trả về đường dẫn PNG."""
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    base = os.path.splitext(os.path.basename(json_path))[0]
    if out_dir is None:
        out_dir = os.path.dirname(json_path)
    os.makedirs(out_dir, exist_ok=True)

    html_path = os.path.join(out_dir, base + ".html")
    png_path = os.path.join(out_dir, base + ".png")

    # sinh HTML
    html_content = build_html(data)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[OK] Đã tạo HTML: {html_path}")

    # capture PNG (check cache)
    if is_png_fresh(html_path, png_path):
        print(f"[CACHE] PNG đã mới, dùng lại: {png_path}")
    else:
        capture_html_to_png(html_path, png_path)

    return png_path


def capture_only(html_path: str, png_path: str = None) -> str:
    if png_path is None:
        png_path = os.path.splitext(html_path)[0] + ".png"
    if is_png_fresh(html_path, png_path):
        print(f"[CACHE] PNG đã mới, dùng lại: {png_path}")
        return png_path
    capture_html_to_png(html_path, png_path)
    return png_path


# ---------- CLI ----------
if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Dùng:")
        print("  python swimlane_generator.py <input.json> [-o out_dir]")
        print("  python swimlane_generator.py --capture-only <input.html> [-o out.png]")
        sys.exit(1)

    if args[0] == "--capture-only":
        html_p = args[1]
        out_p = args[args.index("-o")+1] if "-o" in args else None
        capture_only(html_p, out_p)
    else:
        json_p = args[0]
        out_d = args[args.index("-o")+1] if "-o" in args else None
        generate(json_p, out_d)
