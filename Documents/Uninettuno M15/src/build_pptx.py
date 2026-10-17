# -*- coding: utf-8 -*-
"""Generatore PowerPoint (.pptx) per Uninettuno M15 — Motori a turbina gas (18 lezioni).

Rispetta integralmente:
1. Format per la realizzazione delle videolezioni (Maria Amata Garito, Uninettuno):
   - Copertina con titolo corso, docente, università, numero e titolo lezione
   - Obiettivi, Domande di innesco, Prerequisiti, Indice ragionato
   - Sintesi intermedie con Termini chiave e Domande di verifica (Cyberspazio didattico)
   - Ricapitolazione finale con riferimenti al testo e slide Materiali della lezione
   - Palette cromatica: SOLO blu, verde, nero, giallo/oro in tutte le loro tonalità.
     VIETATO il rosso, VIETATO l'abbinamento puro bianco e nero. Sfondo omogeneo.
2. Best practice grafiche e feedback utente:
   - IMMAGINI PROTAGONISTE: le figure occupano l'intera larghezza e altezza utile, senza miniaturizzazioni.
   - NESSUNA FORMA/DISEGNO ARTEFATTO: zero icone disegnate a mano con archi/cerchi; la copertina usa
     la vera immagine 3D fotorealistica del motore (img/ai_copertina.jpg); le slide introduttive usano
     layout tipografico puro ed editoriale con badge numerici eleganti.
   - SDOPPIAMENTO SLIDE: quando una sezione contiene sia teoria/tabelle/formule sia figure, vengono generate
     due slide distinte (Teoria a tutta larghezza + Figura gigante protagonista) sincronizzando il copione.
   - Font safe-list (Cambria per titoli, Calibri per corpo e tabelle).
   - Copione integrale inserito nelle Note del relatore (Speaker Notes) di ciascuna slide.
"""
import hashlib
import html
import math
import os
import pathlib
import re
import subprocess
import sys

import fitz  # PyMuPDF
from bs4 import BeautifulSoup, NavigableString
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

sys.stdout.reconfigure(encoding="utf-8")

SRC = pathlib.Path(__file__).resolve().parent
ROOT = SRC.parent
FIG_DIR = ROOT / "fig"
IMG_DIR = ROOT / "img"
OUT_DIR = ROOT / "pptx"
CACHE_DIR = SRC / "_pptx_cache"
MIKTEX_PDFLATEX = r"C:\Users\Gianmarco\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe"

DOCENTE = "Ing. Gianmarco Ardia"
UNIV = "Università Telematica Internazionale UNINETTUNO"
CORSO = "Motori a turbina gas"
SOTTO_CORSO = "Ingegneria Gestionale — Indirizzo Manutentore Aeronautico (9 CFU · 18 ore)"
CYBER = "www.uninettunouniversity.net"

# ==============================================================================
# PALETTE UNINETTUNO (Blu, Verde, Nero-Antracite, Giallo/Oro — ZERO ROSSO,
# ZERO BIANCO/NERO PURO, SFONDI OMOGENEI)
# ==============================================================================
BG_DARK = RGBColor(0x0B, 0x25, 0x45)       # Blu notte profondo (Copertina, Sintesi, Recap, Finale)
BG_LIGHT = RGBColor(0xEE, 0xF5, 0xFA)      # Blu ghiaccio omogeneo (Slide di contenuto)

C_BLUE = RGBColor(0x0B, 0x5F, 0x8A)        # Blu primario
C_BLUE_DARK = RGBColor(0x08, 0x3D, 0x5E)   # Blu profondo
C_GREEN = RGBColor(0x0A, 0x7F, 0x6B)       # Verde ottanio / smeraldo tecnico
C_GREEN_DARK = RGBColor(0x07, 0x59, 0x4B)  # Verde profondo
C_GOLD = RGBColor(0xB3, 0x7D, 0x00)        # Giallo ocra / oro scuro (alta leggibilità su chiaro)
C_GOLD_BRIGHT = RGBColor(0xF2, 0xB7, 0x05) # Giallo oro brillante (per sfondi scuri)
C_INK = RGBColor(0x10, 0x1E, 0x2B)         # Nero-blu antracite per testo principale
C_MUTED = RGBColor(0x3B, 0x52, 0x66)       # Grigio-blu ardesia per didascalie e note
C_LIGHT_TXT = RGBColor(0xF2, 0xF7, 0xFA)   # Testo chiaro su card scure
C_ICE_TXT = RGBColor(0xC9, 0xE2, 0xF5)     # Testo azzurro ghiaccio su card scure

# Card su sfondo chiaro
CARD_BASE = RGBColor(0xF8, 0xFB, 0xFE)
BORD_BASE = RGBColor(0xBD, 0xD3, 0xE6)

TINT_BLUE = RGBColor(0xDF, 0xEE, 0xF8)
BORD_BLUE = RGBColor(0x8A, 0xB8, 0xD9)

TINT_GREEN = RGBColor(0xDC, 0xF2, 0xEC)
BORD_GREEN = RGBColor(0x82, 0xC4, 0xB2)

TINT_GOLD = RGBColor(0xFC, 0xF3, 0xD6)
BORD_GOLD = RGBColor(0xDF, 0xBE, 0x62)

# Card su sfondo scuro
CARD_DARK_BLUE = RGBColor(0x13, 0x38, 0x63)
BORD_DARK_BLUE = RGBColor(0x28, 0x5A, 0x91)
CARD_DARK_GREEN = RGBColor(0x0D, 0x4A, 0x4D)
BORD_DARK_GREEN = RGBColor(0x1F, 0x7A, 0x70)
CARD_DARK_GOLD = RGBColor(0x3B, 0x35, 0x18)
BORD_DARK_GOLD = RGBColor(0x9E, 0x7B, 0x16)

ACCENT_CYCLE = [
    (C_BLUE, TINT_BLUE, BORD_BLUE),
    (C_GREEN, TINT_GREEN, BORD_GREEN),
    (C_GOLD, TINT_GOLD, BORD_GOLD),
    (C_BLUE_DARK, TINT_BLUE, BORD_BLUE),
]

DARK_CYCLE = [
    (C_GOLD_BRIGHT, CARD_DARK_BLUE, BORD_DARK_BLUE),
    (C_GREEN, CARD_DARK_GREEN, BORD_DARK_GREEN),
    (C_BLUE, CARD_DARK_BLUE, BORD_DARK_BLUE),
]

FONT_HEAD = "Cambria"
FONT_BODY = "Calibri"

SLIDE_W = 10.0
SLIDE_H = 5.625


# ==============================================================================
# 1. RENDERING SVG (SENZA ROSSO) E FORMULE LATEX AD ALTA RISOLUZIONE (600 DPI)
# ==============================================================================
def get_svg_png(fig_name: str) -> pathlib.Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    out_png = CACHE_DIR / f"svg_{fig_name}.png"
    svg_path = FIG_DIR / f"{fig_name}.svg"
    if out_png.exists() and out_png.stat().st_mtime >= svg_path.stat().st_mtime:
        return out_png

    svg_content = svg_path.read_text(encoding="utf-8")
    # Bonifica cromatica totale su SVG: elimina ogni rosso e sostituisci con ocra/oro Uninettuno
    red_replacements = [
        ("#b3261e", "#b37d00"),
        ("#c0392b", "#b37d00"),
        ("#d32f2f", "#b37d00"),
        ("#e74c3c", "#b37d00"),
        ("#ff0000", "#b37d00"),
        ("red", "#b37d00"),
    ]
    for old_c, new_c in red_replacements:
        svg_content = svg_content.replace(old_c, new_c)
        svg_content = svg_content.replace(old_c.upper(), new_c)

    doc = fitz.open(stream=svg_content.encode("utf-8"), filetype="svg")
    page = doc[0]
    pix = page.get_pixmap(dpi=300, alpha=False)
    pix.save(str(out_png))
    doc.close()
    return out_png


def resolve_img(kind: str, name: str) -> pathlib.Path:
    if kind == "FIG":
        return get_svg_png(name)
    candidates = [
        IMG_DIR / f"{name}.jpg",
        IMG_DIR / f"{name}.png",
        IMG_DIR / f"ai_{name}.jpg",
        IMG_DIR / f"ai_{name}.png",
    ]
    for c in candidates:
        if c.exists():
            return c
    for f in IMG_DIR.glob(f"*{name}*"):
        if f.suffix.lower() in (".jpg", ".jpeg", ".png"):
            return f
    raise FileNotFoundError(f"Immagine non trovata per {kind}:{name} in {IMG_DIR}")


def sanitize_tex_for_pdflatex(eq: str) -> str:
    s = eq.strip()
    s = re.sub(r"\\d(?![a-zA-Z])", r"\\mathrm{d}", s)
    s = s.replace("{,}", "{,}")
    s = s.replace(r"\minus", "-")
    return s


def precompile_latex_formulas(all_equations: list[str]) -> dict[str, pathlib.Path]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    mapping = {}
    unique_eqs = list(dict.fromkeys(all_equations))
    for eq in unique_eqs:
        eq_hash = hashlib.sha256(eq.encode("utf-8")).hexdigest()[:16]
        out_png = CACHE_DIR / f"eq_{eq_hash}.png"
        mapping[eq] = out_png
        if out_png.exists():
            continue

        clean_eq = sanitize_tex_for_pdflatex(eq)
        tex_content = "\n".join([
            r"\documentclass[preview,border=4pt]{standalone}",
            r"\usepackage[utf8]{inputenc}",
            r"\usepackage[T1]{fontenc}",
            r"\usepackage{lmodern}",
            r"\usepackage{amsmath,amssymb}",
            r"\usepackage{xcolor}",
            r"\pagestyle{empty}",
            r"\definecolor{eqcol}{HTML}{0B2545}",
            r"\begin{document}",
            r"\color{eqcol}",
            r"\[ \displaystyle " + clean_eq + r" \]",
            r"\end{document}",
        ])
        tex_file = CACHE_DIR / f"single_{eq_hash}.tex"
        pdf_file = CACHE_DIR / f"single_{eq_hash}.pdf"
        tex_file.write_text(tex_content, encoding="utf-8")
        subprocess.run(
            [MIKTEX_PDFLATEX, "-interaction=nonstopmode", f"single_{eq_hash}.tex"],
            cwd=str(CACHE_DIR),
            capture_output=True,
            text=True,
        )
        if pdf_file.exists():
            doc = fitz.open(str(pdf_file))
            page = doc[0]
            pix = page.get_pixmap(dpi=600, alpha=True)
            im = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)
            bbox = im.getbbox()
            if bbox:
                pad = 14
                x0 = max(0, bbox[0] - pad)
                y0 = max(0, bbox[1] - pad)
                x1 = min(im.width, bbox[2] + pad)
                y1 = min(im.height, bbox[3] + pad)
                im = im.crop((x0, y0, x1, y1))
            im.save(out_png)
            doc.close()
    return mapping


