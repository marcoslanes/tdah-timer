import customtkinter as ctk
import time
import csv
from datetime import datetime
import os
from tkinter import messagebox

# CONFIGURAÇÕES VISUAIS DO ÍCONE
# Ao gerar o .exe, você precisará converter a imagem acima para 'icon.ico'
# e colocá-la na mesma pasta do script, ou incorporá-la no build.

class ChamadoRow:
    def __init__(self, master, app_instance):
        self.master = master
        self.app = app_instance
        self.running = False
        self.paused = False
        self.start_time = 0
        self.elapsed_time = 0
        self.finalizado = False
        self.blink_state = False

        # Container da Linha (Design Premium)
        self.frame = ctk.CTkFrame(master, corner_radius=20, fg_color="#1e1e1e", border_width=1, border_color="#333")
        self.frame.pack(fill="x", padx=5, pady=4)

        # ID (Aumentado e Centralizado)
        self.entry_id = ctk.CTkEntry(self.frame, placeholder_text="ID", width=100, height=36, 
                                     fg_color="#121212", border_color="#3a3a3a", corner_radius=10, justify="center")
        self.entry_id.pack(side="left", padx=(15, 5), pady=10)

        # Descrição
        self.entry_desc = ctk.CTkEntry(self.frame, placeholder_text="Detalhamento...", 
                                       height=36, fg_color="#121212", border_color="#3a3a3a", corner_radius=10)
        self.entry_desc.pack(side="left", padx=5, pady=10, expand=True, fill="x")

        # Tempo e Status (Fonte Consolas para precisão)
        self.label_timer = ctk.CTkLabel(self.frame, text="00:00:00", font=("Consolas", 18, "bold"), text_color="#00FF41", width=100)
        self.label_timer.pack(side="left", padx=10)

        self.label_status = ctk.CTkLabel(self.frame, text="Aguardando", font=("Segoe UI", 11), text_color="#777", width=80)
        self.label_status.pack(side="left", padx=5)

        # Botões Circulares Modernos
        btn_size = 36
        btn_radius = 18

        self.btn_play = ctk.CTkButton(self.frame, text="▶", width=btn_size, height=btn_size, corner_radius=btn_radius,
                                      fg_color="#27ae60", hover_color="#2ecc71", font=("Arial", 12), command=self.start)
        self.btn_play.pack(side="left", padx=2)

        self.btn_pause = ctk.CTkButton(self.frame, text="||", width=btn_size, height=btn_size, corner_radius=btn_radius,
                                       fg_color="#f39c12", hover_color="#f1c40f", text_color="black", font=("Arial", 10, "bold"), command=self.pause)
        self.btn_pause.pack(side="left", padx=2)

        self.btn_stop = ctk.CTkButton(self.frame, text="■", width=btn_size, height=btn_size, corner_radius=btn_radius,
                                      fg_color="#c0392b", hover_color="#e74c3c", font=("Arial", 12), command=self.stop)
        self.btn_stop.pack(side="left", padx=2)

        # Botão Apagar Registro (Design Discreto)
        self.btn_del = ctk.CTkButton(self.frame, text="✕", width=btn_size, height=btn_size, corner_radius=btn_radius,
                                      fg_color="transparent", border_width=1, border_color="#444", 
                                      hover_color="#550000", font=("Arial", 11), command=self.confirm_delete)
        self.btn_del.pack(side="left", padx=(5, 15))

    def confirm_delete(self):
        # Janela de confirmação nativa (leve)
        if messagebox.askyesno("Confirmar", "Deseja apagar este registro permanentemente?"):
            self.app.remove_row(self)

    def blink(self):
        if self.paused and not self.finalizado:
            # Efeito de pisca em amarelo sutil
            color = "#3d3200" if self.blink_state else "#1e1e1e"
            self.frame.configure(fg_color=color)
            self.blink_state = not self.blink_state
            self.master.after(700, self.blink)
        elif not self.paused and not self.finalizado:
            self.frame.configure(fg_color="#1e1e1e")

    def update_label(self):
        if self.running:
            total = self.elapsed_time + (time.time() - self.start_time)
            self.label_timer.configure(text=self.format_time(total))
            self.master.after(1000, self.update_label)

    def format_time(self, seconds):
        h, m, s = int(seconds // 3600), int((seconds % 3600) // 60), int(seconds % 60)
        return f"{h:02d}:{m:02d}:{s:02d}"

    def start(self):
        if not self.running and not self.finalizado:
            self.start_time = time.time()
            self.running, self.paused = True, False
            self.label_timer.configure(text_color="#00FF41") # Verde Matrix
            self.label_status.configure(text="Em curso", text_color="#00FF41")
            self.blink()
            self.update_label()

    def pause(self):
        if self.running:
            self.elapsed_time += time.time() - self.start_time
            self.running, self.paused = False, True
            self.label_timer.configure(text_color="#f39c12")
            self.label_status.configure(text="Pausado", text_color="#f39c12")
            self.blink()

    def stop(self):
        if not self.finalizado:
            if self.running: self.pause()
            self.finalizado, self.paused = True, False
            self.frame.configure(fg_color="#111", border_color="#222") # Linha Finalizada
            self.label_timer.configure(text_color="#444")
            self.label_status.configure(text="Finalizado", text_color="#444")
            self.entry_id.configure(state="disabled", text_color="#444")
            self.entry_desc.configure(state="disabled", text_color="#444")
            for btn in [self.btn_play, self.btn_pause, self.btn_stop]:
                btn.configure(state="disabled", fg_color="#1a1a1a")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # NOME ATUALIZADO AQUI
        self.title("Shield Timer | SOC Ops Tracker")
        self.geometry("1100x750")
        ctk.set_appearance_mode("dark")

        # Cabeçalho de Ações
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=40, pady=(30, 10))

        # Ações Globais à direita
        self.btn_report = ctk.CTkButton(self.header, text="📝", font=("Arial", 22), width=50, height=50,
                                        fg_color="#2b2b2b", hover_color="#3a3a3a", corner_radius=12, command=self.export_csv)
        self.btn_report.pack(side="right", padx=(10, 0))

        self.btn_clear = ctk.CTkButton(self.header, text="🗑", font=("Arial", 22), width=50, height=50,
                                       fg_color="#2b2b2b", hover_color="#880000", corner_radius=12, command=self.confirm_clear_all)
        self.btn_clear.pack(side="right", padx=(10, 0))

        self.btn_add = ctk.CTkButton(self.header, text="+ NOVO CHAMADO", font=("Segoe UI", 12, "bold"),
                                     fg_color="#0078D7", hover_color="#005a9e", height=50, corner_radius=12, command=self.add_row)
        self.btn_add.pack(side="right")

        # Container da Listagem
        self.list_container = ctk.CTkFrame(self, fg_color="#121212", corner_radius=15)
        self.list_container.pack(fill="both", expand=True, padx=25, pady=20)

        # TÍTULO DA SEÇÃO ATUALIZADO AQUI
        self.section_title = ctk.CTkLabel(self.list_container, text="LISTAGEM DE REGISTROS", 
                                          font=("Segoe UI", 11, "bold"), text_color="#aaa")
        self.section_title.pack(anchor="w", padx=20, pady=(15, 5))

        # Legenda das Colunas (Header da Tabela)
        self.legend_frame = ctk.CTkFrame(self.list_container, fg_color="transparent", height=30)
        self.legend_frame.pack(fill="x", padx=20)

        labels = [("ID", 100), ("DESCRIÇÃO", 0), ("TEMPO", 100), ("STATUS", 80), ("AÇÕES", 160)]
        for text, width in labels:
            expand = True if text == "DESCRIÇÃO" else False
            anchor = "w" if text == "DESCRIÇÃO" else "center"
            ctk.CTkLabel(self.legend_frame, text=text, font=("Segoe UI", 10, "bold"), 
                         text_color="#555", width=width).pack(side="left", padx=5, expand=expand, anchor=anchor)

        # Scrollable Area
        self.scroll = ctk.CTkScrollableFrame(self.list_container, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=10, pady=(0, 15))

        self.rows = []

    def add_row(self):
        self.rows.append(ChamadoRow(self.scroll, self))

    def remove_row(self, row_obj):
        row_obj.frame.destroy()
        self.rows.remove(row_obj)

    def confirm_clear_all(self):
        if self.rows and messagebox.askyesno("Limpar Tela", "Isso apagará TODOS os registros da tela. Continuar?"):
            for row in self.rows[:]:
                self.remove_row(row)

    def export_csv(self):
        if not self.rows: return
        path = f"report_soc_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["ID", "Descricao", "Tempo", "Status"])
            for r in self.rows:
                status = r.label_status.cget("text")
                w.writerow([r.entry_id.get(), r.entry_desc.get(), r.label_timer.cget("text"), status])
        os.startfile(os.getcwd())

if __name__ == "__main__":
    app = App()
    app.mainloop()