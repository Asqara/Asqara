#!/usr/bin/env python3
"""
ASQARA.TECH — README asset generator.

Generates every animated SVG used in README.md and DESIGN_SYSTEM.md,
in both dark and light variants, from a single set of design tokens.

    python3 scripts/build_assets.py

Edit TOKENS / content below and re-run to regenerate ./assets.
No dependencies beyond the Python standard library.
"""
import json
import os
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")
ICONS = json.load(open(os.path.join(ROOT, "scripts", "icons.json")))

# ─────────────────────────────────────────────────────────────
# Design tokens (mirrors asqara.tech)
# ─────────────────────────────────────────────────────────────
TOKENS = {
    "dark": {
        "bg": "#0c0d0f", "surface": "#121317", "border": "#292b30",
        "text": "#f2f1ec", "muted": "#a8a8a2", "violet": "#9875ff",
        "lime": "#d7ff3f", "acc": "#d7ff3f", "onLime": "#101010",
        "grid": "#1b1d22",
    },
    "light": {
        "bg": "#f4f3ef", "surface": "#faf9f6", "border": "#d4d2cc",
        "text": "#101010", "muted": "#595959", "violet": "#8155ff",
        "lime": "#d7ff3f", "acc": "#5f7f00", "onLime": "#101010",
        "grid": "#e6e4de",
    },
}
SANS = "Geist, -apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Roboto, 'Helvetica Neue', Arial, sans-serif"
MONO = "'Geist Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace"
EASE = "cubic-bezier(.16,1,.3,1)"


def e(s):
    return escape(str(s))