# ==============================================================================
# 2. CONVERSIONE MATEMATICA INLINE E PARSING HTML CON RUN NATIVI
# ==============================================================================
DOT_MAP = {
    "m": "ṁ", "M": "Ṁ", "E": "Ė", "e": "ė", "x": "ẋ", "X": "Ẋ",
    "y": "ẏ", "z": "ż", "Z": "Ż", "w": "ẇ", "W": "Ẇ", "r": "ṙ",
    "s": "ṡ", "p": "ṗ", "v": "v̇", "V": "V̇", "q": "q̇", "Q": "Q̇",
}

GREEK_MAP = {
    r"\alpha": "α", r"\beta": "β", r"\gamma": "γ", r"\delta": "δ", r"\Delta": "Δ",
    r"\varepsilon": "ε", r"\epsilon": "ε", r"\eta": "η", r"\theta": "θ", r"\vartheta": "ϑ",
    r"\lambda": "λ", r"\mu": "μ", r"\nu": "ν", r"\pi": "π", r"\rho": "ρ",
    r"\sigma": "σ", r"\tau": "τ", r"\omega": "ω", r"\Omega": "Ω",
    r"\simeq": " ≃ ", r"\approx": " ≈ ", r"\propto": " ∝ ", r"\sim": " ~ ",
    r"\equiv": " ≡ ", r"\ne": " ≠ ", r"\neq": " ≠ ", r"\le": " ≤ ", r"\leq": " ≤ ",
    r"\ge": " ≥ ", r"\geq": " ≥ ", r"\infty": "∞", r"\partial": "∂", r"\nabla": "∇",
    r"\rightarrow": " → ", r"\to": " → ", r"\Rightarrow": " ⇒ ",
    r"\longrightarrow": " ⟶ ", r"\Longrightarrow": " ⟹ ",
    r"\longleftrightarrow": " ⟺ ", r"\Longleftrightarrow": " ⟺ ",
    r"\times": " × ", r"\cdot": "·", r"\div": "÷", r"\minus": "−", r"\pm": "±",
    r"\mp": "∓", r"\sum": "∑", r"\prod": "∏", r"\int": "∫",
    r"\angle": "∠", r"\ell": "ℓ", r"\checkmark": "✓",
    r"\tfrac12": "½", r"\frac12": "½", r"\tfrac{1}{2}": "½", r"\tfrac{9}{10}": "9/10",
    r"\mathrm{d}": "d", r"\cos": "cos ", r"\sin": "sin ", r"\tan": "tan ",
    r"\ln": "ln ", r"\log": "log ",
    r"\%": "%", r"\_": "_", r"\&": "&",
    r"\qquad": "   ", r"\quad": "  ", r"\enspace": " ",
    r"\,": " ", r"\;": " ", r"\ ": " ",
}


def parse_balanced_arg(s: str, start_idx: int) -> tuple[str | None, int]:
    """Estrae l'argomento racchiuso tra parentesi graffe bilanciate partendo da start_idx."""
    if start_idx >= len(s) or s[start_idx] != "{":
        return None, start_idx
    depth = 0
    for i in range(start_idx, len(s)):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return s[start_idx + 1:i], i + 1
    return None, start_idx


def inline_math_to_text(expr: str, for_speech: bool = False) -> str:
    """Converte un'espressione LaTeX in testo pulito e naturale, senza residui di codice."""
    s = html.unescape(expr.strip())
    s = s.replace("{,}", ",")

    # Rimozione parentesi di dimensionamento LaTeX
    s = re.sub(r"\\left\s*[\(\[\{]", lambda m: m.group(0)[-1], s)
    s = re.sub(r"\\right\s*[\)\]\}]", lambda m: m.group(0)[-1], s)
    s = re.sub(r"\\left\.|\\right\.", "", s)

    # Underbrace e overbrace
    while True:
        m = re.search(r"\\(underbrace|overbrace)\b", s)
        if not m:
            break
        idx = m.end()
        while idx < len(s) and s[idx].isspace():
            idx += 1
        main_arg, idx2 = parse_balanced_arg(s, idx)
        if main_arg is None:
            break
        while idx2 < len(s) and s[idx2].isspace():
            idx2 += 1
        sub_arg = None
        if idx2 < len(s) and s[idx2] in ("_", "^"):
            idx3 = idx2 + 1
            while idx3 < len(s) and s[idx3].isspace():
                idx3 += 1
            sub_arg, idx4 = parse_balanced_arg(s, idx3)
            idx_end = idx4 if sub_arg is not None else idx2
        else:
            idx_end = idx2
        if sub_arg:
            sub_clean = re.sub(r"\\text\{([^}]*)\}", r"\1", sub_arg).strip()
            rep = f"{main_arg} [{sub_clean}]"
        else:
            rep = main_arg
        s = s[:m.start()] + rep + s[idx_end:]

    # Frazioni annidate con parser bilanciato
    while True:
        m = re.search(r"\\(d|t)?frac\b", s)
        if not m:
            break
        idx = m.end()
        while idx < len(s) and s[idx].isspace():
            idx += 1
        num, idx2 = parse_balanced_arg(s, idx)
        if num is None:
            break
        while idx2 < len(s) and s[idx2].isspace():
            idx2 += 1
        den, idx3 = parse_balanced_arg(s, idx2)
        if den is None:
            break
        s = s[:m.start()] + f"({num})/({den})" + s[idx3:]

    # Radici quadrate (con e senza graffe)
    while True:
        m = re.search(r"\\sqrt\b", s)
        if not m:
            break
        idx = m.end()
        while idx < len(s) and s[idx].isspace():
            idx += 1
        arg, idx2 = parse_balanced_arg(s, idx)
        if arg is not None:
            s = s[:m.start()] + f"√({arg})" + s[idx2:]
        else:
            m_token = re.match(r"\\([a-zA-Z]+)|([a-zA-Z0-9])", s[idx:])
            if m_token:
                tok = m_token.group(0)
                tok_clean = GREEK_MAP.get(tok, tok.lstrip("\\"))
                s = s[:m.start()] + f"√{tok_clean}" + s[idx + len(tok):]
            else:
                break

    # Spacchettamento macro di testo e boxature
    for tag in ["mathrm", "text", "mathbf", "bm", "bold", "boxed"]:
        while True:
            m = re.search(r"\\" + tag + r"\b", s)
            if not m:
                break
            idx = m.end()
            while idx < len(s) and s[idx].isspace():
                idx += 1
            if idx < len(s) and s[idx] == "{":
                arg, idx2 = parse_balanced_arg(s, idx)
                if arg is not None:
                    s = s[:m.start()] + arg + s[idx2:]
                    continue
            # Se non ci sono graffe, consuma un token singolo o rimuovi il comando
            m_tok = re.match(r"\\[a-zA-Z]+|[a-zA-Z0-9]+", s[idx:])
            if m_tok:
                tok = m_tok.group(0)
                tok_clean = GREEK_MAP.get(tok, tok.lstrip("\\"))
                s = s[:m.start()] + tok_clean + s[idx + len(tok):]
            else:
                s = s[:m.start()] + s[idx:]

    # Derivate temporali, vettori e barre (con caratteri Unicode precomposti standard)
    s = re.sub(r"\\ddot\s*\{?([a-zA-Z])\}?", lambda m: m.group(1) + "\u0308", s)
    s = re.sub(r"\\dot\s*\{?([a-zA-Z])\}?", lambda m: DOT_MAP.get(m.group(1), m.group(1) + "\u0307"), s)
    s = re.sub(r"\\vec\s*\{?([a-zA-Z])\}?", lambda m: m.group(1) + "\u20d7", s)
    s = re.sub(r"\\bar\s*\{?([a-zA-Z0-9])\}?", lambda m: m.group(1) + "\u0304", s)

    s = re.sub(r"\^\s*\{?\s*\\circ\s*\}?", "°", s)

    # Mappa simboli e lettere greche
    for k, v in sorted(GREEK_MAP.items(), key=lambda x: -len(x[0])):
        s = s.replace(k, v)

    s = re.sub(r"\\d(?![a-zA-Z])", "d", s)

    # Gestione pedici e apici
    if for_speech:
        s = re.sub(r"_\{([^}]*)\}", r"_\1", s)
        s = re.sub(r"_([a-zA-Z0-9]+)", r"_\1", s)
        s = re.sub(r"\^\{([^}]*)\}", r"^\1", s)
        s = re.sub(r"\^([a-zA-Z0-9+-]+)", r"^\1", s)
    else:
        s = re.sub(r"_\{([^}]*)\}", lambda m: f"<sub>{html.escape(m.group(1))}</sub>", s)
        s = re.sub(r"_([a-zA-Z0-9]+)", lambda m: f"<sub>{html.escape(m.group(1))}</sub>", s)
        s = re.sub(r"\^\{([^}]*)\}", lambda m: f"<sup>{html.escape(m.group(1))}</sup>", s)
        s = re.sub(r"\^([a-zA-Z0-9+-]+)", lambda m: f"<sup>{html.escape(m.group(1))}</sup>", s)

    # Pulizia finale da comandi LaTeX orfani o residui e graffe
    s = re.sub(r"\\[a-zA-Z]+", "", s)
    s = s.replace("{", "").replace("}", "")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def clean_html_to_segments(node_or_html) -> list[tuple[str, bool, bool, int]]:
    if isinstance(node_or_html, str):
        s = node_or_html
    else:
        s = "".join(str(c) for c in node_or_html.contents)

    s = s.replace("della linea rossa il compressore", "della linea di pompaggio il compressore")
    s = s.replace("rosso, ambra, verde:", "livelli di allarme e avviso:")

    s = re.sub(
        r"\\\((.*?)\\\)",
        lambda m: f"<m>{inline_math_to_text(m.group(1))}</m>",
        s,
        flags=re.S,
    )
    s = s.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    soup = BeautifulSoup(s, "html.parser")
    segments = []

    def walk(n, b=False, it=False, sc=0):
        if isinstance(n, NavigableString):
            txt = html.unescape(str(n))
            if txt:
                segments.append((txt, b, it, sc))
        elif getattr(n, "name", None):
            nb = b or (n.name in ("b", "strong", "th"))
            nit = it or (n.name in ("i", "em", "m"))
            nsc = -1 if n.name == "sub" else (1 if n.name == "sup" else sc)
            for child in n.children:
                walk(child, nb, nit, nsc)

    walk(soup)
    cleaned = []
    for txt, b, it, sc in segments:
        parts = txt.split("\n")
        parts = [re.sub(r"[ \t\r\f\v]+", " ", p) for p in parts]
        txt_norm = "\n".join(parts)
        if txt_norm:
            cleaned.append((txt_norm, b, it, sc))
    return cleaned


