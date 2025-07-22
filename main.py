from tkinter import messagebox
import pymupdf  # type: ignore
from pathlib import Path
import customtkinter as ctk  # type: ignore
import re

# ──────────────────────────────────────────────────────────────────────────┐
FILE_IN          = "cv_fl_template/CV_2025_Flavien_CAMPEAUX_TitleLess.pdf" #│
FILE_OUT_PREFIX  = "CV_2025_Flavien_CAMPEAUX_"                             #│
SEARCH_TEXT      = "Recherche d’alternance"                                #│     
FONT_PATH        = r"fonts/proximanova_regular.ttf"                        #│
OUTPUT_DIR       = r"pdf_cv/"                                              #│
FONT_SIZE        = 15                                                      #│
COLOR            = (0, 0, 0)                                               #│
OFFSET_X         = 12                                                      #│
OFFSET_Y         = 12                                                      #│
# ──────────────────────────────────────────────────────────────────────────┘

def modif_resume_title(pdf_in, pdf_out, search_txt, new_txt):
    if not Path(FONT_PATH).exists():
        raise FileNotFoundError(f"Police introuvable : {FONT_PATH}")

    doc = pymupdf.open(pdf_in)
    page = doc.load_page(0)

    rects = page.search_for(search_txt)
    if not rects:
        doc.close()
        raise RuntimeError(f"'{search_txt}' non trouvé dans le PDF.")
    r = rects[0]

    x_start = r.x1 + OFFSET_X
    y_start = r.y0 + OFFSET_Y

    page.insert_text(
        (x_start, y_start),
        new_txt,
        fontname="ProximaNova",
        fontfile=FONT_PATH,
        fontsize=FONT_SIZE,
        color=COLOR
    )

    doc.save(pdf_out)
    doc.close()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Modifier le titre du CV")
        self.geometry("400x160")
        self.resizable(False, False)

        # Label + Entry pour le nouveau texte
        ctk.CTkLabel(self, text="Nouveau texte à insérer :").grid(row=0, column=0, padx=10, pady=(15, 5), sticky="w")
        self.new_text_entry = ctk.CTkEntry(self, width=380)
        # vide par défaut
        self.new_text_entry.insert(0, "")  
        self.new_text_entry.grid(row=1, column=0, padx=10, sticky="ew")

        # Bouton Valider
        self.validate_btn = ctk.CTkButton(self, text="Valider", command=self.on_validate)
        self.validate_btn.grid(row=2, column=0, padx=10, pady=20, sticky="ew")

    def on_validate(self):
        new_txt = self.new_text_entry.get().strip()
        if not new_txt:
            print("Erreur : veuillez saisir un texte.")
            return

        # Nettoyage et suffixage
        safe_suffix = re.sub(r'[^A-Za-z0-9_-]', '', new_txt.replace(' ', '_'))
        if not safe_suffix:
            print("Erreur : le texte saisi n'est pas valide pour un nom de fichier.")
            return
        pdf_filename = f"{FILE_OUT_PREFIX}{safe_suffix}.pdf"
        pdf_out = OUTPUT_DIR + pdf_filename

        try:
            modif_resume_title(FILE_IN, str(pdf_out), SEARCH_TEXT, new_txt)
            messagebox.showinfo(
                "Succès",
                f"Le PDF a bien été généré :\n{pdf_out}"
            )
        except Exception as e:
            messagebox.showerror(
                "Erreur", 
                f"Impossible de générer le PDF :\n{e}"
            )


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()