import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os
from datetime import datetime
import psutil

class BackupApp:
    def __init__(self, master):
        self.master = master
        master.title("Backup de Pen Drive")

        # Definir tamanho mínimo
        master.minsize(width=400, height=200)

        # Obter as dimensões da tela
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        # Calcular a posição para centralizar a janela
        x = (screen_width - master.winfo_reqwidth()) // 2
        y = (screen_height - master.winfo_reqheight()) // 2

        # Definir a posição inicial da janela
        master.geometry(f"+{x}+{y}")

        self.label = tk.Label(master, text="Selecione o Pen Drive:")
        self.label.pack()

        self.button_browse = tk.Button(master, text="Procurar", command=self.find_pen_drive)
        self.button_browse.pack()

        self.backup_button = tk.Button(master, text="Fazer Backup", command=self.backup_files)
        self.backup_button.pack()

    def find_pen_drive(self):
        pen_drive_candidates = [drive.device for drive in psutil.disk_partitions() if 'removable' in drive.opts]
        
        if not pen_drive_candidates:
            messagebox.showinfo("Nenhum Pen Drive", "Nenhum pen drive encontrado.")
        else:
            pen_drive_path = filedialog.askdirectory(title="Selecione o Pen Drive", initialdir=pen_drive_candidates[0])
            self.pen_drive_path = pen_drive_path
            self.label.config(text=f"Pen Drive Selecionado: {pen_drive_path}")

    def backup_files(self):
        if not hasattr(self, 'pen_drive_path'):
            messagebox.showerror("Erro", "Por favor, selecione um Pen Drive.")
            return

        backup_folder = self.create_backup_folder()

        try:
            file_list = os.listdir(self.pen_drive_path)
            for file_name in file_list:
                source_path = os.path.join(self.pen_drive_path, file_name)
                destination_path = os.path.join(backup_folder, file_name)
                shutil.copy(source_path, destination_path)

            messagebox.showinfo("Backup Concluído", "Backup realizado com sucesso!")
            self.open_backup_folder(backup_folder)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro durante o backup: {str(e)}")

    def create_backup_folder(self):
        today = datetime.today().strftime('%Y-%m-%d')
        backup_folder = os.path.join(os.path.expanduser('~'), 'Documents', f'Backup_{today}')
        os.makedirs(backup_folder, exist_ok=True)
        return backup_folder

    def open_backup_folder(self, folder_path):
        os.startfile(folder_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = BackupApp(root)
    root.mainloop()