def plain_text_of(node_or_html) -> str:
    segs = clean_html_to_segments(node_or_html)
    return "".join(t for t, _, _, _ in segs).strip()


def fill_paragraph_segments(
    para,
    segments: list,
    font_size: float,
    base_color: RGBColor,
    bold_color: RGBColor = None,
    math_color: RGBColor = None,
    font_name: str = FONT_BODY,
    force_bold: bool = False,
):
    if bold_color is None:
        bold_color = base_color
    if math_color is None:
        math_color = bold_color
    for seg in segments:
        if len(seg) == 3:
            txt, is_b, is_it = seg
            sc = 0
        else:
            txt, is_b, is_it, sc = seg
        run = para.add_run()
        run.text = txt
        run.font.name = font_name
        run.font.size = Pt(font_size)
        run.font.bold = bool(force_bold or is_b)
        run.font.italic = bool(is_it and sc == 0)
        if is_b:
            run.font.color.rgb = bold_color
        elif is_it:
            run.font.color.rgb = math_color
        else:
            run.font.color.rgb = base_color
        if sc == -1:
            run._r.get_or_add_rPr().set("baseline", "-25000")
        elif sc == 1:
            run._r.get_or_add_rPr().set("baseline", "30000")


# ==============================================================================
# 3. PARSING E SDOPPIAMENTO INTELLIGENTE DELLE SLIDE (IMMAGINI PROTAGONISTE)
# ==============================================================================
S_RE = re.compile(r"<!--S(.*?)-->(.*?)<!--/S-->", re.S)


def html_to_speaker_notes(raw_html: str) -> str:
    if not raw_html.strip():
        return ""
    s = re.sub(
        r'<div class="reg">\s*(.*?)\s*</div>',
        lambda m: "\n[REGIA: " + plain_text_of(m.group(1)) + "]\n",
        raw_html,
        flags=re.S,
    )
    s = re.sub(r"<figure>.*?</figure>", "", s, flags=re.S)
    s = re.sub(
        r"\\\[(.*?)\\\]",
        lambda m: "\n  Formula: " + inline_math_to_text(m.group(1), for_speech=True) + "\n",
        s,
        flags=re.S,
    )
    s = re.sub(
        r"\\\((.*?)\\\)",
        lambda m: inline_math_to_text(m.group(1), for_speech=True),
        s,
        flags=re.S,
    )
    soup = BeautifulSoup(s, "html.parser")
    paras = []
    for el in soup.find_all(["p", "div", "li"]):
        if el.name == "div" and "box" in (el.get("class") or []):
            continue
        t = html.unescape(el.get_text(" ", strip=True))
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            paras.append(t)
    if not paras:
        t = html.unescape(soup.get_text(" ", strip=True))
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            paras.append(t)
    return "\n\n".join(paras)


def parse_slide_body(body_html: str) -> dict:
    b = body_html.strip()
    b = re.sub(
        r"\\\[(.*?)\\\]",
        lambda m: f"<mathblock>{html.escape(m.group(1).strip())}</mathblock>",
        b,
        flags=re.S,
    )
    soup = BeautifulSoup(b, "html.parser")
    data = {
        "h3": None,
        "cits": [],
        "notas": [],
        "paras": [],
        "figures": [],     # list of (kind, name, caption_html)
        "mathblocks": [],  # list of raw tex strings
        "tables": [],      # list of rows
        "lists": [],       # list of (is_ordered, items_html_list)
    }

    for node in soup.children:
        if isinstance(node, NavigableString):
            s = str(node).strip()
            for kind, name in re.findall(r"\{\{(IMG|FIG):([a-z0-9_]+)\}\}", s):
                data["figures"].append((kind, name, ""))
            continue
        name = getattr(node, "name", None)
        if not name:
            continue
        if name == "h3":
            data["h3"] = str(node)
        elif name == "mathblock":
            data["mathblocks"].append(html.unescape(node.get_text()).strip())
        elif name == "figure":
            raw_f = str(node)
            m = re.search(r"\{\{(IMG|FIG):([a-z0-9_]+)\}\}", raw_f)
            cap_node = node.find("figcaption")
            cap_html = str(cap_node) if cap_node else ""
            if m:
                data["figures"].append((m.group(1), m.group(2), cap_html))
        elif name == "div" and "due" in (node.get("class") or []):
            for fig in node.find_all("figure"):
                raw_f = str(fig)
                m = re.search(r"\{\{(IMG|FIG):([a-z0-9_]+)\}\}", raw_f)
                cap_node = fig.find("figcaption")
                cap_html = str(cap_node) if cap_node else ""
                if m:
                    data["figures"].append((m.group(1), m.group(2), cap_html))
        elif name in ("ul", "ol"):
            items = [str(li) for li in node.find_all("li", recursive=False)]
            data["lists"].append((name == "ol", items))
        elif name == "table":
            rows = []
            for tr in node.find_all("tr"):
                row = []
                for cell in tr.find_all(["th", "td"]):
                    is_h = cell.name == "th"
                    is_n = "n" in (cell.get("class") or [])
                    row.append((str(cell), is_h, is_n))
                if row:
                    rows.append(row)
            if rows:
                data["tables"].append(rows)
        elif name == "p":
            cls = node.get("class") or []
            raw_p = str(node)
            for kind, img_name in re.findall(r"\{\{(IMG|FIG):([a-z0-9_]+)\}\}", raw_p):
                data["figures"].append((kind, img_name, ""))
            cleaned_p = re.sub(r"\{\{(IMG|FIG):([a-z0-9_]+)\}\}", "", raw_p)
            if plain_text_of(cleaned_p):
                if "cit" in cls:
                    data["cits"].append(cleaned_p)
                elif "nota" in cls:
                    data["notas"].append(cleaned_p)
                else:
                    data["paras"].append(cleaned_p)
    return data


def has_non_fig_content(body: dict) -> bool:
    return bool(
        body["cits"]
        or body["mathblocks"]
        or body["tables"]
        or body["lists"]
        or body["paras"]
        or body["notas"]
    )


def parse_lesson_file(filepath: pathlib.Path, lesson_num: int, total_lessons: int) -> dict:
    t = filepath.read_text(encoding="utf-8")
    h2_m = re.search(r"<h2[^>]*>(.*?)</h2>", t, re.S)
    lesson_title = plain_text_of(h2_m.group(1)) if h2_m else filepath.stem

    matches = list(S_RE.finditer(t))
    slides = []

    # 1. Slide Copertina
    pre_text = t[h2_m.end():matches[0].start()] if (h2_m and matches) else ""
    slides.append({
        "type": "cover",
        "title": lesson_title,
        "body": {},
        "notes": html_to_speaker_notes(pre_text) or f"Lezione {lesson_num} di {total_lessons}: {lesson_title}.",
    })

    # 2. Slide interne con sdoppiamento intelligente:
    # Se una sezione ha SIA testo/tabelle/formule SIA figure, la sdoppiamo in:
    #   A) Teoria / Dati / Formule a tutta pagina
    #   B) Figura Protagonista GIGANTE a tutta pagina
    for idx, m in enumerate(matches):
        s_title = plain_text_of(m.group(1))
        s_body_raw = m.group(2)
        next_start = matches[idx + 1].start() if idx + 1 < len(matches) else t.rfind("</section>")
        spoken_raw = t[m.end():next_start]
        full_notes = html_to_speaker_notes(spoken_raw)
        parsed_b = parse_slide_body(s_body_raw)

        figs = parsed_b["figures"]
        has_other = has_non_fig_content(parsed_b)

        if figs and has_other:
            # Sdoppia in due slide consecutive!
            # Slide A: Teoria / Formule / Liste / Tabelle
            body_theory = {
                "h3": parsed_b["h3"],
                "cits": list(parsed_b["cits"]),
                "notas": list(parsed_b["notas"]),
                "paras": list(parsed_b["paras"]),
                "figures": [],
                "mathblocks": list(parsed_b["mathblocks"]),
                "tables": list(parsed_b["tables"]),
                "lists": list(parsed_b["lists"]),
            }
            # Slide B: Figura Protagonista
            body_figure = {
                "h3": parsed_b["h3"],
                "cits": [],
                "notas": [],
                "paras": [],
                "figures": list(figs),
                "mathblocks": [],
                "tables": [],
                "lists": [],
            }

            # Suddividi le note del copione:
            # Paragrafi che fanno riferimento a figure/schemi/motore vs introduzione teorica
            paras_raw = [p.strip() for p in full_notes.split("\n\n") if p.strip()]
            theory_paras = []
            figure_paras = []
            for p in paras_raw:
                p_lower = p.lower()
                if any(w in p_lower for w in ("figura", "schema", "grafico", "diagramma", "guardate", "vedete", "rotore", "sezione", "disegno")):
                    figure_paras.append(p)
                else:
                    theory_paras.append(p)

            notes_a = "\n\n".join(theory_paras) if theory_paras else full_notes
            notes_b = "\n\n".join(figure_paras) if figure_paras else f"[PROIEZIONE SCHEMA / FIGURA]\n\n{full_notes}"

            slides.append({
                "type": "inner",
                "title": s_title,
                "body": body_theory,
                "notes": notes_a,
            })
            slides.append({
                "type": "inner",
                "title": f"{s_title} — Schema e componenti",
                "body": body_figure,
                "notes": notes_b,
            })
        else:
            slides.append({
                "type": "inner",
                "title": s_title,
                "body": parsed_b,
                "notes": full_notes,
            })

    # 3. Slide finale Uninettuno: Materiali della lezione
    slides.append({
        "type": "closing",
        "title": "Materiali della lezione",
        "body": {},
        "notes": (
            "Tutto il materiale di questa lezione, le slide, le esercitazioni e le domande di verifica, "
            "lo trovate nella mia pagina dell'ambiente di apprendimento UNINETTUNO "
            f"({CYBER}). Buono studio, e arrivederci."
        ),
    })

    return {
        "num": lesson_num,
        "total": total_lessons,
        "stem": filepath.stem,
        "title": lesson_title,
        "slides": slides,
    }


