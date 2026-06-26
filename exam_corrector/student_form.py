#!/usr/bin/env python3
"""
ExamCorrector - Modulo Risposta Studente

Legge exam_info.json dalla stessa cartella e mostra il modulo di risposta.
Fase 1: inserimento nome. Fase 2: avvia esame (con timer countdown se configurato).
Salva le risposte come NomeCognome_risposte.json nella stessa cartella.
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

    exam_name        = info.get("exam_name", "Esame")
    num_questions    = info.get("num_questions", 0)
    num_choices      = info.get("num_choices", 3)
    duration_minutes = int(info.get("duration_minutes", 0))
    choices          = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:max(2, min(num_choices, 26))])

    if num_questions <= 0:
        messagebox.showerror("Errore", "Configurazione non valida (num_questions <= 0).")
        root.destroy()
        return

    # ── Style ────────────────────────────────────────────────────────────────
    s = ttk.Style(root)
    s.theme_use("clam")
    s.configure("TButton",    font=FONT_UI, padding=[8, 5])
    s.configure("TLabel",     background=C_BG, foreground=C_TEXT, font=FONT_UI)
    s.configure("TFrame",     background=C_BG)
    s.configure("TEntry",     fieldbackground=C_WHITE, font=("Segoe UI", 11))
    s.configure("TScrollbar", background=C_BORDER, troughcolor=C_BG)
    s.configure("Accent.TButton",  background=C_NAVY,    foreground="white", font=FONT_BOLD)
    s.configure("Start.TButton",   background="#1e5928", foreground="white",
                font=("Segoe UI", 11, "bold"))
    s.map("Accent.TButton", background=[("active", C_BLUE), ("pressed", "#163a5a")])
    s.map("Start.TButton",  background=[("active", "#2a7a38"), ("pressed", "#155520")])

    root.deiconify()
    root.title(f"Modulo Risposte — {exam_name}")
    root.configure(bg=C_BG)
    root.geometry("720x600")
    root.minsize(580, 460)

    # ── Header ────────────────────────────────────────────────────────────────
    header = tk.Frame(root, bg=C_NAVY, height=58)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)

    hf = tk.Frame(header, bg=C_NAVY)
    hf.pack(side="left", fill="y", padx=14, pady=8)
    tk.Label(hf, text=exam_name, bg=C_NAVY, fg="white",
             font=("Segoe UI", 13, "bold")).pack(anchor="w")
    header_sub_var = tk.StringVar(value="Inserisci i tuoi dati e avvia l'esame")
    tk.Label(hf, textvariable=header_sub_var,
             bg=C_NAVY, fg="#7db3e0", font=("Segoe UI", 8)).pack(anchor="w")

    # Timer widget in header (right side) — solo se durata > 0
    timer_var       = tk.StringVar()
    timer_val_label = None
    timer_bg_frames = []
    if duration_minutes > 0:
        tf = tk.Frame(header, bg=C_NAVY)
        tf.pack(side="right", fill="y", padx=14, pady=6)
        timer_bg_frames.extend([header, hf, tf])
        tk.Label(tf, text="Tempo rimanente", bg=C_NAVY, fg="#7db3e0",
                 font=("Segoe UI", 7)).pack(anchor="e")
        timer_val_label = tk.Label(tf, textvariable=timer_var,
                                    bg=C_NAVY, fg="white",
                                    font=("Segoe UI", 18, "bold"), width=5)
        timer_val_label.pack(anchor="e")
        timer_var.set(f"{duration_minutes:02d}:00")

    # ── Timer logic ───────────────────────────────────────────────────────────
    _remaining    = [duration_minutes * 60]
    _timer_active = [False]

    def _tick():
        if not _timer_active[0]:
            return
        if _remaining[0] <= 0:
            _timer_active[0] = False
            timer_var.set("00:00")
            if timer_val_label:
                timer_val_label.config(fg="#FF6666")
            _auto_save()
            return
        m, s = divmod(_remaining[0], 60)
        timer_var.set(f"{m:02d}:{s:02d}")
        if timer_val_label:
            if _remaining[0] <= 60:
                timer_val_label.config(fg="#FF4444")
                for fr in timer_bg_frames:
                    fr.config(bg="#8B1a1a")
                timer_val_label.config(bg="#8B1a1a")
            elif _remaining[0] <= 300:
                timer_val_label.config(fg="#FFDD44")
                for fr in timer_bg_frames:
                    fr.config(bg="#7d5000")
                timer_val_label.config(bg="#7d5000")
        _remaining[0] -= 1
        root.after(1000, _tick)

    def _auto_save():
        name    = name_var.get().strip() or "studente"
        answers = [v.get() for v in answer_vars]
        out     = Path(__file__).parent / f"{_safe_name(name)}_risposte.json"
        data    = {"name": name, "exam_name": exam_name,
                   "num_questions": num_questions, "answers": answers, "auto_saved": True}
        try:
            with open(out, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            messagebox.showwarning(
                "Tempo scaduto",
                f"Il tempo è scaduto!\n\nRisposte salvate automaticamente in:\n{out.name}"
                "\n\nConsegna questo file al docente.",
            )
        except Exception as e:
            messagebox.showerror("Errore salvataggio automatico", str(e))

    # ── Bottom bar (switcha contenuto tra le due fasi) ────────────────────────
    bottom_bar = tk.Frame(root, bg=C_BG)
    bottom_bar.pack(fill="x", side="bottom", padx=12, pady=(4, 10))

    status_var = tk.StringVar()
    status_lbl = tk.Label(bottom_bar, textvariable=status_var, bg=C_BG,
                           fg="#1e5928", font=FONT_UI)

    # ── Contenuto centrale (si scambia tra fase 1 e fase 2) ──────────────────
    middle = tk.Frame(root, bg=C_BG)
    middle.pack(fill="both", expand=True, padx=12, pady=8)

    # ════════════════════════════════════════════════════════════
    # FASE 1 — inserimento dati studente
    # ════════════════════════════════════════════════════════════
    setup_frame = tk.Frame(middle, bg=C_BG)
    setup_frame.pack(fill="both", expand=True)

    if duration_minutes > 0:
        dur_banner = tk.Frame(setup_frame, bg="#dce6f0",
                               highlightbackground=C_BORDER, highlightthickness=1)
        dur_banner.pack(fill="x", pady=(0, 12))
        tk.Label(dur_banner, text=f"  Durata: {duration_minutes} minuti",
                 bg="#dce6f0", fg=C_NAVY, font=FONT_BOLD, pady=9, anchor="w").pack(
            fill="x", padx=14)

    name_card = tk.LabelFrame(setup_frame, text="  Dati Studente  ",
                               bg=C_BG, fg=C_NAVY, font=FONT_BOLD, relief="groove", bd=2)
    name_card.pack(fill="x", pady=(0, 12))
    tk.Label(name_card, text="Nome e Cognome:", bg=C_BG, font=FONT_BOLD).pack(
        anchor="w", padx=12, pady=(8, 2))
    name_var = tk.StringVar()
    name_entry = ttk.Entry(name_card, textvariable=name_var, font=("Segoe UI", 12))
    name_entry.pack(fill="x", padx=12, pady=(0, 12))
    name_entry.focus_set()

    def start_exam():
        name = name_var.get().strip()
        if not name:
            messagebox.showwarning("Attenzione", "Inserisci il tuo nome e cognome.")
            name_entry.focus_set()
            return
        setup_frame.pack_forget()
        avvia_btn.pack_forget()
        exam_frame.pack(fill="both", expand=True)
        status_lbl.pack(side="left")
        salva_btn.pack(side="right")
        header_sub_var.set("Rispondi a tutte le domande, poi clicca Salva")
        if duration_minutes > 0:
            _timer_active[0] = True
            _tick()

    avvia_btn = ttk.Button(bottom_bar, text="▶  Avvia Esame",
                            style="Start.TButton", command=start_exam)
    avvia_btn.pack(fill="x")
    name_entry.bind("<Return>", lambda e: start_exam())

    # ════════════════════════════════════════════════════════════
    # FASE 2 — griglia risposte
    # ════════════════════════════════════════════════════════════
    exam_frame = tk.Frame(middle, bg=C_BG)

    # Progress counter
    progress_var = tk.StringVar(value=f"0 / {num_questions} risposte")
    prog_label   = tk.Label(exam_frame, textvariable=progress_var, bg=C_BG,
                             fg="#888", font=("Segoe UI", 9))
    prog_label.pack(anchor="e", pady=(0, 4))

    # Scrollable question area
    q_outer = tk.Frame(exam_frame, bg=C_BG)
    q_outer.pack(fill="both", expand=True)

    canvas     = tk.Canvas(q_outer, bg=C_BG, highlightthickness=0)
    vsb        = ttk.Scrollbar(q_outer, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    inner      = tk.Frame(canvas, bg=C_BG)
    canvas_win = canvas.create_window((0, 0), window=inner, anchor="nw")
    inner.bind("<Configure>",
               lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>",
                lambda e: canvas.itemconfig(canvas_win, width=e.width))
    canvas.bind_all("<MouseWheel>",
                    lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

    # Questions
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

        cell = tk.Frame(inner, bg=C_WHITE,
                        highlightbackground=C_BORDER, highlightthickness=1,
                        padx=4, pady=3)
        cell.grid(row=q // COLS, column=q % COLS, padx=3, pady=3, sticky="nsew")
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

    # ── Save button (aggiunto alla bottom_bar alla transizione fase 1→2) ──────
    def save():
        name    = name_var.get().strip()
        missing = [i + 1 for i, v in enumerate(answer_vars) if not v.get()]
        if missing:
            if not messagebox.askyesno(
                "Risposte mancanti",
                f"Non hai risposto alle domande: {', '.join(map(str, missing))}\n\n"
                "Le domande senza risposta verranno conteggiate come errate.\nSalvare ugualmente?",
            ):
                return
        out = Path(__file__).parent / f"{_safe_name(name)}_risposte.json"
        if out.exists():
            if not messagebox.askyesno(
                "File già esistente",
                f"Esiste già un file per '{name}':\n{out.name}\n\nSovrascrivere?",
            ):
                return
        _timer_active[0] = False
        data = {"name": name, "exam_name": exam_name,
                "num_questions": num_questions, "answers": [v.get() for v in answer_vars]}
        with open(out, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        status_var.set(f"✓ Risposte salvate: {out.name}")
        messagebox.showinfo("Salvato",
                            f"Risposte salvate in:\n{out}\n\nConsegna questo file al docente.")

    salva_btn = ttk.Button(bottom_bar, text="Salva le mie risposte",
                            style="Accent.TButton", command=save)

    root.mainloop()


def _safe_name(name: str) -> str:
    safe = "".join(c if c.isalnum() or c in " _-" else "_" for c in name)
    return safe.strip().replace(" ", "_")


if __name__ == "__main__":
    main()
