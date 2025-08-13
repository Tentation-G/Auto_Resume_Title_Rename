from tkinter import messagebox
import pymupdf  # type: ignore
from pathlib import Path
import customtkinter as ctk  # type: ignore
import re

# ──────────────────────────────────────────────────────────────────────────┐
FILE_IN          = "cv_fl_template/CV_2025_Flavien_CAMPEAUX_.pdf"          #│
FILE_OUT_PREFIX  = "CV_2025_Flavien_CAMPEAUX_"                             #│
SEARCH_TEXT      = "Recherche d’alternance"                                #│     
SEARCH_YEAR      = "  ans"                                                 #│     
FONT_PATH        = r"fonts/proximanova_regular.ttf"                        #│
OUTPUT_DIR       = r"pdf_file/"                                            #│
#                                                                          #│
COLOR            = (0, 0, 0)                                               #|
# Title Data                                                               #│
FONT_SIZE_TITLE  = 15                                                      #│
OFFSET_X_TITLE   = 12                                                      #│
OFFSET_Y_TITLE   = 12                                                      #│
# Years Data                                                               #│
FONT_SIZE_YEAR   = 12                                                      #│
OFFSET_X_YEAR    = -28                                                     #│
OFFSET_Y_YEAR    = 9.5                                                     #│
# S Data                                                                   #│
FONT_SIZE_S      = 10                                                      #│
OFFSET_X_S       = 0                                                       #│
OFFSET_Y_S       = 10                                                      #│
# ──────────────────────────────────────────────────────────────────────────┘

def modif_resume_title(pdf_in, pdf_out, search_txt, search_year, new_txt, new_nby):
    if not Path(FONT_PATH).exists():
        raise FileNotFoundError(f"Police introuvable : {FONT_PATH}")

    doc = pymupdf.open(pdf_in)
    page = doc.load_page(0)

    # Title coord
    rects_title = page.search_for(search_txt)
    if not rects_title:
        doc.close()
        raise RuntimeError(f"'{search_txt}' non trouvé dans le PDF.")
    r_title = rects_title[0]

    x_start_title = r_title.x1 + OFFSET_X_TITLE
    y_start_title = r_title.y0 + OFFSET_Y_TITLE
    
    # Year coord
    rects_year = page.search_for(search_year)
    if not rects_year:
        doc.close()
        raise RuntimeError(f"'{search_year}' non trouvé dans le PDF.")
    r_year = rects_year[1]

    x_start_year = r_year.x1 + OFFSET_X_YEAR
    y_start_year = r_year.y0 + OFFSET_Y_YEAR
    
    if new_nby == "1":
        rect_s = pymupdf.Rect(
            r_year.x1 - 5,  # 5 points à gauche depuis la fin du mot
            r_year.y0,
            r_year.x1,
            r_year.y1
        )
        page.draw_rect(
            rect_s, 
            fill=(1, 1, 1),
            color=(1, 1, 1)
        )

    # insertion titre cv
    page.insert_text(
        (x_start_title, y_start_title),
        new_txt,
        fontname="ProximaNova",
        fontfile=FONT_PATH,
        fontsize=FONT_SIZE_TITLE,
        color=COLOR
    )
    
    # Insertion nb année(s)
    page.insert_text(
        (x_start_year, y_start_year),
        new_nby,
        fontname="ProximaNova",
        fontfile=FONT_PATH,
        fontsize=FONT_SIZE_YEAR,
        color=COLOR
    )

    doc.save(pdf_out)
    doc.close()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Modifier le titre du CV")
        self.resizable(False, False)

        # Label + Entry pour titre cv
        ctk.CTkLabel(self, text="Titre du poste :").grid(row=0, column=0, padx=10, pady=(15, 5), sticky="w")
        self.new_text_entry = ctk.CTkEntry(self, width=380)
        # vide par défaut
        self.new_text_entry.insert(0, "")  
        self.new_text_entry.grid(row=1, column=0, padx=10, sticky="ew")
        
        # Label + Entry pour nb années
        ctk.CTkLabel(self, text="Durée contract (année(s)) :").grid(row=2, column=0, padx=10, pady=(15, 5), sticky="w")
        self.new_nby_entry = ctk.CTkEntry(self, width=380)
        # vide par défaut
        self.new_nby_entry.insert(0, "")  
        self.new_nby_entry.grid(row=3, column=0, padx=10, sticky="ew")

        # Bouton Valider
        self.validate_btn = ctk.CTkButton(self, text="Valider", command=self.on_validate)
        self.validate_btn.grid(row=4, column=0, padx=10, pady=20, sticky="ew")

    def on_validate(self):
        new_txt = self.new_text_entry.get().strip()
        new_nby = self.new_nby_entry.get().strip()
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
            modif_resume_title(FILE_IN, str(pdf_out), SEARCH_TEXT, SEARCH_YEAR, new_txt, new_nby)
            messagebox.showinfo(
                "Succès",
                f"Le PDF a bien été généré :\n{pdf_out}"
            )
        except Exception as e:
            messagebox.showerror(
                "Erreur", 
                f"Impossible de générer le PDF :\n{e}"
            )
            
        self.update()
        self.geometry()


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()