# ==============================================================================
# 4. PRIMITIVE POWERPOINT (ZERO ACCENT LINES, ZERO STRIPES, ANTI-OVERFLOW)
# ==============================================================================
def set_slide_bg(slide, color: RGBColor):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_rounded_card(
    slide,
    x: float,
    y: float,
    w: float,
    h: float,
    fill_color: RGBColor,
    border_color: RGBColor = None,
    border_pt: float = 1.2,
    radius: float = 0.04,
):
    shp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h)
    )
    shp.adjustments[0] = radius
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill_color
    if border_color is not None:
        shp.line.color.rgb = border_color
        shp.line.width = Pt(border_pt)
    else:
        shp.line.fill.background()
    return shp


def add_circle_badge(
    slide,
    cx: float,
    cy: float,
    d: float,
    fill_color: RGBColor,
    label: str,
    text_color: RGBColor = C_LIGHT_TXT,
    font_size: float = 12.0,
):
    shp = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(cx - d / 2), Inches(cy - d / 2), Inches(d), Inches(d)
    )
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill_color
    shp.line.fill.background()
    tf = shp.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = label
    r.font.name = FONT_BODY
    r.font.size = Pt(font_size)
    r.font.bold = True
    r.font.color.rgb = text_color
    return shp


def add_text_box(
    slide,
    x: float,
    y: float,
    w: float,
    h: float,
    segments: list[tuple[str, bool, bool]],
    font_size: float,
    base_color: RGBColor,
    bold_color: RGBColor = None,
    math_color: RGBColor = None,
    font_name: str = FONT_BODY,
    align=PP_ALIGN.LEFT,
    valign=MSO_ANCHOR.MIDDLE,
    force_bold: bool = False,
    line_spacing: float = 1.15,
):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = line_spacing
    fill_paragraph_segments(
        p,
        segments,
        font_size=font_size,
        base_color=base_color,
        bold_color=bold_color,
        math_color=math_color,
        font_name=font_name,
        force_bold=force_bold,
    )
    return tb


def estimate_fitted_fontsize(
    text: str,
    box_w_in: float,
    box_h_in: float,
    max_pt: float = 15.0,
    min_pt: float = 9.5,
    line_spacing: float = 1.18,
) -> float:
    clean = re.sub(r"\s+", " ", text).strip()
    n_chars = max(1, len(clean))
    explicit_breaks = text.count("\n")
    for pt in [max_pt - 0.5 * k for k in range(int((max_pt - min_pt) * 2) + 1)]:
        chars_per_line = max(10, int((box_w_in * 72.0) / (pt * 0.53)))
        n_lines = math.ceil(n_chars / chars_per_line) + explicit_breaks
        req_h_in = (n_lines * pt * line_spacing) / 72.0
        if req_h_in <= box_h_in * 0.90:
            return pt
    return min_pt


def add_picture_contained(
    slide, img_path: pathlib.Path, x: float, y: float, w: float, h: float
):
    """Inserisce un'immagine perfettamente centrata nel box (x, y, w, h) preservando l'aspect ratio."""
    with Image.open(img_path) as im:
        iw, ih = im.size
    aspect = iw / max(1, ih)
    box_aspect = w / max(0.01, h)
    if aspect >= box_aspect:
        pw = w
        ph = w / aspect
    else:
        ph = h
        pw = h * aspect
    px = x + (w - pw) / 2.0
    py = y + (h - ph) / 2.0
    return slide.shapes.add_picture(str(img_path), Inches(px), Inches(py), Inches(pw), Inches(ph))


def draw_header(
    slide,
    lesson_num: int,
    lesson_title: str,
    slide_idx: int,
    slide_tot: int,
    title: str,
    subtitle_html: str = None,
    is_dark: bool = False,
) -> float:
    short_l = lesson_title.split(":")[0].strip()
    if len(short_l) > 48:
        short_l = short_l[:45] + "…"
    pill_txt = f"LEZIONE {lesson_num:02d}  ·  {short_l.upper()}"
    pill_fill = CARD_DARK_BLUE if is_dark else C_BLUE
    pill_fg = C_GOLD_BRIGHT if is_dark else C_LIGHT_TXT
    pill = add_rounded_card(slide, 0.50, 0.24, 5.20, 0.27, pill_fill, radius=0.45)
    tf = pill.text_frame
    tf.word_wrap = False
    tf.margin_left = Inches(0.14)
    tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = pill_txt
    r.font.name = FONT_BODY
    r.font.size = Pt(9.0)
    r.font.bold = True
    r.font.color.rgb = pill_fg

    cnt_fill = CARD_DARK_GREEN if is_dark else TINT_BLUE
    cnt_bord = BORD_DARK_GREEN if is_dark else BORD_BLUE
    cnt_fg = C_LIGHT_TXT if is_dark else C_BLUE_DARK
    cnt = add_rounded_card(slide, 8.65, 0.24, 0.85, 0.27, cnt_fill, cnt_bord, radius=0.45)
    tfc = cnt.text_frame
    tfc.word_wrap = False
    tfc.margin_left = tfc.margin_right = tfc.margin_top = tfc.margin_bottom = 0
    tfc.vertical_anchor = MSO_ANCHOR.MIDDLE
    pc = tfc.paragraphs[0]
    pc.alignment = PP_ALIGN.CENTER
    rc = pc.add_run()
    rc.text = f"{slide_idx:02d} / {slide_tot:02d}"
    rc.font.name = FONT_BODY
    rc.font.size = Pt(9.5)
    rc.font.bold = True
    rc.font.color.rgb = cnt_fg

    title_color = C_LIGHT_TXT if is_dark else C_INK
    t_size = 24.0 if len(title) <= 46 else (21.0 if len(title) <= 62 else 18.5)
    add_text_box(
        slide,
        0.50,
        0.56,
        9.00,
        0.48,
        [(title, True, False)],
        font_size=t_size,
        base_color=title_color,
        bold_color=title_color,
        font_name=FONT_HEAD,
        valign=MSO_ANCHOR.MIDDLE,
    )

    content_y = 1.10
    if subtitle_html:
        segs = clean_html_to_segments(subtitle_html)
        sub_col = C_GOLD_BRIGHT if is_dark else C_GREEN
        add_text_box(
            slide,
            0.50,
            1.04,
            9.00,
            0.30,
            segs,
            font_size=13.5,
            base_color=sub_col,
            bold_color=sub_col,
            font_name=FONT_BODY,
            force_bold=True,
        )
        content_y = 1.38
    return content_y


# ==============================================================================
# 5. COPERTINA, INTRODUZIONE, CHIUSURA E SINTESI (ZERO ICONE FINTE)
# ==============================================================================
def build_cover_slide(slide, lesson_num: int, total_lessons: int, lesson_title: str):
    """Copertina Uninettuno con immagine VERA del motore (ai_copertina.jpg) fotorealistica."""
    set_slide_bg(slide, BG_DARK)

    # Immagine reale/3D ad alta definizione del motore sulla destra (nessun disegno artefatto)
    cover_img = IMG_DIR / "ai_copertina.jpg"
    if cover_img.exists():
        add_rounded_card(slide, 5.05, 0.48, 4.45, 4.65, CARD_DARK_BLUE, BORD_DARK_BLUE, border_pt=1.5, radius=0.04)
        add_picture_contained(slide, cover_img, 5.15, 0.58, 4.25, 4.45)

    # Pill Corso di laurea a sinistra
    left_w = 4.35
    pill = add_rounded_card(slide, 0.50, 0.48, left_w, 0.34, CARD_DARK_BLUE, BORD_DARK_BLUE, radius=0.45)
    tf = pill.text_frame
    tf.margin_left = Inches(0.16)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = SOTTO_CORSO.upper()
    r.font.name = FONT_BODY
    r.font.size = Pt(8.5)
    r.font.bold = True
    r.font.color.rgb = C_GOLD_BRIGHT

    # Titolo insegnamento
    add_text_box(
        slide,
        0.50,
        0.94,
        left_w,
        0.80,
        [(CORSO, True, False)],
        font_size=32.0,
        base_color=C_LIGHT_TXT,
        bold_color=C_LIGHT_TXT,
        font_name=FONT_HEAD,
        valign=MSO_ANCHOR.MIDDLE,
    )

    # Card centrale della Lezione
    add_rounded_card(slide, 0.50, 1.84, left_w, 1.95, CARD_DARK_BLUE, C_GOLD_BRIGHT, border_pt=1.8, radius=0.05)
    badge = add_rounded_card(slide, 0.70, 2.02, 2.05, 0.32, C_GOLD_BRIGHT, radius=0.4)
    tfb = badge.text_frame
    tfb.vertical_anchor = MSO_ANCHOR.MIDDLE
    pb = tfb.paragraphs[0]
    pb.alignment = PP_ALIGN.CENTER
    rb = pb.add_run()
    rb.text = f"LEZIONE {lesson_num} DI {total_lessons}"
    rb.font.name = FONT_BODY
    rb.font.size = Pt(10.5)
    rb.font.bold = True
    rb.font.color.rgb = C_INK

    lt_size = estimate_fitted_fontsize(lesson_title, left_w - 0.40, 1.25, max_pt=18.0, min_pt=13.0)
    add_text_box(
        slide,
        0.70,
        2.42,
        left_w - 0.40,
        1.22,
        [(lesson_title, True, False)],
        font_size=lt_size,
        base_color=C_LIGHT_TXT,
        bold_color=C_LIGHT_TXT,
        font_name=FONT_HEAD,
        valign=MSO_ANCHOR.MIDDLE,
    )

    # Due card in basso: Docente e Università
    bot_w = (left_w - 0.18) / 2.0
    add_rounded_card(slide, 0.50, 3.95, bot_w, 1.18, CARD_DARK_GREEN, BORD_DARK_GREEN, radius=0.06)
    add_text_box(
        slide,
        0.64,
        4.05,
        bot_w - 0.28,
        0.28,
        [("DOCENTE", True, False)],
        font_size=9.0,
        base_color=C_GOLD_BRIGHT,
        bold_color=C_GOLD_BRIGHT,
    )
    add_text_box(
        slide,
        0.64,
        4.35,
        bot_w - 0.28,
        0.68,
        [(DOCENTE, True, False)],
        font_size=13.5,
        base_color=C_LIGHT_TXT,
        bold_color=C_LIGHT_TXT,
        font_name=FONT_HEAD,
    )

    add_rounded_card(slide, 0.50 + bot_w + 0.18, 3.95, bot_w, 1.18, CARD_DARK_BLUE, BORD_DARK_BLUE, radius=0.06)
    add_text_box(
        slide,
        0.50 + bot_w + 0.32,
        4.05,
        bot_w - 0.28,
        0.28,
        [("ATENEO", True, False)],
        font_size=9.0,
        base_color=C_ICE_TXT,
        bold_color=C_ICE_TXT,
    )
    add_text_box(
        slide,
        0.50 + bot_w + 0.32,
        4.35,
        bot_w - 0.28,
        0.68,
        [(UNIV, True, False)],
        font_size=11.5,
        base_color=C_LIGHT_TXT,
        bold_color=C_LIGHT_TXT,
        font_name=FONT_HEAD,
    )


