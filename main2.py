import tkinter as tk
from tkinter import filedialog, messagebox
from collections import Counter
import string
import matplotlib.pyplot as plt

ALLOWED_CHARACTERS = set(string.ascii_letters + string.digits + ".,!@#$%^&*")

def validate_text(text):
    return all(char in ALLOWED_CHARACTERS for char in text)

def analyze_text(text):
    counter = Counter(text)
    total_characters = sum(counter.values())
    frequency = {char: count / total_characters for char, count in counter.items()}
    return counter, frequency

def load_text_from_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                text = file.read()
                return text
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Αποτυχία φόρτωσης αρχείου: {e}")
    return None

def display_results(counter, frequency):
    results_window = tk.Toplevel(root)
    results_window.title("Αποτελέσματα")
    frame = tk.Frame(results_window)
    frame.pack(fill=tk.BOTH, expand=True)
    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tk.Label(scrollable_frame, text="Καταμέτρηση χαρακτήρων:").pack()
    for char in sorted(ALLOWED_CHARACTERS):
        count = counter.get(char, 0)
        tk.Label(scrollable_frame, text=f"'{char}': {count}").pack()

    tk.Label(scrollable_frame, text="\nΣυχνότητα εμφάνισης:").pack()
    sorted_frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
    for char, freq in sorted_frequency:
        tk.Label(scrollable_frame, text=f"'{char}': {freq:.4f}").pack()

    display_frequency_chart(sorted_frequency)

def display_frequency_chart(sorted_frequency):
    characters = [char for char, _ in sorted_frequency]
    frequencies = [freq for _, freq in sorted_frequency]
    plt.figure(figsize=(10, 6))
    plt.bar(characters, frequencies, color="skyblue")
    plt.xlabel("Χαρακτήρες")
    plt.ylabel("Συχνότητα")
    plt.title("Συχνότητα Εμφάνισης Χαρακτήρων")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def process_text_input():
    text = text_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Προειδοποίηση", "Παρακαλώ εισάγετε κείμενο.")
        return

    if not validate_text(text):
        messagebox.showerror("Σφάλμα", "Το κείμενο μπορεί να περιέχει μόνο τους εξής χαρακτήρες:\n "
                                       "Λατινικούς χαρακτήρες (πεζά a-z και κεφαλαία A-Z).\n"
                                       "Αριθμούς (0-9).\n"
                                       "Τα παρακάτω επιτρεπτά σύμβολα: .,!@#$%^&*")
        return

    counter, frequency = analyze_text(text)
    display_results(counter, frequency)

def process_text_file():
    text = load_text_from_file()
    if text is None:
        return

    if not validate_text(text):
        messagebox.showerror("Σφάλμα", "Το κείμενο μπορεί να περιέχει μόνο τους εξής χαρακτήρες:\n"
                                       "Λατινικούς χαρακτήρες (πεζά a-z και κεφαλαία A-Z).\n"
                                       "Αριθμούς (0-9).\n"
                                       "Τα παρακάτω επιτρεπτά σύμβολα: .,!@#$%^&*")
        return

    counter, frequency = analyze_text(text)
    display_results(counter, frequency)

root = tk.Tk()
root.title("Ανάλυση Κειμένου")

text_input_label = tk.Label(root, text="Εισάγετε κείμενο:")
text_input_label.pack()

text_input = tk.Text(root, height=10, width=50)
text_input.pack()

process_button = tk.Button(root, text="Ανάλυση Κειμένου", command=process_text_input)
process_button.pack()

file_button = tk.Button(root, text="Φόρτωση από Αρχείο", command=process_text_file)
file_button.pack()

root.mainloop()
