import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PyPDF2 import PdfMerger

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger - v0.1")

        self.pdf_list = []  # Lista para almacenar las rutas de los PDFs
        self.merger = PdfMerger()  # Instancia de PdfMerger para fusionar PDFs

        self.pdf_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        self.pdf_listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.add_button = tk.Button(root, text="1-Agregar PDFs", command=self.add_pdfs)
        self.add_button.pack(pady=10)

        self.delete_button = tk.Button(root, text="2-Eliminar PDF", command=self.delete_pdf)
        self.delete_button.pack(pady=5)

        self.merge_button = tk.Button(root, text="3-Unir PDFs", command=self.merge_pdfs)
        self.merge_button.pack(pady=10)

    def add_pdfs(self):
        if len(self.pdf_list) < 50:
            file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
            for path in file_paths:
                self.pdf_list.append(path)
                self.pdf_listbox.insert(tk.END, path)
        else:
            messagebox.showwarning("Advertencia", "Se ha alcanzado el máximo de 50 PDFs.")

    def delete_pdf(self):
        selected_indices = self.pdf_listbox.curselection()
        for index in selected_indices:
            pdf_path = self.pdf_list[index]
            self.pdf_list.remove(pdf_path)
            self.pdf_listbox.delete(index)
            self.merger.pages.pop(index)

    def merge_pdfs(self):
        if len(self.pdf_list) == 0:
            messagebox.showwarning("Advertencia", "No se han agregado PDFs para unir.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if output_path:
            try:
                for path in self.pdf_list:
                    self.merger.append(path)
                with open(output_path, "wb") as output_file:
                    self.merger.write(output_file)
                self.merger.close()
                self.pdf_list = []
                self.pdf_listbox.delete(0, tk.END)
                messagebox.showinfo("Éxito", "El PDF ha sido unido y guardado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", "Error al unir el PDF: " + str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