def build_closing_slide(
    slide, lesson_num: int, lesson_title: str, slide_idx: int, slide_tot: int
):
    """Slide finale obbligatoria Uninettuno: Ambiente di apprendimento e Cyberspazio."""
    set_slide_bg(slide, BG_DARK)
    y0 = draw_header(
        slide, lesson_num, lesson_title, slide_idx, slide_tot, "Materiali della lezione", is_dark=True
    )

    # Banner superiore portale Uninettuno
    add_rounded_card(slide, 0.50, y0, 9.00, 1.15, CARD_DARK_GREEN, C_GOLD_BRIGHT, border_pt=1.6, radius=0.05)
    add_circle_badge(slide, 1.10, y0 + 0.57, 0.65, C_GOLD_BRIGHT, "WEB", text_color=C_INK, font_size=11.0)
    add_text_box(
        slide,
        1.60,
        y0 + 0.14,
        7.60,
        0.34,
        [("AMBIENTE DI APPRENDIMENTO UNINETTUNO — CYBERSPAZIO DIDATTICO", True, False)],
        font_size=11.0,
        base_color=C_ICE_TXT,
        bold_color=C_ICE_TXT,
    )
    add_text_box(
        slide,
        1.60,
        y0 + 0.46,
        7.60,
        0.54,
        [(CYBER, True, False)],
        font_size=21.0,
        base_color=C_GOLD_BRIGHT,
        bold_color=C_GOLD_BRIGHT,
        font_name=FONT_HEAD,
    )

    items = [
        ("01", "Pagina del docente-tutor", "Programma dettagliato del corso, mappa concettuale e pianificazione didattica.", C_GOLD_BRIGHT, CARD_DARK_BLUE, BORD_DARK_BLUE),
        ("02", "Guida all'esame", "Criteri di valutazione, modalità di verifica e obiettivi operativi.", C_GREEN, CARD_DARK_BLUE, BORD_DARK_BLUE),
        ("03", "Slide ed esercitazioni", "Presentazioni della videolezione, esercizi svolti e domande di autovalutazione.", C_BLUE, CARD_DARK_GREEN, BORD_DARK_GREEN),
        ("04", "Classi interattive e tutoraggio", "Incontri in aula virtuale, correzione degli esercizi e ricevimento studenti.", C_GOLD_BRIGHT, CARD_DARK_GREEN, BORD_DARK_GREEN),
    ]
    gy = y0 + 1.32
    cw, ch = 4.38, 1.34
    for idx, (num, head, desc, badge_col, cfill, cbord) in enumerate(items):
        r, c = divmod(idx, 2)
        cx = 0.50 + c * (cw + 0.24)
        cy = gy + r * (ch + 0.20)
        add_rounded_card(slide, cx, cy, cw, ch, cfill, cbord, radius=0.06)
        fg_b = C_INK if badge_col == C_GOLD_BRIGHT else C_LIGHT_TXT
        add_circle_badge(slide, cx + 0.44, cy + ch / 2, 0.50, badge_col, num, text_color=fg_b, font_size=13.0)
        add_text_box(
            slide,
            cx + 0.82,
            cy + 0.16,
            cw - 0.96,
            0.36,
            [(head, True, False)],
            font_size=14.5,
            base_color=C_GOLD_BRIGHT if badge_col == C_GOLD_BRIGHT else C_LIGHT_TXT,
            font_name=FONT_HEAD,
        )
        add_text_box(
            slide,
            cx + 0.82,
            cy + 0.54,
            cw - 0.96,
            0.68,
            [(desc, False, False)],
            font_size=12.0,
            base_color=C_ICE_TXT,
            valign=MSO_ANCHOR.TOP,
        )


def build_intro_slide(
    slide,
    lesson_num: int,
    lesson_title: str,
    slide_idx: int,
    slide_tot: int,
    title: str,
    body: dict,
    kind: str,
):
    """Layout tipografico puro per le slide introduttive (Obiettivi, Domande, Prerequisiti, Indice)."""
    set_slide_bg(slide, BG_LIGHT)
    y0 = draw_header(slide, lesson_num, lesson_title, slide_idx, slide_tot, title, body["h3"], is_dark=False)
    avail_h = 5.34 - y0

    # 1. DOMANDE DI INNESCO: 3 Grandi card orizzontali ad alto impatto visivo
    if kind == "domande":
        items = body["lists"][0][1] if body["lists"] else []
        n_it = len(items)
        gap = 0.18
        ch = (avail_h - gap * max(0, n_it - 1)) / max(1, n_it)
        for idx, it_html in enumerate(items):
            cy = y0 + idx * (ch + gap)
            acc_c, tint_c, bord_c = ACCENT_CYCLE[idx % len(ACCENT_CYCLE)]
            add_rounded_card(slide, 0.50, cy, 9.00, ch, CARD_BASE, bord_c, border_pt=1.5, radius=0.05)
            # Badge numerico grande a sinistra
            add_circle_badge(slide, 1.05, cy + ch / 2, 0.62, acc_c, f"0{idx+1}", text_color=C_LIGHT_TXT, font_size=16.0)
            segs = clean_html_to_segments(it_html)
            pt = estimate_fitted_fontsize(plain_text_of(it_html), 7.20, ch - 0.20, max_pt=18.0, min_pt=13.5)
            add_text_box(
                slide,
                1.55,
                cy + 0.10,
                7.70,
                ch - 0.20,
                segs,
                font_size=pt,
                base_color=C_INK,
                bold_color=acc_c,
                font_name=FONT_HEAD,
                force_bold=True,
            )
        return

    # 2. PREREQUISITI: Colonne pilastro pulite (2 o 3 pilastri)
    if kind == "prerequisiti":
        items = body["lists"][0][1] if body["lists"] else []
        n_it = len(items)
        cw = (9.00 - 0.24 * (n_it - 1)) / max(1, n_it)
        for idx, it_html in enumerate(items):
            cx = 0.50 + idx * (cw + 0.24)
            acc_c, tint_c, bord_c = ACCENT_CYCLE[idx % len(ACCENT_CYCLE)]
            add_rounded_card(slide, cx, y0, cw, avail_h, CARD_BASE, bord_c, border_pt=1.5, radius=0.05)
            # Testata del pilastro
            top_b = add_rounded_card(slide, cx + 0.14, y0 + 0.14, cw - 0.28, 0.78, tint_c, bord_c, radius=0.05)
            add_circle_badge(slide, cx + 0.54, y0 + 0.53, 0.48, acc_c, f"0{idx+1}", font_size=13.0)
            add_text_box(
                slide,
                cx + 0.88,
                y0 + 0.28,
                cw - 1.05,
                0.50,
                [(f"PREREQUISITO {idx+1}", True, False)],
                font_size=11.5,
                base_color=acc_c,
                bold_color=acc_c,
            )
            segs = clean_html_to_segments(it_html)
            pt = estimate_fitted_fontsize(plain_text_of(it_html), cw - 0.44, avail_h - 1.25, max_pt=16.0, min_pt=13.0)
            add_text_box(
                slide,
                cx + 0.22,
                y0 + 1.10,
                cw - 0.44,
                avail_h - 1.25,
                segs,
                font_size=pt,
                base_color=C_INK,
                bold_color=acc_c,
                math_color=C_GREEN_DARK,
                valign=MSO_ANCHOR.MIDDLE,
            )
        return

    # 3. OBIETTIVI e METODI: Hero card di contesto a sinistra + card numerate a destra
    items = body["lists"][0][1] if body["lists"] else []
    n_it = len(items)
    left_w = 2.70
    add_rounded_card(slide, 0.50, y0, left_w, avail_h, CARD_DARK_BLUE, BORD_DARK_BLUE, radius=0.05)
    # Badge testuale
    pill = add_rounded_card(slide, 0.70, y0 + 0.32, left_w - 0.40, 0.36, C_GOLD_BRIGHT, radius=0.4)
    tfp = pill.text_frame
    tfp.vertical_anchor = MSO_ANCHOR.MIDDLE
    pp = tfp.paragraphs[0]
    pp.alignment = PP_ALIGN.CENTER
    rp = pp.add_run()
    rp.text = "COMPETENZE CHIAVE" if kind == "obiettivi" else "METODO DI STUDIO"
    rp.font.name = FONT_BODY
    rp.font.size = Pt(10.0)
    rp.font.bold = True
    rp.font.color.rgb = C_INK

    lbl = "OBIETTIVI DELLA LEZIONE" if kind == "obiettivi" else "QUADRO METODOLOGICO"
    add_text_box(
        slide,
        0.66,
        y0 + 0.88,
        left_w - 0.32,
        0.80,
        [(lbl, True, False)],
        font_size=15.0,
        base_color=C_LIGHT_TXT,
        bold_color=C_LIGHT_TXT,
        font_name=FONT_HEAD,
        align=PP_ALIGN.CENTER,
    )
    sub_lbl = (
        f"{n_it} obiettivi specifici da padroneggiare per interpretare il funzionamento del motore."
        if kind == "obiettivi"
        else "Indicazioni operative per affrontare i contenuti teorici e gli esempi numerici."
    )
    add_text_box(
        slide,
        0.66,
        y0 + 1.80,
        left_w - 0.32,
        2.10,
        [(sub_lbl, False, False)],
        font_size=12.5,
        base_color=C_ICE_TXT,
        align=PP_ALIGN.CENTER,
    )

    rx = 0.50 + left_w + 0.22
    rw = 9.50 - rx
    gap = 0.12
    ch = (avail_h - gap * max(0, n_it - 1)) / max(1, n_it)
    for idx, it_html in enumerate(items):
        cy = y0 + idx * (ch + gap)
        acc_c, tint_c, bord_c = ACCENT_CYCLE[idx % len(ACCENT_CYCLE)]
        add_rounded_card(slide, rx, cy, rw, ch, CARD_BASE, bord_c, border_pt=1.3, radius=0.06)
        add_circle_badge(slide, rx + 0.40, cy + ch / 2, 0.46, acc_c, f"{idx+1:02d}", font_size=12.0)
        segs = clean_html_to_segments(it_html)
        pt = estimate_fitted_fontsize(plain_text_of(it_html), rw - 0.90, ch - 0.12, max_pt=14.5, min_pt=11.5)
        add_text_box(
            slide,
            rx + 0.76,
            cy + 0.06,
            rw - 0.90,
            ch - 0.12,
            segs,
            font_size=pt,
            base_color=C_INK,
            bold_color=acc_c,
            math_color=C_GREEN_DARK,
        )


