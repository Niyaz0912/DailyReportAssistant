import sys
import os

# Добавляем src в путь импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.gui.app import ReportAssistant
    import customtkinter as ctk
    
    def main():
        root = ctk.CTk()
        app = ReportAssistant(root)
        root.mainloop()
        
    if __name__ == "__main__":
        main()
except Exception as e:
    print(f"Ошибка импорта: {e}")
    import traceback
    traceback.print_exc()
    input("Нажмите Enter для выхода...")
