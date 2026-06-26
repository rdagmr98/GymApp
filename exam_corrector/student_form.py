#!/usr/bin/env python3
"""
ExamCorrector - Modulo Risposta Studente

Legge exam_info.json dalla stessa cartella e mostra il modulo di risposta.
Salva le risposte come Nome_Cognome_risposte.json nella stessa cartella.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path

C_NAVY   = "#1F4E79"
C_BLUE   = "#2E75B6"
C_BG     = "#f0f4f8"
C_WHITE  = "#ffffff"
C_BORDER = "#d1d9e0"
C_TEXT   = "#1a1a2e"

FONT_UI   = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")


def load_exam_info():
    config_path = Path(__file__).parent / "exam_info.json"
    if not config_path.exists():
        messagebox.showerror(
            "Errore — file mancante",
            f"File exam_info.json non trovato in:\n{config_path.parent}\n\n"
            "Assicurati che exam_info.json sia nella stessa cartella di questo programma.",
        )
        return None
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        messagebox.showerror("Errore", f"Impossibile leggere exam_info.json:\n{e}")
        return None


def main():
    root = tk.Tk()
    root.withdraw()

    info = load_exam_info()
    if not info:
        root.destroy()
        return

    exam_name     = info.get("exam_name", "Esame")
    num_questions = info.get("num_questions", 0)
    num_choices   = info.get("num_choices", 3)
    choices       = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:max(2, min(num_choices, 26))])

    if num_questions <= 0:
        messagebox.showerror("Errore", "Configurazione non valida (num_questions <= 0).")
        root.destroy()
        return

    # ── Style ────────────────────────────────────────────────────────────────
    s = ttk.Style(root)
    s.theme_use("clam")
    s.configure("TButton",  font=FONT_UI,  padding=[8, 5])
    s.configure("TLabel",   background=C_BG, foreground=C_TEXT, font=FONT_UI)
    s.configure("TFrame",   background=C_BG)
    s.configure("TEntry",   fieldbackground=C_WHITE, font=("Segoe UI", 11))
    s.configure("TScrollbar", background=C_BORDER, troughcolor=C_BG)
    s.configure("Accent.TButton", background=C_NAVY, foreground="white", font=FONT_BOLD)
    s.map("Accent.TButton",
          background=[("active", C_BLUE), ("pressed", "#163a5a")])

    root.deiconify()
    root.title(f"Modulo Risposte — {exam_name}")
    root.configure(bg=C_BG)
    root.geometry("720x580")
    root.minsize(580, 440)

    # ── Header ────────────────────────────────────────────────────────────────
    header = tk.Frame(root, bg=C_NAVY, height=58)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)
    hf = tk.Frame(header, bg=C_NAVY)
    hf.pack(side="left", fill="y", padx=14, pady=8)
    tk.Label(hf, text=exam_name, bg=C_NAVY, fg="white",
             font=("Segoe UI", 13, "bold")).pack(anchor="w")
    tk.Label(hf, text="Seleziona una risposta per ogni domanda, poi clicca Salva",
             bg=C_NAVY, fg="#7db3e0", font=("Segoe UI", 8)).pack(anchor="w")

    # ── Body ─────────────────────────────────────────────────────────────────
    body = tk.Frame(root, bg=C_BG)
    body.pack(fill="both", expand=True, padx=12, pady=8)

    # Name row
    name_row = tk.Frame(body, bg=C_BG)
    name_row.pack(fill="x", pady=(0, 6))
    tk.Label(name_row, text="Nome e Cognome:", bg=C_BG, fg=C_TEXT,
             font=FONT_BOLD).pack(side="left", padx=(0, 8))
    name_var = tk.StringVar()
    ttk.Entry(name_row, textvariable=name_var, font=("Segoe UI", 11)).pack(
        side="left", fill="x", expand=True)

    # Progress row
    prog_row = tk.Frame(body, bg=C_BG)
    prog_row.pack(fill="x", pady=(0, 4))
    progress_var = tk.StringVar(value=f"0 / {num_questions} risposte")
    prog_label = tk.Label(prog_row, textvariable=progress_var, bg=C_BG,
                          fg="#888", font=("Segoe UI", 9))
    prog_label.pack(side="right")

    # ── Scrollable question area ──────────────────────────────────────────────
    q_outer = tk.Frame(body, bg=C_BG)
    q_outer.pack(fill="both", expand=True)

    canvas = tk.Canvas(q_outer, bg=C_BG, highlightthickness=0)
    vsb = ttk.Scrollbar(q_outer, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    inner = tk.Frame(canvas, bg=C_BG)
    canvas_win = canvas.create_window((0, 0), window=inner, anchor="nw")

    inner.bind("<Configure>",
               lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>",
                lambda e: canvas.itemconfig(canvas_win, width=e.width))
    canvas.bind_all("<MouseWheel>",
                    lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

    # ── Questions ─────────────────────────────────────────────────────────────
    answer_vars = []
    COLS = 4

    def _update_progress(*_):
        answered = sum(1 for v in answer_vars if v.get())
        if answered == num_questions:
            progress_var.set(f"{answered} / {num_questions} risposte  — tutte completate")
            prog_label.config(fg="#1e5928")
        else:
            progress_var.set(f"{answered} / {num_questions} risposte")
            prog_label.config(fg="#888")

    for q in range(num_questions):
        var = tk.StringVar(value="")
        var.trace_add("write", _update_progress)
        answer_vars.append(var)

        col_g = q % COLS
        row_g = q // COLS

        cell = tk.Frame(inner, bg=C_WHITE,
                        highlightbackground=C_BORDER, highlightthickness=1,
                        padx=4, pady=3)
        cell.grid(row=row_g, column=col_g, padx=3, pady=3, sticky="nsew")

        # Number badge
        tk.Label(cell, text=str(q + 1), bg=C_NAVY, fg="white",
                 font=("Segoe UI", 8, "bold"), width=3, pady=1).pack(side="left", padx=(0, 5))

        for ch in choices:
            tk.Radiobutton(
                cell, text=ch, variable=var, value=ch,
                indicatoron=False,
                bg="#4a86c1", fg="white",
                selectcolor=C_NAVY,
                activebackground=C_BLUE, activeforeground="white",
                relief="flat", bd=0,
                font=("Segoe UI", 9, "bold"),
                width=2, pady=2, cursor="hand2",
            ).pack(side="left", padx=1)

    for c in range(COLS):
        inner.columnconfigure(c, weight=1)

    # ── Footer ────────────────────────────────────────────────────────────────
    footer = tk.Frame(root, bg=C_BG)
    footer.pack(fill="x", padx=12, pady=(4, 10))

    status_var = tk.StringVar()
    tk.Label(footer, textvariable=status_var, bg=C_BG, fg="#1e5928",
             font=FONT_UI).pack(side="left")

    def save():
        name = name_var.get().strip()
        if not name:
            messagebox.showwarning("Attenzione",
                                   "Inserisci il tuo nome e cognome prima di salvare.")
            return

        missing = [i + 1 for i, v in enumerate(answer_vars) if not v.get()]
        if missing:
            if not messagebox.askyesno(
                "Risposte mancanti",
                f"Non hai risposto alle domande: {', '.join(map(str, missing))}\n\n"
                "Le domande senza risposta verranno conteggiate come errate.\nSalvare ugualmente?",
            ):
                return

        out_path = Path(__file__).parent / f"{_safe_name(name)}_risposte.json"
        if out_path.exists():
            if not messagebox.askyesno(
                "File già esistente",
                f"Esiste già un file per '{name}':\n{out_path.name}\n\nSovrascrivere?",
            ):
                return

        data = {
            "name":          name,
            "exam_name":     exam_name,
            "num_questions": num_questions,
            "answers":       [v.get() for v in answer_vars],
        }
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        status_var.set(f"✓ Risposte salvate: {out_path.name}")
        messagebox.showinfo(
            "Salvato",
            f"Risposte salvate in:\n{out_path}\n\nConsegna questo file al docente.",
        )

    ttk.Button(footer, text="Salva le mie risposte", style="Accent.TButton",
               command=save).pack(side="right")

    root.mainloop()


def _safe_name(name: str) -> str:
    safe = "".join(c if c.isalnum() or c in " _-" else "_" for c in name)
    return safe.strip().replace(" ", "_")


if __name__ == "__main__":
    main()