def build_sintesi_slide(
    slide, lesson_num: int, lesson_title: str, slide_idx: int, slide_tot: int, title: str, body: dict
):
    set_slide_bg(slide, BG_DARK)
    y0 = draw_header(slide, lesson_num, lesson_title, slide_idx, slide_tot, title, is_dark=True)

    takeaway_html = body["paras"][0] if body["paras"] else ""
    kw_raw = ""
    for p_html in body["paras"][1:]:
        pt = plain_text_of(p_html)
        if ":" in pt:
            kw_raw = pt.split(":", 1)[1].strip()
        else:
            kw_raw = pt

    # 1. Card Concetto Chiave
    add_rounded_card(slide, 0.50, y0, 9.00, 0.95, CARD_DARK_BLUE, C_GOLD_BRIGHT, border_pt=1.5, radius=0.05)
    pill = add_rounded_card(slide, 0.68, y0 + 0.28, 1.75, 0.38, C_GOLD_BRIGHT, radius=0.4)
    tfp = pill.text_frame
    tfp.vertical_anchor = MSO_ANCHOR.MIDDLE
    pp = tfp.paragraphs[0]
    pp.alignment = PP_ALIGN.CENTER
    rp = pp.add_run()
    rp.text = "PUNTO CHIAVE"
    rp.font.name = FONT_BODY
    rp.font.size = Pt(10.0)
    rp.font.bold = True
    rp.font.color.rgb = C_INK

    segs_tk = clean_html_to_segments(takeaway_html) if takeaway_html else [(title, True, False)]
    tk_pt = estimate_fitted_fontsize(plain_text_of(takeaway_html), 6.75, 0.78, max_pt=16.5, min_pt=12.5)
    add_text_box(
        slide,
        2.58,
        y0 + 0.08,
        6.74,
        0.78,
        segs_tk,
        font_size=tk_pt,
        base_color=C_LIGHT_TXT,
        bold_color=C_GOLD_BRIGHT,
        math_color=C_GOLD_BRIGHT,
        force_bold=True,
    )

    # 2. Fascia Termini Chiave
    ky = y0 + 1.10
    add_text_box(
        slide,
        0.50,
        ky,
        1.85,
        0.44,
        [("TERMINI CHIAVE:", True, False)],
        font_size=11.0,
        base_color=C_GOLD_BRIGHT,
        bold_color=C_GOLD_BRIGHT,
    )
    terms = [t.strip() for t in kw_raw.split(",") if t.strip()]
    if terms:
        tx = 2.45
        for t_idx, t in enumerate(terms):
            tw = min(2.15, max(1.10, 0.12 * len(t) + 0.35))
            if tx + tw > 9.50:
                break
            bg_c, bord_c = (CARD_DARK_GREEN, BORD_DARK_GREEN) if t_idx % 2 == 0 else (CARD_DARK_BLUE, BORD_DARK_BLUE)
            add_rounded_card(slide, tx, ky + 0.04, tw, 0.36, bg_c, bord_c, radius=0.45)
            add_text_box(
                slide,
                tx + 0.08,
                ky + 0.04,
                tw - 0.16,
                0.36,
                [(t, True, False)],
                font_size=10.0,
                base_color=C_LIGHT_TXT,
                bold_color=C_LIGHT_TXT,
                align=PP_ALIGN.CENTER,
            )
            tx += tw + 0.14

    # 3. Tre Domande di Autovalutazione
    qy = ky + 0.60
    q_items = body["lists"][0][1] if body["lists"] else []
    n_q = len(q_items)
    gap_q = 0.14
    qh = (5.30 - qy - gap_q * max(0, n_q - 1)) / max(1, n_q)
    for idx, q_html in enumerate(q_items):
        cy = qy + idx * (qh + gap_q)
        badge_c, c_fill, c_bord = DARK_CYCLE[idx % len(DARK_CYCLE)]
        add_rounded_card(slide, 0.50, cy, 9.00, qh, c_fill, c_bord, border_pt=1.3, radius=0.06)
        fg_b = C_INK if badge_c == C_GOLD_BRIGHT else C_LIGHT_TXT
        add_circle_badge(slide, 0.95, cy + qh / 2, 0.48, badge_c, f"0{idx+1}", text_color=fg_b, font_size=12.5)
        segs = clean_html_to_segments(q_html)
        pt = estimate_fitted_fontsize(plain_text_of(q_html), 8.10, qh - 0.14, max_pt=14.5, min_pt=11.5)
        add_text_box(
            slide,
            1.35,
            cy + 0.06,
            7.95,
            qh - 0.12,
            segs,
            font_size=pt,
            base_color=C_LIGHT_TXT,
            bold_color=badge_c,
            math_color=badge_c,
        )


def build_recap_slide(
    slide, lesson_num: int, lesson_title: str, slide_idx: int, slide_tot: int, title: str, body: dict
):
    set_slide_bg(slide, BG_DARK)
    y0 = draw_header(slide, lesson_num, lesson_title, slide_idx, slide_tot, title, is_dark=True)
    avail_h = 5.34 - y0

    nota_text = plain_text_of(body["notas"][0]) if body["notas"] else ""
    items = body["lists"][0][1] if body["lists"] else []
    n_it = len(items)

    book_h = 0.95 if nota_text else 0.0
    list_h = avail_h - (book_h + 0.18 if book_h else 0.0)

    gap = 0.12
    ch = (list_h - gap * max(0, n_it - 1)) / max(1, n_it)
    for idx, it_html in enumerate(items):
        cy = y0 + idx * (ch + gap)
        badge_c, c_fill, c_bord = DARK_CYCLE[idx % len(DARK_CYCLE)]
        add_rounded_card(slide, 0.50, cy, 9.00, ch, c_fill, c_bord, border_pt=1.3, radius=0.06)
        fg_b = C_INK if badge_c == C_GOLD_BRIGHT else C_LIGHT_TXT
        add_circle_badge(slide, 0.95, cy + ch / 2, 0.48, badge_c, f"0{idx+1}", text_color=fg_b, font_size=12.5)
        segs = clean_html_to_segments(it_html)
        pt = estimate_fitted_fontsize(plain_text_of(it_html), 8.10, ch - 0.12, max_pt=15.0, min_pt=12.0)
        add_text_box(
            slide,
            1.35,
            cy + 0.06,
            7.95,
            ch - 0.12,
            segs,
            font_size=pt,
            base_color=C_LIGHT_TXT,
            bold_color=badge_c,
            math_color=badge_c,
        )

    if nota_text:
        by = y0 + list_h + 0.16
        add_rounded_card(slide, 0.50, by, 9.00, book_h, CARD_DARK_GOLD, BORD_DARK_GOLD, border_pt=1.5, radius=0.06)
        pill = add_rounded_card(slide, 0.70, by + 0.28, 1.95, 0.38, C_GOLD_BRIGHT, radius=0.4)
        tfp = pill.text_frame
        tfp.vertical_anchor = MSO_ANCHOR.MIDDLE
        pp = tfp.paragraphs[0]
        pp.alignment = PP_ALIGN.CENTER
        rp = pp.add_run()
        rp.text = "TESTO DI RIFERIMENTO"
        rp.font.name = FONT_BODY
        rp.font.size = Pt(9.5)
        rp.font.bold = True
        rp.font.color.rgb = C_INK

        segs_b = clean_html_to_segments(body["notas"][0])
        b_pt = estimate_fitted_fontsize(nota_text, 6.45, book_h - 0.16, max_pt=13.0, min_pt=10.5)
        add_text_box(
            slide,
            2.85,
            by + 0.08,
            6.45,
            book_h - 0.16,
            segs_b,
            font_size=b_pt,
            base_color=C_LIGHT_TXT,
            bold_color=C_GOLD_BRIGHT,
            math_color=C_GOLD_BRIGHT,
        )


# ==============================================================================
# 6. TABELLE, FORMULE, LISTE E FIGURE PROTAGONISTE
# ==============================================================================
def draw_styled_table(slide, rows: list, x: float, y: float, w: float, h: float):
    n_rows = len(rows)
    n_cols = max(len(r) for r in rows)
    col_weights = [1.0] * n_cols
    for c in range(n_cols):
        max_len = max((len(plain_text_of(r[c][0])) for r in rows if c < len(r)), default=8)
        col_weights[c] = max(6.0, min(42.0, float(max_len) ** 0.75))
    sum_w = sum(col_weights)
    col_widths = [w * (cw / sum_w) for cw in col_weights]

    avg_row_h = h / max(1, n_rows)
    if n_rows >= 8 or avg_row_h < 0.34:
        f_pt = 10.5
    elif n_rows >= 6 or avg_row_h < 0.44:
        f_pt = 11.5
    else:
        f_pt = 12.5

    tbl_shape = slide.shapes.add_table(n_rows, n_cols, Inches(x), Inches(y), Inches(w), Inches(h))
    tbl = tbl_shape.table
    for c, cw in enumerate(col_widths):
        tbl.columns[c].width = Inches(cw)
    row_h_in = h / max(1, n_rows)
    for r_idx in range(n_rows):
        tbl.rows[r_idx].height = Inches(row_h_in)

    for r_idx, row in enumerate(rows):
        for c_idx, (cell_html, is_h, is_n) in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = Inches(0.12)
            cell.margin_right = Inches(0.12)
            cell.margin_top = Inches(0.04)
            cell.margin_bottom = Inches(0.04)
            cell.fill.solid()
            if is_h or r_idx == 0:
                cell.fill.fore_color.rgb = BG_DARK
                fg = C_GOLD_BRIGHT if c_idx == 0 else C_LIGHT_TXT
                b_col = C_GOLD_BRIGHT
            else:
                if r_idx % 2 == 1:
                    cell.fill.fore_color.rgb = CARD_BASE
                else:
                    cell.fill.fore_color.rgb = TINT_BLUE
                fg = C_BLUE_DARK if c_idx == 0 else C_INK
                b_col = C_GREEN_DARK if c_idx > 0 else C_BLUE_DARK

            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.RIGHT if is_n else PP_ALIGN.LEFT
            segs = clean_html_to_segments(cell_html)
            fill_paragraph_segments(
                p,
                segs,
                font_size=f_pt,
                base_color=fg,
                bold_color=b_col,
                math_color=C_GOLD if (not is_h and r_idx > 0) else C_GOLD_BRIGHT,
                force_bold=bool(is_h or r_idx == 0 or c_idx == 0),
            )


