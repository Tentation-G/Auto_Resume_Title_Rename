import pymupdf  # type: ignore
from pathlib import Path
import customtkinter as ctk # type: ignore


# ──────────────────────────────────────────────────────────────────────┐
FILE_IN     = "cv_fl_template/CV_2025_Flavien_CAMPEAUX_TitleLess.pdf"  #│ 
FILE_OUT    = "CV_2025_Flavien_CAMPEAUX_"                              #│
SEARCH_TEXT = "Recherche d’alternance"                                 #│
NEW_TEXT    = " "                                                      #│
FONT_PATH   = r"fonts\proximanova_regular.ttf"                         #│
FONT_SIZE   = 15                                                       #│
COLOR       = (0, 0, 0)                                                #│
OFFSET_X    = 12                                                       #│
OFFSET_Y    = 12                                                       #│
# ──────────────────────────────────────────────────────────────────────┘

# Front
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("App")
        self.geometry("400x200")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Label + Entry NEW_TEXT
        ctk.CTkLabel(self, text="New Resume Title:").grid(row=0, column=0, padx=10, pady=(10))
        self.new_resume_title_entry = ctk.CTkEntry(self, width=400)
        # valeur par défaut
        self.new_resume_title_entry.insert(0, " ")  
        self.new_resume_title_entry.grid(row=1, column=0, padx=10, pady=(10))

        # Bouton Valider
        self.validate_btn = ctk.CTkButton(self, text="Valider", command=self.on_validate)
        self.validate_btn.grid(row=2, column=0, columnspan=2, pady=20)

    def on_validate(self):
        # get
        NEW_TEXT = self.new_resume_title_entry.get()
        modif_resume_title(
            FILE_IN,
            FILE_OUT,
            SEARCH_TEXT,
            NEW_TEXT
        )
        print(NEW_TEXT)

if __name__ == "__main__":
    app = App()
    app.mainloop()

# Back
def modif_resume_title(pdf_in, pdf_out, search_txt, new_txt):
    if not Path(FONT_PATH).exists():
        raise FileNotFoundError(f"Police introuvable : {FONT_PATH}")

    doc = pymupdf.open(pdf_in)
    page = doc.load_page(0)

    rects = page.search_for(search_txt)
    if not rects:
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

FILE_OUT_SUF = NEW_TEXT.replace(" ", "_")
FILE_OUT += FILE_OUT_SUF + ".pdf"
