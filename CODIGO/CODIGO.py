import os
import ctypes
import customtkinter as ctk
from tkinter import filedialog

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def is_oculto_ou_sistema(path):
    if os.name == "nt":  
        try:
            atributos = ctypes.windll.kernel32.GetFileAttributesW(str(path))
            if atributos == -1:
                return False
            FILE_ATTRIBUTE_HIDDEN = 0x2
            FILE_ATTRIBUTE_SYSTEM = 0x4
            return bool(atributos & (FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM))
        except Exception:
            return False
    else:  
        return os.path.basename(path).startswith(".")

class PastaComparerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("COMPARADOR DE FILES")
        self.geometry("800x600")

        self.diretorio1 = ""
        self.diretorio2 = ""

        self.init_ui()
        self.after(0, lambda: self.state('zoomed'))

    def init_ui(self):
        self.label_titulo = ctk.CTkLabel(self, text="COMPARADOR DE FILES", font=("Arial", 32, "bold"))
        self.label_titulo.pack(pady=(20, 10))

        frame_top = ctk.CTkFrame(self)
        frame_top.pack(pady=10, padx=20, fill="x")

        frame_botoes = ctk.CTkFrame(frame_top)
        frame_botoes.pack(anchor="center")

        self.btn_dir1 = ctk.CTkButton(frame_botoes, text="DIRETÓRIO 1", command=self.selecionar_diretorio1)
        self.btn_dir1.pack(side="left", padx=10)

        self.btn_dir2 = ctk.CTkButton(frame_botoes, text="DIRETÓRIO 2", command=self.selecionar_diretorio2)
        self.btn_dir2.pack(side="left", padx=10)

        self.result_box = ctk.CTkTextbox(self, width=600, height=300)
        self.result_box.pack(pady=10, padx=20)

        self.btn_limpar = ctk.CTkButton(self, text="LIMPAR", command=self.limpar_resultado)
        self.btn_limpar.pack(pady=10)

        self.footer_label = ctk.CTkLabel(
            self,
            text="APP CRIADO PELO VILHALVA\nGITHUB: @VILHALVA",
            text_color="white",
            bg_color="gray"
        )
        self.footer_label.pack(side="bottom", fill="x", pady=(10, 0))

    def selecionar_diretorio1(self):
        self.diretorio1 = filedialog.askdirectory(title="SELECIONE O DIRETÓRIO 1 (PAI)")
        if self.diretorio1:
            self.result_box.insert("end", f"DIRETÓRIO 1 (PAI): {self.diretorio1}\n")
        self.comparar_pastas()

    def selecionar_diretorio2(self):
        self.diretorio2 = filedialog.askdirectory(title="SELECIONE O DIRETÓRIO 2 (FILHO)")
        if self.diretorio2:
            self.result_box.insert("end", f"DIRETÓRIO 2 (FILHO): {self.diretorio2}\n\n")
        self.comparar_pastas()

    def listar_subpastas(self, raiz):
        subpastas = set()
        for dirpath, dirnames, _ in os.walk(raiz):
            dirnames[:] = [d for d in dirnames if not is_oculto_ou_sistema(os.path.join(dirpath, d))]
            for dirname in dirnames:
                caminho_relativo = os.path.relpath(os.path.join(dirpath, dirname), raiz)
                subpastas.add(caminho_relativo.replace("\\", "/"))
        return subpastas

    def listar_arquivos(self, raiz):
        arquivos = set()
        for dirpath, _, filenames in os.walk(raiz):
            for filename in filenames:
                caminho_completo = os.path.join(dirpath, filename)
                if not is_oculto_ou_sistema(caminho_completo):
                    caminho_relativo = os.path.relpath(caminho_completo, raiz)
                    arquivos.add(caminho_relativo.replace("\\", "/"))
        return arquivos

    def comparar_pastas(self):
        if not self.diretorio1 or not self.diretorio2:
            return

        pastas1 = self.listar_subpastas(self.diretorio1)
        pastas2 = self.listar_subpastas(self.diretorio2)

        arquivos1 = self.listar_arquivos(self.diretorio1)
        arquivos2 = self.listar_arquivos(self.diretorio2)

        faltando_pastas = pastas1 - pastas2
        faltando_arquivos = arquivos1 - arquivos2

        if faltando_pastas:
            self.result_box.insert("end", "📁 PASTAS/SUBPASTAS FALTANDO NO DIRETÓRIO 2:\n\n")
            for pasta in sorted(faltando_pastas):
                self.result_box.insert("end", f"- {pasta}/\n")
            self.result_box.insert("end", "\n")

        if faltando_arquivos:
            self.result_box.insert("end", "📄 ARQUIVOS FALTANDO NO DIRETÓRIO 2:\n\n")
            for arquivo in sorted(faltando_arquivos):
                self.result_box.insert("end", f"- {arquivo}\n")
            self.result_box.insert("end", "\n")

        if not faltando_pastas and not faltando_arquivos:
            self.result_box.insert("end", "✅ NENHUMA PASTA OU ARQUIVO FALTANDO. OS DIRETÓRIOS ESTÃO SINCRONIZADOS!\n")

    def limpar_resultado(self):
        self.result_box.delete("1.0", "end")

if __name__ == "__main__":
    app = PastaComparerApp()
    app.mainloop()