def draw_equation_card(
    slide, eq_tex: str, eq_map: dict, x: float, y: float, w: float, h: float
):
    add_rounded_card(slide, x, y, w, h, TINT_GOLD, BORD_GOLD, border_pt=1.5, radius=0.06)
    if w >= 4.2 and h >= 0.75:
        b = add_rounded_card(slide, x + 0.14, y + 0.12, 1.15, 0.26, C_BLUE_DARK, radius=0.4)
        tf = b.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = "RELAZIONE"
        r.font.name = FONT_BODY
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = C_GOLD_BRIGHT
        img_x = x + 1.35
        img_w = w - 1.50
    else:
        img_x = x + 0.14
        img_w = w - 0.28

    eq_png = eq_map.get(eq_tex)
    if eq_png and eq_png.exists():
        add_picture_contained(slide, eq_png, img_x, y + 0.08, img_w, h - 0.16)
    else:
        # Fallback con espressione formattata OpenXML
        clean_s = inline_math_to_text(eq_tex)
        segs = clean_html_to_segments(f"<m>{clean_s}</m>")
        pt = estimate_fitted_fontsize(clean_s, img_w, h - 0.16, max_pt=20.0, min_pt=13.0)
        add_text_box(
            slide,
            img_x,
            y + 0.08,
            img_w,
            h - 0.16,
            segs,
            font_size=pt,
            base_color=C_BLUE_DARK,
            bold_color=C_BLUE_DARK,
            font_name=FONT_HEAD,
            align=PP_ALIGN.CENTER,
            force_bold=True,
        )


def draw_list_cards(
    slide,
    items_html: list[str],
    x: float,
    y: float,
    w: float,
    h: float,
    use_two_cols: bool = False,
):
    n = len(items_html)
    if n == 0:
        return
    if use_two_cols and n >= 4 and w >= 6.5:
        cols = 2
        rows = math.ceil(n / 2)
        gap_x, gap_y = 0.20, 0.14
        cw = (w - gap_x) / 2.0
        ch = (h - gap_y * (rows - 1)) / rows
        for idx, it_html in enumerate(items_html):
            r, c = divmod(idx, 2)
            cx = x + c * (cw + gap_x)
            cy = y + r * (ch + gap_y)
            acc_c, tint_c, bord_c = ACCENT_CYCLE[idx % len(ACCENT_CYCLE)]
            add_rounded_card(slide, cx, cy, cw, ch, CARD_BASE, bord_c, border_pt=1.3, radius=0.06)
            d = min(0.40, ch * 0.65)
            add_circle_badge(slide, cx + 0.32, cy + ch / 2, d, acc_c, f"{idx+1:02d}", font_size=10.5)
            segs = clean_html_to_segments(it_html)
            pt = estimate_fitted_fontsize(plain_text_of(it_html), cw - 0.72, ch - 0.10, max_pt=13.5, min_pt=10.0)
            add_text_box(
                slide,
                cx + 0.60,
                cy + 0.05,
                cw - 0.70,
                ch - 0.10,
                segs,
                font_size=pt,
                base_color=C_INK,
                bold_color=acc_c,
                math_color=C_GREEN_DARK,
            )
    else:
        gap_y = 0.12 if n <= 4 else 0.08
        ch = (h - gap_y * (n - 1)) / n
        for idx, it_html in enumerate(items_html):
            cy = y + idx * (ch + gap_y)
            acc_c, tint_c, bord_c = ACCENT_CYCLE[idx % len(ACCENT_CYCLE)]
            add_rounded_card(slide, x, cy, w, ch, CARD_BASE, bord_c, border_pt=1.3, radius=0.06)
            d = min(0.42, max(0.28, ch * 0.68))
            add_circle_badge(slide, x + 0.36, cy + ch / 2, d, acc_c, f"{idx+1:02d}", font_size=11.0)
            segs = clean_html_to_segments(it_html)
            pt = estimate_fitted_fontsize(plain_text_of(it_html), w - 0.80, ch - 0.08, max_pt=14.5, min_pt=10.5)
            add_text_box(
                slide,
                x + 0.68,
                cy + 0.04,
                w - 0.80,
                ch - 0.08,
                segs,
                font_size=pt,
                base_color=C_INK,
                bold_color=acc_c,
                math_color=C_GREEN_DARK,
            )


def draw_content_stack(
    slide,
    body: dict,
    eq_map: dict,
    x: float,
    y: float,
    w: float,
    h: float,
    allow_two_col_list: bool = False,
):
    blocks = []
    for c_html in body["cits"]:
        blocks.append(("cit", c_html, 0.55))
    for eq in body["mathblocks"]:
        blocks.append(("math", eq, 0.88))
    for tbl in body["tables"]:
        weight = max(1.40, min(3.00, 0.36 * len(tbl)))
        blocks.append(("table", tbl, weight))
    for _, items in body["lists"]:
        weight = max(1.20, min(2.80, 0.44 * len(items)))
        blocks.append(("list", items, weight))
    for p_html in body["paras"]:
        blocks.append(("para", p_html, 0.55))
    for n_html in body["notas"]:
        blocks.append(("nota", n_html, 0.48))

    if not blocks:
        return

    n_b = len(blocks)
    gap = 0.14 if n_b > 1 else 0.0
    avail_h = h - gap * (n_b - 1)
    tot_w = sum(b[2] for b in blocks)
    cur_y = y

    for b_kind, payload, bw in blocks:
        bh = avail_h * (bw / tot_w)
        if b_kind == "cit":
            add_rounded_card(slide, x, cur_y, w, bh, BG_DARK, C_GOLD_BRIGHT, border_pt=1.5, radius=0.06)
            segs = clean_html_to_segments(payload)
            pt = estimate_fitted_fontsize(plain_text_of(payload), w - 0.32, bh - 0.10, max_pt=16.0, min_pt=12.0)
            add_text_box(
                slide,
                x + 0.16,
                cur_y + 0.05,
                w - 0.32,
                bh - 0.10,
                segs,
                font_size=pt,
                base_color=C_GOLD_BRIGHT,
                bold_color=C_LIGHT_TXT,
                math_color=C_GOLD_BRIGHT,
                align=PP_ALIGN.CENTER,
                force_bold=True,
            )
        elif b_kind == "math":
            draw_equation_card(slide, payload, eq_map, x, cur_y, w, bh)
        elif b_kind == "table":
            draw_styled_table(slide, payload, x, cur_y, w, bh)
        elif b_kind == "list":
            draw_list_cards(slide, payload, x, cur_y, w, bh, use_two_cols=allow_two_col_list)
        elif b_kind in ("para", "nota"):
            c_fill = TINT_GOLD if b_kind == "nota" else CARD_BASE
            c_bord = BORD_GOLD if b_kind == "nota" else BORD_GREEN
            add_rounded_card(slide, x, cur_y, w, bh, c_fill, c_bord, radius=0.06)
            segs = clean_html_to_segments(payload)
            pt = estimate_fitted_fontsize(plain_text_of(payload), w - 0.32, bh - 0.10, max_pt=13.0, min_pt=10.5)
            add_text_box(
                slide,
                x + 0.16,
                cur_y + 0.05,
                w - 0.32,
                bh - 0.10,
                segs,
                font_size=pt,
                base_color=C_INK,
                bold_color=C_BLUE_DARK,
                math_color=C_GREEN_DARK,
            )
        cur_y += bh + gap