def svg(w, h, body, T, css="", title="ASQARA.TECH"):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{e(title)}">
<title>{e(title)}</title>
<style>
.m{{font-family:{MONO}}}.s{{font-family:{SANS}}}
.t{{fill:{T['text']}}}.mu{{fill:{T['muted']}}}.v{{fill:{T['violet']}}}.a{{fill:{T['acc']}}}.ol{{fill:{T['onLime']}}}
.fb{{transform-box:fill-box;transform-origin:center}}
.r{{animation:rise .9s {EASE} both}}
.f{{animation:fade 1.2s ease both}}
.blink{{animation:blink 1.05s steps(1) infinite}}
.pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2.2s ease-out infinite}}
.spin{{transform-box:fill-box;transform-origin:center;animation:spin 14s linear infinite}}
.flow{{stroke-dasharray:3 7;animation:flow .9s linear infinite}}
.draw{{stroke-dasharray:1;animation:draw 1.6s {EASE} both}}
.grow{{transform-box:fill-box;transform-origin:left center;animation:grow 1.6s {EASE} both}}
@keyframes rise{{from{{opacity:0;transform:translateY(16px)}}to{{opacity:1;transform:none}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes pulse{{0%{{transform:scale(1);opacity:.9}}100%{{transform:scale(3.2);opacity:0}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes flow{{to{{stroke-dashoffset:-20}}}}
@keyframes draw{{from{{stroke-dashoffset:1}}to{{stroke-dashoffset:0}}}}
@keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
{css}
</style>
<rect width="{w}" height="{h}" fill="{T['bg']}"/>
{body}
</svg>
"""


def d(sec):
    return f'style="animation-delay:{sec:.2f}s"'


def brackets(x, y, w, h, color, s=10, sw=1.5):
    p = (f"M{x},{y+s}V{y}H{x+s} M{x+w-s},{y}H{x+w}V{y+s} "
         f"M{x+w},{y+h-s}V{y+h}H{x+w-s} M{x+s},{y+h}H{x}V{y+h-s}")
    return f'<path d="{p}" fill="none" stroke="{color}" stroke-width="{sw}"/>'


def grid(w, h, T, step=40, id_="g"):
    return (f'<defs><pattern id="{id_}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
            f'<path d="M{step} 0H0V{step}" fill="none" stroke="{T["grid"]}" stroke-width="1"/></pattern></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#{id_})"/>')


def wrap(text, n):
    lines, cur = [], ""
    for word in text.split():
        if len(cur) + len(word) + (1 if cur else 0) > n:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}" if cur else word
    if cur:
        lines.append(cur)
    return lines


def tw(text, size, mono=True):
    return len(text) * size * (0.61 if mono else 0.56)


def chip(x, y, label, T, fill=None, color=None, size=11):
    w = tw(label, size) + 18
    fill = fill or "none"
    color = color or T["text"]
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="24" fill="{fill}" stroke="{T["border"]}"/>'
            f'<text x="{x+9}" y="{y+16}" class="m" font-size="{size}" fill="{color}" letter-spacing=".5">{e(label)}</text>'), w


def icon(name, x, y, size, color):
    s = size / 24
    return f'<path transform="translate({x},{y}) scale({s:.3f})" d="{ICONS[name]}" fill="{color}"/>'


def star(cx, cy, r, color, cls="spin", delay=0):
    """The ✣ glyph from the site, drawn as geometry so it renders everywhere."""
    arms = "".join(
        f'<rect x="{cx - r*0.18:.1f}" y="{cy - r:.1f}" width="{r*0.36:.1f}" height="{r*2:.1f}" rx="{r*0.18:.1f}" '
        f'transform="rotate({a} {cx} {cy})"/>' for a in (0, 45, 90, 135))
    return f'<g class="{cls}" fill="{color}" {d(delay)}>{arms}</g>'


# ─────────────────────────────────────────────────────────────
# 1. HERO
# ─────────────────────────────────────────────────────────────
def hero(T):
    W, H = 1000, 440
    css = f"""
.scan{{animation:scan 6s linear infinite}}
@keyframes scan{{from{{transform:translateY(-40px)}}to{{transform:translateY({H}px)}}}}
.glow{{animation:glow 5s ease-in-out infinite}}
@keyframes glow{{50%{{opacity:.35}}}}
.orb1{{transform-box:view-box;transform-origin:830px 215px;animation:spin 18s linear infinite}}
.orb2{{transform-box:view-box;transform-origin:830px 215px;animation:spin 11s linear infinite reverse}}
.orb3{{transform-box:view-box;transform-origin:830px 215px;animation:spin 7s linear infinite}}
.cube{{transform-box:view-box;transform-origin:830px 215px;animation:wob 9s ease-in-out infinite}}
@keyframes wob{{50%{{transform:rotate(18deg) scale(1.06)}}}}
"""
    nav = "WORK / EXPERIENCE / SYSTEM / ABOUT / CONTACT"
    b = [grid(W, H, T)]
    b.append(f'<defs><radialGradient id="rg" cx="830" cy="215" r="260" gradientUnits="userSpaceOnUse">'
             f'<stop offset="0" stop-color="{T["violet"]}" stop-opacity=".30"/>'
             f'<stop offset="1" stop-color="{T["violet"]}" stop-opacity="0"/></radialGradient>'
             f'<linearGradient id="sl" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{T["acc"]}" stop-opacity="0"/>'
             f'<stop offset="1" stop-color="{T["acc"]}" stop-opacity=".18"/></linearGradient></defs>')
    b.append(f'<rect class="glow" width="{W}" height="{H}" fill="url(#rg)"/>')
    # top bar
    b.append(f'<g class="f"><text x="32" y="31" class="s t" font-size="16" font-weight="800" letter-spacing="1">ASQARA<tspan class="v">.TECH</tspan></text>'
             f'<text x="500" y="30" text-anchor="middle" class="m mu" font-size="11" letter-spacing="1.5">{nav}</text>'
             f'<circle cx="790" cy="26" r="4" class="a"/><circle cx="790" cy="26" r="4" class="a pulse"/>'
             f'<text x="802" y="30" class="m t" font-size="11" letter-spacing="1.5">OPERATIONAL</text>'
             f'<text x="968" y="30" text-anchor="end" class="m mu" font-size="11">UTC+7</text></g>')
    b.append(f'<line x1="0" y1="52" x2="{W}" y2="52" stroke="{T["border"]}"/>')
    # orbit object
    cx, cy = 830, 215
    b.append(f'<g class="orb1" fill="none" stroke="{T["violet"]}" stroke-width="1.2" opacity=".9">'
             f'<ellipse cx="{cx}" cy="{cy}" rx="120" ry="42"/><circle cx="{cx+120}" cy="{cy}" r="4" fill="{T["violet"]}"/></g>')
    b.append(f'<g class="orb2" fill="none" stroke="{T["border"]}" stroke-width="1.2">'
             f'<ellipse cx="{cx}" cy="{cy}" rx="42" ry="120"/><circle cx="{cx}" cy="{cy-120}" r="3.5" fill="{T["acc"]}" stroke="none"/></g>')
    b.append(f'<g class="orb3" fill="none" stroke="{T["muted"]}" stroke-width=".8" stroke-dasharray="2 6">'
             f'<circle cx="{cx}" cy="{cy}" r="150"/></g>')
    cube = (f"M{cx},{cy-46} L{cx+40},{cy-23} L{cx+40},{cy+23} L{cx},{cy+46} L{cx-40},{cy+23} L{cx-40},{cy-23} Z "
            f"M{cx},{cy-46} L{cx},{cy} M{cx},{cy} L{cx+40},{cy+23} M{cx},{cy} L{cx-40},{cy+23}")
    b.append(f'<g class="cube"><path d="{cube}" fill="{T["surface"]}" fill-opacity=".6" stroke="{T["text"]}" stroke-width="1.4"/>'
             f'{star(cx, cy + 2, 11, T["acc"])}</g>')
    b.append(f'<text x="{cx}" y="{cy+160}" text-anchor="middle" class="m mu f" font-size="10" letter-spacing="3" {d(1.4)}>FULL-STACK DEVELOPER</text>')
    # headline
    b.append(f'<text x="32" y="104" class="m v r" font-size="13" letter-spacing="1.5" {d(.2)}>/ 01  <tspan class="mu">SYSTEMS / SOFTWARE / INFRASTRUCTURE</tspan></text>')
    b.append(f'<g class="r" {d(.35)}><text x="28" y="190" class="s t" font-size="78" font-weight="800" letter-spacing="-3" textLength="575" lengthAdjust="spacingAndGlyphs">SYSTEMS BUILT</text></g>')
    b.append(f'<g class="r" {d(.55)}><text x="28" y="272" class="s t" font-size="78" font-weight="800" letter-spacing="-3" textLength="560" lengthAdjust="spacingAndGlyphs">FOR REAL USE<tspan class="a">.</tspan></text></g>')
    b.append(f'<rect x="602" y="214" width="22" height="58" class="a blink"/>')
    b.append(f'<text x="32" y="318" class="s mu r" font-size="17" {d(.8)}>Alfath Asqar Tsani — software engineer building full-stack apps,</text>')
    b.append(f'<text x="32" y="342" class="s mu r" font-size="17" {d(.9)}>data infrastructure &amp; production systems at university scale.</text>')
    # bottom bar
    b.append(f'<line x1="0" y1="384" x2="{W}" y2="384" stroke="{T["border"]}"/>')
    b.append(f'<g class="f" {d(1.1)}><text x="32" y="415" class="m t" font-size="11" letter-spacing="2">FULL-STACK · DATA · PRODUCTION</text>'
             f'<text x="500" y="415" text-anchor="middle" class="m mu" font-size="11" letter-spacing="1.5">SCN_01 / 2026 SOFTWARE ENGINEERING / BOGOR</text>'
             f'<text x="968" y="415" text-anchor="end" class="m mu" font-size="11">06.5971° S  106.8060° E</text></g>')
    b.append(f'<rect class="scan" x="0" y="0" width="{W}" height="40" fill="url(#sl)"/>')
    b.append(brackets(8, 60, W - 16, 316, T["muted"], 14, 1))
    return svg(W, H, "\n".join(b), T, css, "Alfath Asqar Tsani — Systems built for real use")


# ─────────────────────────────────────────────────────────────
# 2. MARQUEE
# ─────────────────────────────────────────────────────────────
def marquee(T):
    W, H, SEG = 1000, 76, 560
    css = f"""
.mq1{{animation:mq1 16s linear infinite}}@keyframes mq1{{to{{transform:translateX(-{SEG}px)}}}}
.mq2{{animation:mq2 20s linear infinite}}@keyframes mq2{{from{{transform:translateX(-{SEG}px)}}to{{transform:none}}}}
"""
    t1 = "FULL-STACK / PLATFORM / DATA / PRODUCTION ✣ "
    t2 = "DESIGN THE INTERFACE / OPERATE THE SYSTEM ✣ "
    row1 = "".join(f'<text x="{i*SEG}" y="30" class="m t" font-size="14" font-weight="600" letter-spacing="2" textLength="{SEG-34}" lengthAdjust="spacing">{e(t1.strip())}</text>' for i in range(4))
    row2 = "".join(f'<text x="{i*SEG}" y="63" class="m ol" font-size="14" font-weight="600" letter-spacing="2" textLength="{SEG-34}" lengthAdjust="spacing">{e(t2.strip())}</text>' for i in range(4))
    b = [f'<rect y="0" width="{W}" height="40" fill="{T["surface"]}"/>',
         f'<rect y="40" width="{W}" height="36" fill="{T["lime"]}"/>',
         f'<line x1="0" y1="0.5" x2="{W}" y2="0.5" stroke="{T["border"]}"/>',
         f'<line x1="0" y1="40" x2="{W}" y2="40" stroke="{T["border"]}"/>',
         f'<g class="mq1">{row1}</g>', f'<g class="mq2">{row2}</g>']
    return svg(W, H, "\n".join(b), T, css, "Full-stack / Platform / Data / Production")


# ─────────────────────────────────────────────────────────────
# 3. SECTION HEADERS
# ─────────────────────────────────────────────────────────────
SECTIONS = [
    ("about", "02", "ABOUT / PROFILE", "Engineering beyond the UI."),
    ("principles", "03", "ENGINEERING PRINCIPLES", "How I build."),
    ("work", "04", "SELECTED WORK", "Selected systems."),
    ("platform", "05", "PLATFORM ENGINEERING", "Beyond the interface."),
    ("data", "06", "DATA INFRASTRUCTURE", "One source. Many systems."),
    ("stack", "07", "TECHNOLOGY MATRIX", "Tools with a purpose."),
    ("other", "08", "OTHER ENGINEERING WORK", "Automation & research."),
    ("archive", "09", "PROJECT ARCHIVE / PUBLIC BUILDS", "More builds."),
    ("experience", "10", "EXPERIENCE", "Operating in context."),
    ("education", "11", "EDUCATION / CERTIFICATION", "Foundations."),
    ("telemetry", "12", "GITHUB TELEMETRY", "Activity stream."),
    ("status", "13", "SYSTEM STATUS", "Profile operational."),
    ("contact", "14", "CONTACT / OPEN CHANNEL", "Let's build something useful."),
]


def section(T, idx, label, title):
    W, H = 1000, 112
    css = """
.run{animation:run 4.5s cubic-bezier(.65,0,.35,1) infinite}
@keyframes run{0%{transform:translateX(0)}50%{transform:translateX(976px)}100%{transform:translateX(0)}}
"""
    b = [f'<line x1="0" y1="10" x2="{W}" y2="10" stroke="{T["border"]}"/>',
         f'<line x1="0" y1="10" x2="{W}" y2="10" stroke="{T["violet"]}" stroke-width="2" pathLength="1" class="draw"/>',
         f'<rect class="run" x="0" y="7" width="24" height="6" fill="{T["lime"]}"/>',
         f'<text x="24" y="44" class="m v r" font-size="13" letter-spacing="1.5">/ {idx}  <tspan class="mu">{e(label)}</tspan></text>',
         f'<g class="r" {d(.15)}><text x="22" y="94" class="s t" font-size="40" font-weight="800" letter-spacing="-1.4">{e(title.upper())}</text></g>',
         f'<text x="{W-52}" y="44" text-anchor="end" class="m mu f" font-size="11" letter-spacing="1.5" {d(.3)}>SCN_{idx}</text>',
         star(W - 34, 40, 9, T["acc"]),
         ]
    return svg(W, H, "\n".join(b), T, css, f"/ {idx} {label} — {title}")


# ─────────────────────────────────────────────────────────────
# 4. METRICS
# ─────────────────────────────────────────────────────────────
METRICS = [
    ("~8,000", "", "STUDENT RECORDS", "normalized across services", .92),
    ("~1,000", "RPS", "PEAK PRODUCTION LOAD", "on Kubernetes / k3s", .78),
    ("Rp600M+", "", "TRANSACTION VALUE", "handled in production", .86),
    ("~60%", "", "FASTER PAGE LOAD", "Next.js optimization", .60),
]


def metrics(T):
    W, H = 1000, 196
    cw = W / 4
    b = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" fill="{T["surface"]}" stroke="{T["border"]}"/>']
    spark = "M0,26 L18,22 L36,24 L54,14 L72,18 L90,8 L108,12 L126,2"
    for i, (val, unit, label, sub, pct) in enumerate(METRICS):
        x = i * cw
        dl = .15 * i
        if i:
            b.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{T["border"]}"/>')
        b.append(f'<g class="r" {d(dl)}>'
                 f'<text x="{x+24}" y="34" class="m mu" font-size="11" letter-spacing="2">0 {i+1}</text>'
                 f'<text x="{x+24}" y="92" class="s t" font-size="44" font-weight="800" letter-spacing="-1.5">{e(val)}'
                 + (f'<tspan class="v" font-size="18" letter-spacing="0" dx="6">{unit}</tspan>' if unit else "") +
                 f'</text>'
                 f'<text x="{x+24}" y="120" class="m t" font-size="11" letter-spacing="1.5">{e(label)}</text>'
                 f'<text x="{x+24}" y="138" class="s mu" font-size="13">{e(sub)}</text></g>')
        b.append(f'<path transform="translate({x+cw-150},22)" d="{spark}" fill="none" stroke="{T["violet"]}" stroke-width="1.6" pathLength="1" class="draw" {d(.4+dl)}/>')
        b.append(f'<circle cx="{x+cw-24}" cy="24" r="3" class="a"/><circle cx="{x+cw-24}" cy="24" r="3" class="a pulse" {d(dl)}/>')
        b.append(f'<rect x="{x+24}" y="160" width="{cw-48}" height="6" fill="{T["border"]}"/>')
        b.append(f'<rect x="{x+24}" y="160" width="{(cw-48)*pct:.0f}" height="6" fill="{T["lime"] if i % 2 else T["violet"]}" class="grow" {d(.5+dl)}/>')
    return svg(W, H, "\n".join(b), T, "", "Key metrics")


# ─────────────────────────────────────────────────────────────
# 5. PRINCIPLES
# ─────────────────────────────────────────────────────────────
PRINCIPLES = [
    ("SYSTEMS THINKING", "Architecture before complexity."),
    ("REAL USERS", "Built from real operational problems."),
    ("DATA FIRST", "Reliable systems need structured data."),
    ("PRODUCTION MATTERS", "Software isn't done until it survives production."),
    ("FUNCTION OVER NOISE", "Interfaces should communicate before they decorate."),
]


def principles(T):
    W, H, cw = 1000, 220, 200
    css = """
.hop{animation:hop 7.5s steps(1) infinite}
@keyframes hop{0%{transform:translateX(0)}20%{transform:translateX(200px)}40%{transform:translateX(400px)}60%{transform:translateX(600px)}80%{transform:translateX(800px)}}
.hl{animation:hl 7.5s steps(1) infinite;opacity:0}
@keyframes hl{0%,20%{opacity:1}20.01%,100%{opacity:0}}
"""
    b = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" fill="none" stroke="{T["border"]}"/>']
    b.append(f'<g class="hop"><rect x="0" y="0" width="{cw}" height="{H}" fill="{T["violet"]}" fill-opacity=".08"/>'
             f'<rect x="0" y="0" width="{cw}" height="4" fill="{T["lime"]}"/></g>')
    for i, (t, desc) in enumerate(PRINCIPLES):
        x = i * cw
        if i:
            b.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{T["border"]}"/>')
        lines = wrap(desc, 19)
        txt = "".join(f'<tspan x="{x+20}" dy="{0 if j == 0 else 22}">{e(l)}</tspan>' for j, l in enumerate(lines))
        b.append(f'<g class="r" {d(.12*i)}>'
                 f'<text x="{x+20}" y="40" class="m v" font-size="12" letter-spacing="2">0 {i+1}</text>'
                 f'<text x="{x+20}" y="78" class="m t" font-size="12" font-weight="700" letter-spacing="1.2">{e(t)}</text>'
                 f'<text x="{x+20}" y="114" class="s mu" font-size="16">{txt}</text></g>')
        b.append(star(x + cw - 26, 36, 7, T["acc"], "spin", i * .5))
    return svg(W, H, "\n".join(b), T, css, "Engineering principles")


# ─────────────────────────────────────────────────────────────
# 6. PROJECT CARDS
# ─────────────────────────────────────────────────────────────
PROJECTS = [
    ("mysoc", "MySOC", "PLATFORM ENGINEERING", "2026",
     "Integrated operational platform connecting committee workflows, participant management, administration and institutional stakeholders.",
     ["Next.js", "TypeScript", "Bun", "PostgreSQL", "k8s"], "~1,000 RPS", ["nextdotjs", "bun", "postgresql", "redis", "kubernetes"]),
    ("helpdesk", "MySOC Helpdesk", "SUPPORT EXPERIENCE", "2026",
     "Focused help center that gives participants one trusted place to find guidance and support.",
     ["Web Support", "Knowledge Base", "Support UX"], "SUPPORT", ["nextdotjs", "typescript", "react"]),
    ("ormawa", "Ormawa Eksekutif PKU", "ORGANIZATION PLATFORM", "2024—2025",
     "Public information and publication platform for one of the largest student organizations at PKU IPB.",
     ["Laravel", "Inertia.js", "Tailwind CSS"], "PUBLIC", []),
    ("studentorientation", "StudentOrientation", "DATA INFRASTRUCTURE", "2025",
     "Central student platform for orientation, participant management, information delivery and digital student services.",
     ["Next.js", "TypeScript", "PostgreSQL"], "~8,000 STUDENTS", ["nextdotjs", "typescript", "postgresql"]),
    ("store", "Agrisymphony Store", "COMMERCE PLATFORM", "2025",
     "Digital merchandise platform supporting products, orders, transactions and merchandise operations.",
     ["Next.js", "TypeScript", "PostgreSQL"], "Rp600M+", ["nextdotjs", "typescript", "postgresql"]),
    ("agrisymphony", "Agrisymphony", "PUBLIC WEBSITE & TICKETING", "2025",
     "Public event website and digital services supporting event information and official ticket sales.",
     ["Next.js", "TypeScript", "Tailwind CSS"], "1,000+ TICKETS", ["nextdotjs", "typescript", "react"]),
]


def card(T, i, p):
    slug, name, cat, year, desc, tech, kpi, icons = p
    W, H = 480, 300
    css = f"""
.sweep{{animation:sweep 5s ease-in-out infinite}}
@keyframes sweep{{0%{{transform:translateX(-120px)}}60%,100%{{transform:translateX({W+40}px)}}}}
.arrow{{animation:arrow 1.8s {EASE} infinite}}
@keyframes arrow{{0%,40%{{transform:none}}70%{{transform:translate(5px,-5px)}}100%{{transform:none}}}}
"""
    b = [f'<defs><linearGradient id="sw{i}" x1="0" x2="1"><stop offset="0" stop-color="{T["violet"]}" stop-opacity="0"/>'
         f'<stop offset=".5" stop-color="{T["violet"]}" stop-opacity=".14"/><stop offset="1" stop-color="{T["violet"]}" stop-opacity="0"/></linearGradient>'
         f'<clipPath id="cp{i}"><rect width="{W}" height="{H}"/></clipPath></defs>',
         f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" fill="{T["surface"]}" stroke="{T["border"]}"/>',
         f'<g clip-path="url(#cp{i})"><rect class="sweep" x="0" y="0" width="120" height="{H}" fill="url(#sw{i})"/></g>',
         f'<g class="r"><text x="24" y="40" class="m v" font-size="13" letter-spacing="2">0 {i+1}</text>'
         f'<text x="{W-24}" y="40" text-anchor="end" class="m mu" font-size="11" letter-spacing="1.2">{e(cat)} · {e(year)}</text></g>',
         f'<line x1="24" y1="56" x2="{W-24}" y2="56" stroke="{T["border"]}"/>',
         f'<g class="r" {d(.1)}><text x="22" y="104" class="s t" font-size="{30 if len(name) < 18 else 26}" font-weight="800" letter-spacing="-.8">{e(name)}</text></g>',
         f'<g class="arrow"><text x="{W-24}" y="104" text-anchor="end" class="s a" font-size="26" font-weight="700">↗</text></g>']
    lines = wrap(desc, 52)[:3]
    txt = "".join(f'<tspan x="24" dy="{0 if j == 0 else 21}">{e(l)}</tspan>' for j, l in enumerate(lines))
    b.append(f'<g class="r" {d(.2)}><text x="24" y="138" class="s mu" font-size="14.5">{txt}</text></g>')
    x = 24
    chips = []
    for t in tech:
        c, w = chip(x, 222, t, T)
        chips.append(c)
        x += w + 6
    b.append(f'<g class="r" {d(.3)}>{"".join(chips)}</g>')
    b.append(f'<line x1="24" y1="262" x2="{W-24}" y2="262" stroke="{T["border"]}" stroke-dasharray="2 4"/>')
    b.append(f'<circle cx="30" cy="280" r="3.5" class="a"/><circle cx="30" cy="280" r="3.5" class="a pulse"/>'
             f'<text x="42" y="284" class="m t" font-size="11" letter-spacing="1.5">{e(kpi)}</text>')
    ix = W - 24
    for n in reversed(icons):
        ix -= 18
        b.append(icon(n, ix, 271, 16, T["muted"]))
        ix -= 8
    b.append(brackets(6, 6, W - 12, H - 12, T["muted"], 8, 1))
    return svg(W, H, "\n".join(b), T, css, f"{name} — {cat}")


# ─────────────────────────────────────────────────────────────
# 7. PLATFORM ENGINEERING STACK
# ─────────────────────────────────────────────────────────────
LAYERS = [
    ("CLIENTS", "Web · Mobile · Operators", None),
    ("WEB APPLICATION", "Next.js · React · Interface", "nextdotjs"),
    ("APPLICATION SERVICES", "Business logic · RBAC · Integration", "bun"),
    ("POSTGRESQL + REDIS", "Persistent data · Cache · Sessions", "postgresql"),
    ("DOCKER", "Containerized services", "docker"),
    ("KUBERNETES / k3s", "Orchestration · Routing · Recovery", "kubernetes"),
]


def platform(T):
    W, H = 1000, 540
    top, bh, gap = 34, 62, 18
    span = (len(LAYERS) - 1) * (bh + gap)
    css = f"""
.pk{{animation:pk 3.6s cubic-bezier(.65,0,.35,1) infinite}}
@keyframes pk{{0%{{transform:translateY(0);opacity:0}}8%{{opacity:1}}92%{{opacity:1}}100%{{transform:translateY({span}px);opacity:0}}}}
.pku{{animation:pku 4.2s cubic-bezier(.65,0,.35,1) infinite}}
@keyframes pku{{0%{{transform:translateY({span}px);opacity:0}}8%{{opacity:1}}92%{{opacity:1}}100%{{transform:translateY(0);opacity:0}}}}
.lit{{animation:lit 3.6s ease infinite;opacity:0}}
@keyframes lit{{0%,100%{{opacity:0}}6%{{opacity:1}}24%{{opacity:0}}}}
"""
    b = [grid(W, H, T, 40, "gp")]
    # left column
    b.append(f'<g class="r"><text x="24" y="112" class="s t" font-size="96" font-weight="800" letter-spacing="-4">~1,000</text></g>')
    b.append(f'<g class="r" {d(.15)}><text x="28" y="146" class="m v" font-size="14" letter-spacing="2">RPS <tspan class="mu">/ PEAK PRODUCTION LOAD</tspan></text></g>')
    para = wrap("Products don't stop at the browser. I work across service boundaries, data storage, containers, orchestration, deployment and the operational decisions that keep software useful.", 44)
    txt = "".join(f'<tspan x="28" dy="{0 if j == 0 else 24}">{e(l)}</tspan>' for j, l in enumerate(para))
    b.append(f'<g class="r" {d(.3)}><text x="28" y="196" class="s mu" font-size="16">{txt}</text></g>')
    b.append(f'<text x="28" y="{196 + 24*len(para) + 22}" class="m t" font-size="11" letter-spacing="2">PRODUCTION SYSTEM</text>')
    tags = ["CONTAINERIZED", "ORCHESTRATED", "SCALABLE", "RECOVERABLE"]
    ty = 196 + 24 * len(para) + 40
    for k, t in enumerate(tags):
        x = 28 + (k % 2) * 190
        y = ty + (k // 2) * 40
        b.append(f'<g class="r" {d(.45+.1*k)}><rect x="{x}" y="{y}" width="176" height="30" fill="{T["surface"]}" stroke="{T["border"]}"/>'
                 f'<circle cx="{x+16}" cy="{y+15}" r="3.5" class="a"/><circle cx="{x+16}" cy="{y+15}" r="3.5" class="a pulse" {d(k*.4)}/>'
                 f'<text x="{x+30}" y="{y+19}" class="m t" font-size="11" letter-spacing="1.5">{t}</text></g>')
    # rail
    rx = 486
    b.append(f'<line x1="{rx}" y1="{top+bh/2}" x2="{rx}" y2="{top+bh/2+span}" stroke="{T["border"]}" stroke-width="2"/>')
    b.append(f'<line x1="{rx}" y1="{top+bh/2}" x2="{rx}" y2="{top+bh/2+span}" stroke="{T["violet"]}" stroke-width="2" class="flow"/>')
    for k in range(3):
        b.append(f'<rect class="pk" x="{rx-5}" y="{top+bh/2-5}" width="10" height="10" fill="{T["lime"]}" style="animation-delay:{k*1.2:.1f}s"/>')
    b.append(f'<rect class="pku" x="{rx-3}" y="{top+bh/2-3}" width="6" height="6" fill="{T["violet"]}"/>')
    bx, bw = 512, W - 512 - 24
    for k, (name, sub, ic) in enumerate(LAYERS):
        y = top + k * (bh + gap)
        b.append(f'<line x1="{rx}" y1="{y+bh/2}" x2="{bx}" y2="{y+bh/2}" stroke="{T["border"]}"/>')
        b.append(f'<circle cx="{rx}" cy="{y+bh/2}" r="5" fill="{T["bg"]}" stroke="{T["violet"]}" stroke-width="2"/>')
        b.append(f'<g class="r" {d(.1*k)}><rect x="{bx}" y="{y}" width="{bw}" height="{bh}" fill="{T["surface"]}" stroke="{T["border"]}"/>'
                 f'<rect x="{bx}" y="{y}" width="{bw}" height="{bh}" fill="none" stroke="{T["violet"]}" stroke-width="1.5" class="lit" style="animation-delay:{k*0.6:.1f}s"/>'
                 f'<text x="{bx+20}" y="{y+37}" class="m v" font-size="13" letter-spacing="1">0{k+1}</text>'
                 f'<text x="{bx+62}" y="{y+28}" class="s t" font-size="16" font-weight="700">{e(name)}</text>'
                 f'<text x="{bx+62}" y="{y+47}" class="m mu" font-size="11">{e(sub)}</text>'
                 + (icon(ic, bx + bw - 44, y + 19, 24, T["muted"]) if ic else star(bx + bw - 32, y + bh / 2, 9, T["acc"]))
                 + '</g>')
        if k < len(LAYERS) - 1:
            b.append(f'<text x="{bx+bw/2}" y="{y+bh+14}" text-anchor="middle" class="m mu" font-size="11">↓</text>')
    return svg(W, H, "\n".join(b), T, css, "Platform engineering — production stack")


# ─────────────────────────────────────────────────────────────
# 8. DATA PIPELINE
# ─────────────────────────────────────────────────────────────
STEPS = ["RAW SOURCES", "CLEANING", "VALIDATION", "NORMALIZATION", "CENTRAL STUDENT DATA"]
CONSUMERS = ["ATTENDANCE", "GROUPING", "AUTH", "HELPDESK", "STUDENT SERVICES", "INTERNAL OPS"]


def pipeline(T):
    W, H = 1000, 430
    css = """
.hot{animation:hot 5s ease infinite}
@keyframes hot{0%,100%{opacity:.0}10%,30%{opacity:1}}
"""
    b = [grid(W, H, T, 40, "gd")]
    sw, sy, sh = 172, 40, 96
    gap = (W - 48 - 5 * sw) / 4
    for k, s in enumerate(STEPS):
        x = 24 + k * (sw + gap)
        last = k == len(STEPS) - 1
        fill = T["lime"] if last else T["surface"]
        cls_t = "ol" if last else "t"
        cls_i = "ol" if last else "v"
        lines = wrap(s, 14)
        txt = "".join(f'<tspan x="{x+16}" dy="{0 if j == 0 else 18}">{e(l)}</tspan>' for j, l in enumerate(lines))
        b.append(f'<g class="r" {d(.15*k)}><rect x="{x}" y="{sy}" width="{sw}" height="{sh}" fill="{fill}" stroke="{T["border"]}"/>'
                 f'<text x="{x+16}" y="{sy+28}" class="m {cls_i}" font-size="12" letter-spacing="2">0 {k+1}</text>'
                 f'<text x="{x+16}" y="{sy+60}" class="m {cls_t}" font-size="13" font-weight="700" letter-spacing="1">{txt}</text></g>')
        b.append(f'<rect x="{x}" y="{sy}" width="{sw}" height="3" fill="{T["violet"]}" class="hot" style="animation-delay:{k*0.8:.1f}s"/>')
        if not last:
            ax = x + sw
            b.append(f'<line x1="{ax+4}" y1="{sy+sh/2}" x2="{ax+gap-4}" y2="{sy+sh/2}" stroke="{T["violet"]}" stroke-width="2" class="flow"/>'
                     f'<path d="M{ax+gap-10},{sy+sh/2-5} L{ax+gap-3},{sy+sh/2} L{ax+gap-10},{sy+sh/2+5}" fill="none" stroke="{T["violet"]}" stroke-width="2"/>')
    # fan-out
    ox = 24 + 4 * (sw + gap) + sw / 2
    oy = sy + sh
    cw, cy = 146, 300
    cgap = (W - 48 - 6 * cw) / 5
    for k, c in enumerate(CONSUMERS):
        x = 24 + k * (cw + cgap)
        tx = x + cw / 2
        path = f"M{ox},{oy} C{ox},{oy+90} {tx},{cy-90} {tx},{cy}"
        b.append(f'<path d="{path}" fill="none" stroke="{T["border"]}" stroke-width="1.5"/>')
        b.append(f'<path d="{path}" fill="none" stroke="{T["acc"]}" stroke-width="1.5" class="flow" style="animation-duration:{.7+k*.12:.2f}s"/>')
        b.append(f'<g class="r" {d(.8+.08*k)}><rect x="{x}" y="{cy}" width="{cw}" height="40" fill="{T["surface"]}" stroke="{T["border"]}"/>'
                 f'<text x="{x+12}" y="{cy+25}" class="m a" font-size="12">+</text>'
                 f'<text x="{x+26}" y="{cy+25}" class="m t" font-size="11" letter-spacing="1">{e(c)}</text></g>')
    b.append(f'<circle cx="{ox}" cy="{oy}" r="5" class="a"/><circle cx="{ox}" cy="{oy}" r="5" class="a pulse"/>')
    b.append(f'<line x1="24" y1="368" x2="{W-24}" y2="368" stroke="{T["border"]}"/>')
    b.append(f'<g class="r" {d(1.2)}><text x="24" y="408" class="s t" font-size="30" font-weight="800" letter-spacing="-1">~8,000</text>'
             f'<text x="160" y="406" class="m mu" font-size="12" letter-spacing="2">STUDENT RECORDS · ONE SOURCE · MANY SYSTEMS</text></g>')
    b.append(star(W - 36, 398, 10, T["acc"]))
    return svg(W, H, "\n".join(b), T, css, "Data infrastructure pipeline")


# ─────────────────────────────────────────────────────────────
# 9. EXPERIENCE TIMELINE
# ─────────────────────────────────────────────────────────────
EXPERIENCE = [
    ("2025 — PRESENT", "Information Systems Coordinator", "OMB IPB 63 × Agrisymphony 2026", True),
    ("2025 — PRESENT", "Web Developer", "Code Panda", True),
    ("2025", "Web Developer", "Agrisymphony", False),
    ("2025", "Head of Research & Development", "Ormawa Eksekutif PKU IPB", False),
    ("2024", "Data Operations", "Balai Penyuluhan Pertanian Bekri", False),
]


def timeline(T):
    W, rh, top = 1000, 66, 56
    H = top + rh * len(EXPERIENCE) + 12
    b = [f'<text x="64" y="26" class="m mu" font-size="11" letter-spacing="2">YEAR</text>',
         f'<text x="290" y="26" class="m mu" font-size="11" letter-spacing="2">ROLE</text>',
         f'<text x="660" y="26" class="m mu" font-size="11" letter-spacing="2">ORGANIZATION</text>',
         f'<line x1="0" y1="40" x2="{W}" y2="40" stroke="{T["border"]}"/>',
         f'<line x1="28" y1="{top}" x2="28" y2="{H-24}" stroke="{T["border"]}" stroke-width="2"/>',
         f'<line x1="28" y1="{top}" x2="28" y2="{H-24}" stroke="{T["violet"]}" stroke-width="2" pathLength="1" class="draw"/>']
    for k, (yr, role, org, now) in enumerate(EXPERIENCE):
        y = top + k * rh
        cy = y + 22
        b.append(f'<g class="r" {d(.15*k)}>'
                 f'<text x="64" y="{cy+5}" class="m {"a" if now else "t"}" font-size="12" letter-spacing="1.5">{e(yr)}</text>'
                 f'<text x="290" y="{cy+6}" class="s t" font-size="18" font-weight="700">{e(role)}</text>'
                 f'<text x="660" y="{cy+5}" class="s mu" font-size="15">{e(org)}</text></g>')
        b.append(f'<line x1="64" y1="{y+rh-10}" x2="{W}" y2="{y+rh-10}" stroke="{T["border"]}" stroke-dasharray="2 4"/>')
        if now:
            b.append(f'<circle cx="28" cy="{cy}" r="6" class="a"/><circle cx="28" cy="{cy}" r="6" class="a pulse" {d(k*.6)}/>')
        else:
            b.append(f'<circle cx="28" cy="{cy}" r="5" fill="{T["bg"]}" stroke="{T["violet"]}" stroke-width="2"/>')
    return svg(W, H, "\n".join(b), T, "", "Experience timeline")


# ─────────────────────────────────────────────────────────────
# 10. SYSTEM STATUS
# ─────────────────────────────────────────────────────────────
STATUS = [
    ("CURRENT FOCUS", "Platform Engineering", None),
    ("LOCATION", "Bogor, Indonesia", None),
    ("TIMEZONE", "UTC+7", "clock"),
    ("AVAILABILITY", "Open to opportunities", "dot"),
    ("GITHUB", "@Asqara", None),
    ("ACTIVITY_STREAM", "ACTIVE", "eq"),
    ("GPA", "3.80 / 4.00", None),
    ("PROFILE", "OPERATIONAL", "dot"),
]


def status(T):
    W, H = 1000, 200
    cw, ch = 250, 100
    css = """
.eq{transform-box:fill-box;transform-origin:bottom;animation:eq .9s ease-in-out infinite alternate}
@keyframes eq{from{transform:scaleY(.2)}to{transform:scaleY(1)}}
.hand{transform-box:view-box;animation:spin 6s linear infinite}
"""
    b = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" fill="{T["surface"]}" stroke="{T["border"]}"/>',
         f'<line x1="0" y1="{ch}" x2="{W}" y2="{ch}" stroke="{T["border"]}"/>']
    for k, (lab, val, kind) in enumerate(STATUS):
        x = (k % 4) * cw
        y = (k // 4) * ch
        if k % 4:
            b.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+ch}" stroke="{T["border"]}"/>')
        b.append(f'<g class="r" {d(.07*k)}><text x="{x+22}" y="{y+36}" class="m mu" font-size="11" letter-spacing="2">{e(lab)}</text>'
                 f'<text x="{x+22}" y="{y+70}" class="s t" font-size="19" font-weight="700">{e(val)}</text></g>')
        if kind == "dot":
            b.append(f'<circle cx="{x+cw-26}" cy="{y+32}" r="4.5" class="a"/><circle cx="{x+cw-26}" cy="{y+32}" r="4.5" class="a pulse" {d(k*.3)}/>')
        elif kind == "eq":
            for j in range(5):
                b.append(f'<rect class="eq" x="{x+cw-62+j*8}" y="{y+18}" width="5" height="22" fill="{T["violet"]}" style="animation-delay:{j*0.13:.2f}s"/>')
        elif kind == "clock":
            cx, cy = x + cw - 32, y + 32
            b.append(f'<circle cx="{cx}" cy="{cy}" r="12" fill="none" stroke="{T["muted"]}" stroke-width="1.5"/>'
                     f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-9}" stroke="{T["acc"]}" stroke-width="2" class="hand" style="transform-origin:{cx}px {cy}px"/>'
                     f'<circle cx="{cx}" cy="{cy}" r="2" class="a"/>')
    return svg(W, H, "\n".join(b), T, css, "System status")


# ─────────────────────────────────────────────────────────────
# 11. CONTACT / FOOTER
# ─────────────────────────────────────────────────────────────
def contact(T):
    W, H = 1000, 360
    gx, gy, gr = 820, 160, 108
    css = f"""
.mer{{transform-box:view-box;transform-origin:{gx}px {gy}px;animation:mer 6s linear infinite}}
@keyframes mer{{0%{{transform:scaleX(1)}}50%{{transform:scaleX(-1)}}100%{{transform:scaleX(1)}}}}
"""
    b = [grid(W, H, T, 40, "gc")]
    b.append(f'<text x="24" y="44" class="m v r" font-size="13" letter-spacing="1.5">/ 14  <tspan class="mu">CONTACT / OPEN CHANNEL</tspan></text>')
    b.append(f'<g class="r" {d(.15)}><text x="20" y="124" class="s t" font-size="64" font-weight="800" letter-spacing="-2.5" textLength="370" lengthAdjust="spacingAndGlyphs">LET\'S BUILD</text></g>')
    b.append(f'<g class="r" {d(.3)}><text x="20" y="194" class="s t" font-size="64" font-weight="800" letter-spacing="-2.5" textLength="580" lengthAdjust="spacingAndGlyphs">SOMETHING USEFUL<tspan class="a">.</tspan></text></g>')
    b.append(f'<g class="r" {d(.45)}><text x="24" y="236" class="s mu" font-size="16">Open to software engineering opportunities, technical collaboration</text>'
             f'<text x="24" y="260" class="s mu" font-size="16">and building ambitious systems.</text></g>')
    # globe
    b.append(f'<circle cx="{gx}" cy="{gy}" r="{gr}" fill="{T["surface"]}" stroke="{T["text"]}" stroke-width="1.2"/>')
    for ry in (0.35, 0.7):
        b.append(f'<ellipse cx="{gx}" cy="{gy}" rx="{gr}" ry="{gr*ry*0.5:.0f}" fill="none" stroke="{T["border"]}"/>')
    b.append(f'<line x1="{gx-gr}" y1="{gy}" x2="{gx+gr}" y2="{gy}" stroke="{T["border"]}"/>')
    for k, rx in enumerate((0.25, 0.55, 0.85)):
        b.append(f'<g class="mer" style="animation-delay:-{k*1.2:.1f}s"><ellipse cx="{gx}" cy="{gy}" rx="{gr*rx:.0f}" ry="{gr}" fill="none" stroke="{T["violet"]}" stroke-width="1" opacity=".8"/></g>')
    mx, my = gx + 26, gy + 18
    b.append(f'<circle cx="{mx}" cy="{my}" r="5" class="a"/><circle cx="{mx}" cy="{my}" r="5" class="a pulse"/>'
             f'<line x1="{mx}" y1="{my}" x2="{mx+80}" y2="{my+70}" stroke="{T["acc"]}"/>'
             f'<text x="{mx+86}" y="{my+74}" class="m t" font-size="11" letter-spacing="1.5">BOGOR</text>')
    b.append(f'<text x="{W-24}" y="{gy+gr+30}" text-anchor="end" class="m mu f" font-size="11" letter-spacing="1.5" {d(.6)}>GLOBAL NODE · 06.5971° S 106.8060° E · UTC+7</text>')
    b.append(f'<line x1="0" y1="310" x2="{W}" y2="310" stroke="{T["border"]}"/>')
    b.append(f'<text x="24" y="340" class="m mu" font-size="11" letter-spacing="1.5">© 2026 ASQARA.TECH — SYSTEMS BUILT FOR REAL USE.</text>')
    b.append(f'<text x="{W-24}" y="340" text-anchor="end" class="m t" font-size="11" letter-spacing="1.5">START A CONVERSATION <tspan class="a">↗</tspan></text>')
    return svg(W, H, "\n".join(b), T, css, "Contact — Let's build something useful")


# ─────────────────────────────────────────────────────────────
# 12. DESIGN SYSTEM SHEETS
# ─────────────────────────────────────────────────────────────
def ds_palette(T, mode):
    W, H = 1000, 250
    keys = [("bg", "Background"), ("surface", "Surface"), ("border", "Border"), ("text", "Text"),
            ("muted", "Muted"), ("violet", "Violet / primary"), ("lime", "Lime / signal")]
    cw = (W - 48) / len(keys)
    b = [f'<text x="24" y="36" class="m v" font-size="13" letter-spacing="1.5">/ DS-01  <tspan class="mu">COLOR TOKENS — {mode.upper()}</tspan></text>']
    for k, (key, name) in enumerate(keys):
        x = 24 + k * cw
        b.append(f'<g class="r" {d(.07*k)}><rect x="{x}" y="58" width="{cw-10:.0f}" height="110" fill="{T[key]}" stroke="{T["border"]}"/>'
                 f'<text x="{x}" y="194" class="m t" font-size="12" font-weight="700">--{key}</text>'
                 f'<text x="{x}" y="214" class="m mu" font-size="11">{T[key]}</text>'
                 f'<text x="{x}" y="232" class="s mu" font-size="12">{e(name)}</text></g>')
    return svg(W, H, "\n".join(b), T, "", f"Color tokens ({mode})")


def ds_type(T):
    W, H = 1000, 420
    rows = [
        ("DISPLAY", "s t", 64, 800, -2.5, "SYSTEMS BUILT.", "Geist 800 · 64–96 · -0.04em · UPPERCASE"),
        ("H1", "s t", 40, 800, -1.4, "Selected systems.", "Geist 800 · 40 · -0.035em"),
        ("H2", "s t", 26, 700, -.6, "Platform engineering", "Geist 700 · 26"),
        ("BODY", "s mu", 16, 400, 0, "Software engineer building full-stack apps and data infrastructure.", "Geist 400 · 16 / 1.5"),
        ("LABEL", "m v", 13, 400, 1.5, "/ 04  SELECTED WORK", "Geist Mono 400 · 11–13 · +0.12em · UPPERCASE"),
        ("DATA", "m t", 12, 700, 1.5, "~1,000 RPS · UTC+7 · SCN_01", "Geist Mono 700 · 11–12 · tabular"),
    ]
    b = [f'<text x="24" y="36" class="m v" font-size="13" letter-spacing="1.5">/ DS-02  <tspan class="mu">TYPOGRAPHY</tspan></text>']
    y = 70
    for k, (tag, cls, size, wt, ls, sample, spec) in enumerate(rows):
        lh = max(size * 1.15, 34)
        y += lh
        b.append(f'<line x1="24" y1="{y-lh-6:.0f}" x2="{W-24}" y2="{y-lh-6:.0f}" stroke="{T["border"]}"/>')
        b.append(f'<g class="r" {d(.08*k)}><text x="24" y="{y-8:.0f}" class="m mu" font-size="10" letter-spacing="2">{tag}</text>'
                 f'<text x="120" y="{y-8:.0f}" class="{cls}" font-size="{size}" font-weight="{wt}" letter-spacing="{ls}">{e(sample)}</text>'
                 f'<text x="{W-24}" y="{y+12:.0f}" text-anchor="end" class="m mu" font-size="10">{e(spec)}</text></g>')
        y += 22
    return svg(W, int(y + 10), "\n".join(b), T, "", "Typography scale")


def ds_components(T):
    W, H = 1000, 360
    b = [f'<text x="24" y="36" class="m v" font-size="13" letter-spacing="1.5">/ DS-03  <tspan class="mu">COMPONENTS &amp; MOTION</tspan></text>']
    # buttons
    b.append(f'<text x="24" y="76" class="m mu" font-size="10" letter-spacing="2">BUTTONS</text>')
    b.append(f'<rect x="24" y="88" width="200" height="44" fill="{T["lime"]}"/><text x="44" y="115" class="m ol" font-size="12" font-weight="700" letter-spacing="1.5">START A PROJECT ↗</text>')
    b.append(f'<rect x="236" y="88" width="170" height="44" fill="none" stroke="{T["text"]}"/><text x="256" y="115" class="m t" font-size="12" letter-spacing="1.5">VIEW GITHUB ↗</text>')
    b.append(f'<text x="420" y="115" class="m v" font-size="12" letter-spacing="1.5">EXPLORE WORK ↗</text>')
    # chips & status
    b.append(f'<text x="24" y="168" class="m mu" font-size="10" letter-spacing="2">CHIPS / STATUS</text>')
    x = 24
    for t in ["Next.js", "TypeScript", "PostgreSQL", "k3s"]:
        c, w = chip(x, 180, t, T)
        b.append(c)
        x += w + 6
    b.append(f'<circle cx="{x+20}" cy="192" r="4" class="a"/><circle cx="{x+20}" cy="192" r="4" class="a pulse"/>'
             f'<text x="{x+32}" y="196" class="m t" font-size="11" letter-spacing="1.5">OPERATIONAL</text>')
    # index / glyph
    b.append(f'<text x="24" y="248" class="m mu" font-size="10" letter-spacing="2">GLYPHS</text>')
    b.append(f'<text x="24" y="284" class="m v" font-size="14" letter-spacing="2">/ 01</text>'
             f'<text x="84" y="284" class="m t" font-size="14" letter-spacing="2">0 1</text>'
             f'<text x="140" y="284" class="s a" font-size="22" font-weight="700">↗</text>'
             f'<text x="180" y="284" class="m mu" font-size="14">→ ↓ · ×</text>')
    b.append(star(276, 279, 10, T["acc"]))
    b.append(brackets(300, 258, 60, 40, T["muted"], 8, 1))
    # motion
    css = """.demo{animation:demo 2.4s cubic-bezier(.16,1,.3,1) infinite}@keyframes demo{0%{transform:translateY(14px);opacity:0}40%,80%{transform:none;opacity:1}100%{opacity:0}}"""
    b.append(f'<text x="560" y="76" class="m mu" font-size="10" letter-spacing="2">MOTION</text>')
    demos = [("rise", "900ms · ease-out-expo", f'<rect class="demo" x="560" y="96" width="120" height="30" fill="{T["violet"]}"/>'),
             ("flow", "900ms · linear ∞", f'<line x1="700" y1="111" x2="820" y2="111" stroke="{T["violet"]}" stroke-width="2" class="flow"/>'),
             ("pulse", "2.2s · ease-out ∞", f'<circle cx="870" cy="111" r="5" class="a"/><circle cx="870" cy="111" r="5" class="a pulse"/>')]
    for k, (n, spec, el) in enumerate(demos):
        b.append(el)
        bx = 560 + k * 140
        b.append(f'<text x="{bx}" y="150" class="m t" font-size="11">{n}</text><text x="{bx}" y="166" class="m mu" font-size="10">{spec}</text>')
    b.append(f'<line x1="560" y1="196" x2="{W-24}" y2="196" stroke="{T["border"]}"/>')
    b.append(f'<line x1="560" y1="196" x2="{W-24}" y2="196" stroke="{T["violet"]}" stroke-width="2" pathLength="1" class="draw"/>')
    b.append(f'<text x="560" y="218" class="m mu" font-size="10">draw · 1.6s · ease-out-expo</text>')
    b.append(f'<rect x="560" y="240" width="{W-584}" height="6" fill="{T["border"]}"/><rect x="560" y="240" width="300" height="6" fill="{T["lime"]}" class="grow"/>')
    b.append(f'<text x="560" y="266" class="m mu" font-size="10">grow · 1.6s · ease-out-expo</text>')
    b.append(f'<text x="560" y="318" class="m mu" font-size="10" letter-spacing="1.5">RADIUS 0 · BORDER 1PX · GRID 40PX · NO SHADOWS</text>')
    return svg(W, H, "\n".join(b), T, css, "Components and motion")


# ─────────────────────────────────────────────────────────────
def write(name, fn, *args):
    for mode, T in TOKENS.items():
        p = os.path.join(OUT, f"{name}-{mode}.svg")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(fn(T, *args))


def main():
    write("hero", hero)
    write("marquee", marquee)
    write("metrics", metrics)
    write("principles", principles)
    write("platform", platform)
    write("pipeline", pipeline)
    write("timeline", timeline)
    write("status", status)
    write("contact", contact)
    for slug, idx, label, title in SECTIONS:
        write(f"section/{slug}", section, idx, label, title)
    for i, p in enumerate(PROJECTS):
        write(f"projects/{p[0]}", card, i, p)
    os.makedirs(os.path.join(OUT, "ds"), exist_ok=True)
    for mode, T in TOKENS.items():
        with open(os.path.join(OUT, "ds", f"palette-{mode}.svg"), "w") as f:
            f.write(ds_palette(T, mode))
    write("ds/type", ds_type)
    write("ds/components", ds_components)
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    print(f"generated {n} files in {OUT}")


if __name__ == "__main__":
    main()
