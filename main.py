import customtkinter as ctk
from gui import ReportAssistant

if __name__ == "__main__":
    root = ctk.CTk()
    app = ReportAssistant(root)
    root.mainloop()