def build_technical_slide(
    slide,
    lesson_num: int,
    lesson_title: str,
    slide_idx: int,
    slide_tot: int,
    title: str,
    body: dict,
    eq_map: dict,
):
    """Costruisce una slide tecnica garantendo figure MAESTOSE e PROTAGONISTE."""
    set_slide_bg(slide, BG_LIGHT)
    y0 = draw_header(slide, lesson_num, lesson_title, slide_idx, slide_tot, title, body["h3"], is_dark=False)
    avail_h = 5.34 - y0
    figs = body["figures"]
    has_other = has_non_fig_content(body)

    # --------------------------------------------------------------------------
    # CASO A: SLIDE DEDICATA A 1 FIGURA (PROTAGONISTA ASSOLUTA)
    # --------------------------------------------------------------------------
    if len(figs) == 1 and not has_other:
        kind, name, cap_html = figs[0]
        img_path = resolve_img(kind, name)
        cap_txt = plain_text_of(cap_html) if cap_html else ""

        if cap_txt:
            cap_h = 0.65
            fh = avail_h - cap_h - 0.12
            # Grande card immagine a tutta larghezza
            add_rounded_card(slide, 0.50, y0, 9.00, fh, CARD_BASE, BORD_BASE, radius=0.04)
            add_picture_contained(slide, img_path, 0.60, y0 + 0.08, 8.80, fh - 0.16)
            # Card didascalia orizzontale in basso a tutta larghezza
            cy = y0 + fh + 0.12
            add_rounded_card(slide, 0.50, cy, 9.00, cap_h, TINT_BLUE, BORD_BLUE, radius=0.05)
            add_circle_badge(slide, 0.92, cy + cap_h / 2, 0.44, C_BLUE, "FIG", text_color=C_LIGHT_TXT, font_size=10.0)
            segs = clean_html_to_segments(cap_html)
            c_pt = estimate_fitted_fontsize(cap_txt, 7.95, cap_h - 0.12, max_pt=12.5, min_pt=9.5)
            add_text_box(
                slide,
                1.28,
                cy + 0.06,
                8.05,
                cap_h - 0.12,
                segs,
                font_size=c_pt,
                base_color=C_BLUE_DARK,
                bold_color=C_BLUE_DARK,
                math_color=C_GREEN_DARK,
            )
        else:
            # Immagine a TUTTO SCHERMO sotto l'intestazione (senza didascalia)
            add_rounded_card(slide, 0.50, y0, 9.00, avail_h, CARD_BASE, BORD_BASE, radius=0.04)
            add_picture_contained(slide, img_path, 0.60, y0 + 0.10, 8.80, avail_h - 0.20)
        return

    # --------------------------------------------------------------------------
    # CASO B: SLIDE DEDICATA A 2 o 3 FIGURE AFFIANCATE (PROTAGONISTE)
    # --------------------------------------------------------------------------
    if len(figs) >= 2 and not has_other:
        n_f = len(figs)
        gap_x = 0.20
        fw = (9.00 - gap_x * (n_f - 1)) / n_f
        for idx, (kind, name, cap_html) in enumerate(figs):
            fx = 0.50 + idx * (fw + gap_x)
            img_path = resolve_img(kind, name)
            cap_txt = plain_text_of(cap_html) if cap_html else ""
            if cap_txt:
                cap_h = 0.65
                fh = avail_h - cap_h - 0.10
                add_rounded_card(slide, fx, y0, fw, fh, CARD_BASE, BORD_BASE, radius=0.04)
                add_picture_contained(slide, img_path, fx + 0.08, y0 + 0.08, fw - 0.16, fh - 0.16)
                cy = y0 + fh + 0.10
                add_rounded_card(slide, fx, cy, fw, cap_h, TINT_BLUE, BORD_BLUE, radius=0.05)
                segs = clean_html_to_segments(cap_html)
                c_pt = estimate_fitted_fontsize(cap_txt, fw - 0.24, cap_h - 0.10, max_pt=11.0, min_pt=8.5)
                add_text_box(
                    slide,
                    fx + 0.12,
                    cy + 0.05,
                    fw - 0.24,
                    cap_h - 0.10,
                    segs,
                    font_size=c_pt,
                    base_color=C_BLUE_DARK,
                    align=PP_ALIGN.CENTER,
                )
            else:
                add_rounded_card(slide, fx, y0, fw, avail_h, CARD_BASE, BORD_BASE, radius=0.04)
                add_picture_contained(slide, img_path, fx + 0.08, y0 + 0.10, fw - 0.16, avail_h - 0.20)
        return

    # --------------------------------------------------------------------------
    # CASO C: SLIDE DI TEORIA / FORMULE / TABELLE (SENZA FIGURE)
    # --------------------------------------------------------------------------
    if not figs:
        draw_content_stack(slide, body, eq_map, 0.50, y0, 9.00, avail_h, allow_two_col_list=True)
        return

    # --------------------------------------------------------------------------
    # FALLBACK (se presente sia figura che testo e non già sdoppiata)
    # --------------------------------------------------------------------------
    kind, name, cap_html = figs[0]
    fw = 4.40
    cw = 9.00 - fw - 0.20
    fx, cx = 0.50 + cw + 0.20, 0.50
    img_path = resolve_img(kind, name)
    add_rounded_card(slide, fx, y0, fw, avail_h, CARD_BASE, BORD_BASE, radius=0.04)
    add_picture_contained(slide, img_path, fx + 0.10, y0 + 0.10, fw - 0.20, avail_h - 0.20)
    draw_content_stack(slide, body, eq_map, cx, y0, cw, avail_h, allow_two_col_list=False)


# ==============================================================================
# 7. COSTRUZIONE COMPLETA LEZIONI E DECK MASTER PPTX
# ==============================================================================
def build_lesson_presentation(lesson_data: dict, eq_map: dict) -> Presentation:
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)
    blank_layout = prs.slide_layouts[6]

    l_num = lesson_data["num"]
    l_tot = lesson_data["total"]
    l_title = lesson_data["title"]
    slides = lesson_data["slides"]
    s_tot = len(slides)

    for s_idx, s in enumerate(slides, start=1):
        slide = prs.slides.add_slide(blank_layout)
        s_type = s["type"]
        s_title = s["title"]
        s_body = s["body"]
        s_notes = s["notes"]

        if s_type == "cover":
            build_cover_slide(slide, l_num, l_tot, l_title)
        elif s_type == "closing":
            build_closing_slide(slide, l_num, l_title, s_idx, s_tot)
        else:
            t_lower = s_title.lower()
            if "sintesi" in t_lower:
                build_sintesi_slide(slide, l_num, l_title, s_idx, s_tot, s_title, s_body)
            elif "ricapitolazione" in t_lower:
                build_recap_slide(slide, l_num, l_title, s_idx, s_tot, s_title, s_body)
            elif any(w in t_lower for w in ("obiettivo", "obiettivi")):
                build_intro_slide(slide, l_num, l_title, s_idx, s_tot, s_title, s_body, "obiettivi")
            elif any(w in t_lower for w in ("perché studiare", "perche studiare", "domande")):
                build_intro_slide(slide, l_num, l_title, s_idx, s_tot, s_title, s_body, "domande")
            elif any(w in t_lower for w in ("che cosa serve", "prerequisiti", "serve")):
                build_intro_slide(slide, l_num, l_title, s_idx, s_tot, s_title, s_body, "prerequisiti")
            elif any(w in t_lower for w in ("come seguire", "come studiare")):
                build_intro_slide(slide, l_num, l_title, s_idx, s_tot, s_title, s_body, "metodi")
            else:
                build_technical_slide(slide, l_num, l_title, s_idx, s_tot, s_title, s_body, eq_map)

        if s_notes:
            slide.notes_slide.notes_text_frame.text = s_notes

    return prs


def copy_slide_elements(src_slide, dst_slide):
    for shape in src_slide.shapes:
        dst_slide.shapes._spTree.append(shape._element)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    all_lesson_files = sorted(SRC.glob("a[0-1][0-9].html"))
    total_lessons = len(all_lesson_files)

    target_lesson = None
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg.isdigit():
            target_lesson = int(arg)
        elif arg.startswith("a") and arg[1:].isdigit():
            target_lesson = int(arg[1:])

    if target_lesson is not None:
        lesson_files = [f for f in all_lesson_files if f.name == f"a{target_lesson:02d}.html"]
        print(f"Modalita singola lezione: {lesson_files[0].name if lesson_files else 'Non trovata'}")
    else:
        lesson_files = all_lesson_files
        print(f"Trovate {total_lessons} lezioni in {SRC}")

    print("Passo 1: Parsing dei file sorgente HTML e sdoppiamento intelligente...")
    parsed_lessons = []
    all_eqs = []
    for f in lesson_files:
        idx = int(re.search(r"a(\d+)", f.stem).group(1))
        data = parse_lesson_file(f, idx, total_lessons)
        parsed_lessons.append(data)
        for s in data["slides"]:
            for eq in s["body"].get("mathblocks", []):
                all_eqs.append(eq)

    print(f"Passo 2: Pre-compilazione LaTeX di {len(all_eqs)} formule matematiche a 600 DPI...")
    eq_map = precompile_latex_formulas(all_eqs)
    print(f"Formule pronte in cache: {len(eq_map)}")

    print(f"Passo 3: Generazione di {len(parsed_lessons)} presentazioni PowerPoint...")
    prs_list = []
    for l_data in parsed_lessons:
        num = l_data["num"]
        out_file = OUT_DIR / f"MTG_Lezione_{num:02d}.pptx"
        prs = build_lesson_presentation(l_data, eq_map)
        prs.save(str(out_file))
        prs_list.append((l_data, prs))
        print(f"  [OK] Lezione {num:02d} generata: {out_file.name} ({len(l_data['slides'])} slide)")

    if target_lesson is not None:
        print(f"Singola lezione {target_lesson:02d} completata.")
        return

    print("Passo 4: Generazione del deck unico master (MTG_Slide.pptx)...")
    master_prs = Presentation()
    master_prs.slide_width = Inches(SLIDE_W)
    master_prs.slide_height = Inches(SLIDE_H)
    blank_layout = master_prs.slide_layouts[6]

    total_master_slides = sum(len(d["slides"]) for d in parsed_lessons)
    current_master_idx = 1

    for l_data in parsed_lessons:
        l_num = l_data["num"]
        l_tot = l_data["total"]
        l_title = l_data["title"]
        for s in l_data["slides"]:
            slide = master_prs.slides.add_slide(blank_layout)
            s_type = s["type"]
            s_title = s["title"]
            s_body = s["body"]
            s_notes = s["notes"]

            if s_type == "cover":
                build_cover_slide(slide, l_num, l_tot, l_title)
            elif s_type == "closing":
                build_closing_slide(slide, l_num, l_title, current_master_idx, total_master_slides)
            else:
                t_lower = s_title.lower()
                if "sintesi" in t_lower:
                    build_sintesi_slide(slide, l_num, l_title, current_master_idx, total_master_slides, s_title, s_body)
                elif "ricapitolazione" in t_lower:
                    build_recap_slide(slide, l_num, l_title, current_master_idx, total_master_slides, s_title, s_body)
                elif any(w in t_lower for w in ("obiettivo", "obiettivi")):
                    build_intro_slide(slide, l_num, l_title, current_master_idx, total_master_slides, s_title, s_body, "obiettivi")
                elif any(w in t_lower for w in ("perché studiare", "perche studiare", "domande")):
                    build_intro_slide(slide, l_num, l_title, current_master_idx, total_master_slides, s_title, s_body, "domande")
                elif any(w in t_lower for w in ("che cosa serve", "prerequisiti", "serve")):
                    build_intro_slide(slide, l_num, l_title, current_master_idx, total_master_slides, s_title, s_body, "prerequisiti")
                elif any(w in t_lower for w in ("come seguire", "come studiare")):
                    build_intro_slide(slide, l_num, l_title, current_master_idx, total_master_slides, s_title, s_body, "metodi")
                else:
                    build_technical_slide(slide, l_num, l_title, current_master_idx, total_master_slides, s_title, s_body, eq_map)

            if s_notes:
                slide.notes_slide.notes_text_frame.text = s_notes
            current_master_idx += 1

    master_path = ROOT / "MTG_Slide.pptx"
    master_prs.save(str(master_path))
    print(f"  [OK] Deck master completo generato: {master_path} ({total_master_slides} slide)")
    print("TUTTE LE PRESENTAZIONI PPTX SONO PRONTE CON IMMAGINI PROTAGONISTE!")


if __name__ == "__main__":
    main()
