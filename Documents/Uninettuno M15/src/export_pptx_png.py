import sys
import pathlib
import win32com.client

sys.stdout.reconfigure(encoding="utf-8")

def export_presentation_to_png(pptx_path: pathlib.Path, output_dir: pathlib.Path, width=1920, height=1080):
    output_dir.mkdir(parents=True, exist_ok=True)
    abs_pptx = str(pptx_path.resolve())
    
    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    # Non rendiamo visibile la finestra o lasciamola minimizzata
    try:
        prs = powerpoint.Presentations.Open(abs_pptx, WithWindow=False)
    except Exception:
        prs = powerpoint.Presentations.Open(abs_pptx)
        
    try:
        total = prs.Slides.Count
        print(f"Esportazione di {total} slide da {pptx_path.name} a {output_dir} ({width}x{height})...")
        for idx in range(1, total + 1):
            slide = prs.Slides(idx)
            out_file = output_dir / f"slide_{idx:02d}.png"
            slide.Export(str(out_file.resolve()), "PNG", width, height)
            print(f"  [OK] Salvata {out_file.name}")
    finally:
        prs.Close()
        # Non chiudiamo l'applicazione se l'utente la stava usando, ma se non ci sono altre presentazioni aperte possiamo uscire
        if powerpoint.Presentations.Count == 0:
            powerpoint.Quit()

if __name__ == "__main__":
    pptx_file = pathlib.Path("pptx/MTG_Lezione_03.pptx")
    out_dir = pathlib.Path("pptx/renders_lez03")
    export_presentation_to_png(pptx_file, out_dir)
