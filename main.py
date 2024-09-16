import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
import csv
from fpdf import FPDF

# Ana Pencereyi oluştur
root = tk.Tk()
root.title("Data Entry and Visualization Dashboard")
root.geometry("400x400")

# Tema stili ekleme
style = ttk.Style()
style.theme_use('clam')  # Tema uygulanıyor

# Gelir Girişi
label_income = ttk.Label(root, text="Income (in $):")
label_income.pack(pady=5)
entry_income = ttk.Entry(root)
entry_income.pack(pady=5)

# Gider Girişi
label_expense = ttk.Label(root, text="Expenses (in $):")
label_expense.pack(pady=5)
entry_expense = ttk.Entry(root)
entry_expense.pack(pady=5)

# Satış Girişi
label_sales = ttk.Label(root, text="Monthly Sales (Units):")
label_sales.pack(pady=5)
entry_sales = ttk.Entry(root)
entry_sales.pack(pady=5)

# Verileri CSV ve PDF'ye Kaydetme
def save_data(income, expense, sales):
    # CSV'ye Kaydet
    with open('financial_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([income, expense, sales])

def save_pdf(income, expense, profit):
    # Dosya kaydetme penceresi
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title="Save PDF as")
    if file_path:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Financial Report", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Income: ${income}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Expenses: ${expense}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Profit: ${profit}", ln=True, align='L')
        pdf.output(file_path)
        messagebox.showinfo("Success", f"PDF saved at {file_path}")

# Verileri Al ve Grafik Gösterimi Yap
def show_data():
    try:
        income = float(entry_income.get())
        expense = float(entry_expense.get())
        sales = int(entry_sales.get())

        # Basit bir veri analizi: Kar Hesaplama
        profit = income - expense
        income_expense_ratio = income / expense if expense != 0 else float('inf')  # Gelir-Gider Oranı
        profit_margin = (profit / income) * 100 if income != 0 else 0  # Kar Yüzdesi

        # Verileri Kaydet
        save_data(income, expense, sales)
        save_pdf(income, expense, profit)

        # Grafiksel Gösterim
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))

        # Bar grafiği: Gelir, Gider ve Kar
        axs[0].bar(['Income', 'Expenses', 'Profit'], [income, expense, profit], color=['green', 'red', 'blue'])
        axs[0].set_title('Income, Expenses, and Profit')
        axs[0].set_ylabel('Amount (in $)')

        # Pie chart: Gelirin Kaynakları (örnek veri ile)
        categories = ['Sales', 'Other']
        sales_income = income * 0.8  # Gelirin %80'i satışlardan
        other_income = income * 0.2  # Gelirin %20'si diğer kaynaklardan
        axs[1].pie([sales_income, other_income], labels=categories, autopct='%1.1f%%', colors=['skyblue', 'lightcoral'])
        axs[1].set_title('Income Distribution')

        # Sonuçları ekrana yazdır
        messagebox.showinfo("Analysis Results",
                            f"Income: ${income}\nExpenses: ${expense}\nProfit: ${profit}\n"
                            f"Income-Expense Ratio: {income_expense_ratio:.2f}\nProfit Margin: {profit_margin:.2f}%")

        # Grafik gösterimi
        plt.tight_layout()
        plt.show()

        # Başka işlem yapmak ister misiniz?
        if messagebox.askyesno("Continue", "Would you like to perform another operation?"):
            entry_income.delete(0, tk.END)
            entry_expense.delete(0, tk.END)
            entry_sales.delete(0, tk.END)
        else:
            root.quit()

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers!")

# Gönder Butonu
btn_submit = ttk.Button(root, text="Submit Data & Show Graphs", command=show_data)
btn_submit.pack(pady=10)

# Çıkış Butonu
def exit_app():
    root.quit()

btn_exit = ttk.Button(root, text="Exit", command=exit_app)
btn_exit.pack(pady=10)

root.mainloop()
