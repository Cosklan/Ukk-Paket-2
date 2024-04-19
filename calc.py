import tkinter as tk
from reportlab.pdfgen import canvas
from tkinter import messagebox
from tkinter import simpledialog


LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
ORANGE = "#FF9F0C"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0, 0)
        self.window.title("Zenith Calc (Tekan H unuk masuk history)")

        icon_path = "ikon.png"
        self.icon = tk.PhotoImage(file=icon_path)
        self.window.iconphoto(True, self.icon)

        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), ".": (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)

        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.history = []
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        self.window.bind("h", self.show_history)
        self.window.bind("<Return>", lambda event: self.evaluate())
        self.window.bind("<H>", lambda event: self.show_history())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def add_to_history(self, operation, result):
        self.history.append((operation, result))

    def show_history(self, event=None):
        if not hasattr(self, 'history_window') or not self.history_window.winfo_exists():
            self.history_window = tk.Toplevel(self.window)
            self.history_window.title("History")
            self.history_window.geometry("400x300")

            history_listbox = tk.Listbox(self.history_window, font=("Arial", 12))
            history_listbox.pack(side="left", fill="both", expand=True)

            scrollbar = tk.Scrollbar(self.history_window, orient="vertical", command=history_listbox.yview)
            scrollbar.pack(side="right", fill="y")

            history_listbox.config(yscrollcommand=scrollbar.set)

            for operation, result in self.history:
                history_listbox.insert("end", f"{operation} = {result}")

            export_button = tk.Button(self.history_window, text="Export to PDF", bg=ORANGE, fg=WHITE, font=SMALL_FONT_STYLE,
                                    borderwidth=0, command=lambda: self.export_to_pdf(history_listbox))
            export_button.pack(side="bottom", fill="both")
        else:
            self.history_window.lift()



    def export_to_pdf(self, history_listbox):
        file_name = simpledialog.askstring("Export", "Masukan nama PDF:")
        if file_name:
            pdf_file = f"{file_name}.pdf"
            c = canvas.Canvas(pdf_file)
            y = 750
            for i in range(history_listbox.size()):
                entry = history_listbox.get(i)
                if entry:
                    c.drawString(50, y, entry)
                    y -= 20

            c.save()

            messagebox.showinfo("PDF Export", "History Disimpan ke {}".format(pdf_file))
            print(f"History disimpan ke {pdf_file}")

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_pangkat_button()
        self.create_akar_button()

    def create_display_labels(self):
        total_label =tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E,bg=LIGHT_GRAY,
                              fg=LABEL_COLOR,padx=24,font=SMALL_FONT_STYLE)
        total_label.pack(expand=True,fill='both')

        label =tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E,bg=LIGHT_GRAY,
                              fg=LABEL_COLOR,padx=24,font=LARGE_FONT_STYLE)
        label.pack(expand=True,fill='both')

        return total_label,label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221,bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame
    
    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()
    
    def create_digit_buttons(self):
        for digit,grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit),bg=WHITE,fg=LABEL_COLOR,font=DIGITS_FONT_STYLE,
                               borderwidth=0,command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0],column=grid_value[1],sticky=tk.NSEW)
        
    def append_operator(self, operator):
        if self.current_expression:  
            if self.current_expression[-1] not in self.operations:
                self.current_expression += operator
                self.total_expression += self.current_expression
                self.current_expression = ""
                self.update_total_label()
                self.update_label()


    
    def create_operator_buttons(self):
        i = 0
        for operator,symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol,bg=OFF_WHITE,fg=LABEL_COLOR,font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i,column=4,sticky=tk.NSEW)
            i += 1
    
    def clear(self):
        self.current_expression =""
        self.total_expression =""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
         button = tk.Button(self.buttons_frame, text="C",bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=self.clear)
         button.grid(row=0,column=1, sticky=tk.NSEW)

    def pangkat(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()
    
    def create_pangkat_button(self):
         button = tk.Button(self.buttons_frame, text="x\u00b2",bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=self.pangkat)
         button.grid(row=0,column=2, sticky=tk.NSEW)

    def akar(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()     
    
    def create_akar_button(self):
         button = tk.Button(self.buttons_frame, text="\u221ax",bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=self.akar)
         button.grid(row=0,column=3, sticky=tk.NSEW)
    

    def evaluate(self):
        operation = self.total_expression + self.current_expression
        try:
            result = str(eval(operation))
            self.add_to_history(operation, result) 
            self.current_expression = result
            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()
            self.update_total_label()



    def create_equals_button(self):
         button = tk.Button(self.buttons_frame, text="=",bg=ORANGE, fg=WHITE, font=DEFAULT_FONT_STYLE,
                               borderwidth=0,command=self.evaluate)
         button.grid(row=4,column=3,columnspan=2, sticky=tk.NSEW)
            

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True,fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator,symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)
    
    
    
    def update_label(self):
        result = self.current_expression[:11]
        try:
            # Try converting the result to float
            result_float = float(result)
            # Check if the float is equivalent to its integer representation
            if result_float == int(result_float):
                # If yes, convert it to integer
                result = str(int(result_float))
            else:
                # If not, keep it as float
                result = str(result_float)
        except ValueError:
            # If conversion to float fails, keep the original result
            pass
        self.label.config(text=result)

    def run(self):
        self.window.mainloop()

if __name__ =="__main__":
    calc = Calculator()
    calc.run()