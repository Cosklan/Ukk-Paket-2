import tkinter as tk
from tkinter import messagebox, simpledialog
from reportlab.pdfgen import canvas

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
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
        self.window.title("Zenith Calc (Tekan H untuk masuk history)")

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

        self.converter_windows = {}  # Initialize converter windows

        self.create_menu()

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
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

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
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                            borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def pangkat(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_pangkat_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                            borderwidth=0, command=self.pangkat)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def akar(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_akar_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                            borderwidth=0, command=self.akar)
        button.grid(row=0, column=3, sticky=tk.NSEW)

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
        button = tk.Button(self.buttons_frame, text="=", bg=ORANGE, fg=WHITE, font=DEFAULT_FONT_STYLE,
                            borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
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

    def create_menu(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="History", command=self.show_history)
        file_menu.add_command(label="Exit", command=self.window.quit)

        converter_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Converters", menu=converter_menu)
        converter_menu.add_command(label="Temperature Converter", command=lambda: self.open_converter("Temperature Converter"))
        converter_menu.add_command(label="Length Converter", command=lambda: self.open_converter("Length Converter"))
        converter_menu.add_command(label="Weight Converter", command=lambda: self.open_converter("Weight Converter"))

    def open_converter(self, converter_name):
        if converter_name not in self.converter_windows or not self.converter_windows[converter_name].winfo_exists():
            self.converter_windows[converter_name] = tk.Toplevel(self.window)
            self.converter_windows[converter_name].title(converter_name)
            self.converter_windows[converter_name].geometry("300x250")
            self.converter_windows[converter_name].resizable(0,0)

            if converter_name == "Temperature Converter":
                self.create_temperature_converter(self.converter_windows[converter_name])
            elif converter_name == "Length Converter":
                self.create_length_converter(self.converter_windows[converter_name])
            elif converter_name == "Weight Converter":
                self.create_weight_converter(self.converter_windows[converter_name])
        else:
            self.converter_windows[converter_name].lift()

    def create_temperature_converter(self, window):
        def convert_temperature():
            try:
                value = float(entry.get())
                from_unit = from_var.get()
                to_unit = to_var.get()

                if from_unit == "Celcius" and to_unit == "Farenheit":
                    result = (value * 9/5) + 32
                elif from_unit == "Celcius" and to_unit == "Kelvin":
                    result = value + 273.15
                elif from_unit == "Farenheit" and to_unit == "Celcius":
                    result = (value - 32) * 5/9
                elif from_unit == "Farenheit" and to_unit == "Kelvin":
                    result = (value - 32) * 5/9 + 273.15
                elif from_unit == "Kelvin" and to_unit == "Celcius":
                    result = value - 273.15
                elif from_unit == "Kelvin" and to_unit == "Farenheit":
                    result = (value - 273.15) * 9/5 + 32
                else:
                    result = value

                # Format result without trailing zeros
                result_text = "{:.2f}".format(result).rstrip('0').rstrip('.')
                result_label.config(text=f"Result: {result_text}", fg="blue")
            except ValueError:
                result_label.config(text="Result: Invalid input", fg="red")

        entry = tk.Entry(window, font=("Arial", 12))
        entry.pack(pady=10)

        from_var = tk.StringVar(window)
        from_var.set("Celcius")
        from_menu = tk.OptionMenu(window, from_var, "Celcius", "Farenheit", "Kelvin")
        from_menu.config(font=("Arial", 12))
        from_menu.pack(pady=5)

        to_var = tk.StringVar(window)
        to_var.set("Farenheit")
        to_menu = tk.OptionMenu(window, to_var, "Celcius", "Farenheit", "Kelvin")
        to_menu.config(font=("Arial", 12))
        to_menu.pack(pady=5)

        convert_button = tk.Button(window, text="Convert", command=convert_temperature, font=("Arial", 12), bg="#FF9F0C", fg="white")
        convert_button.pack(pady=5)

        result_label = tk.Label(window, text="Result: ", font=("Arial", 14))
        result_label.pack(pady=10)


    def create_length_converter(self, window):
        def convert_length():
            try:
                value = float(entry.get())
                from_unit = from_var.get()
                to_unit = to_var.get()

                # Length conversion logic
                conversion_factors = {
                    "Meter": {"Centimeter": 100, "Kilometer": 0.001, "Inch": 39.3701, "Miles": 0.000621371,
                            "Foot": 3.28084, "Yards": 1.09361},
                    "Centimeter": {"Meter": 0.01, "Kilometer": 0.00001, "Inch": 0.393701, "Miles": 0.00000621371,
                                "Foot": 0.0328084, "Yards": 0.0109361},
                    "Kilometer": {"Meter": 1000, "Centimeter": 100000, "Inch": 39370.1, "Miles": 0.621371,
                                "Foot": 3280.84, "Yards": 1093.61},
                    "Inch": {"Meter": 0.0254, "Centimeter": 2.54, "Kilometer": 0.0000254, "Miles": 0.000015783,
                            "Foot": 0.0833333, "Yards": 0.0277778},
                    "Miles": {"Meter": 1609.34, "Centimeter": 160934, "Kilometer": 1.60934, "Inch": 63360,
                            "Foot": 5280, "Yards": 1760},
                    "Foot": {"Meter": 0.3048, "Centimeter": 30.48, "Kilometer": 0.0003048, "Inch": 12,
                            "Miles": 0.000189394, "Yards": 0.333333},
                    "Yards": {"Meter": 0.9144, "Centimeter": 91.44, "Kilometer": 0.0009144, "Inch": 36,
                            "Miles": 0.000568182, "Foot": 3}
                }

                if from_unit in conversion_factors and to_unit in conversion_factors[from_unit]:
                    result = value * conversion_factors[from_unit][to_unit]
                else:
                    result = value

                # Format result without trailing zeros
                result_text = "{:.2f}".format(result).rstrip('0').rstrip('.')
                result_text = f"{result_text} {to_unit}"

                result_label.config(text=f"Result: {result_text}", fg="blue")
            except ValueError:
                result_label.config(text="Result: Invalid input", fg="red")

        entry = tk.Entry(window, font=("Arial", 12))
        entry.pack(pady=10)

        from_var = tk.StringVar(window)
        from_var.set("Meter")
        from_menu = tk.OptionMenu(window, from_var, "Meter", "Centimeter", "Kilometer", "Inch", "Miles", "Foot", "Yards")
        from_menu.config(font=("Arial", 12))
        from_menu.pack(pady=5)

        to_var = tk.StringVar(window)
        to_var.set("Centimeter")
        to_menu = tk.OptionMenu(window, to_var, "Meter", "Centimeter", "Kilometer", "Inch", "Miles", "Foot", "Yards")
        to_menu.config(font=("Arial", 12))
        to_menu.pack(pady=5)

        convert_button = tk.Button(window, text="Convert", command=convert_length, font=("Arial", 12), bg="#FF9F0C", fg="white")
        convert_button.pack(pady=5)

        result_label = tk.Label(window, text="Result: ", font=("Arial", 14))
        result_label.pack(pady=10)



    def create_weight_converter(self, window):
        def convert_weight():
            try:
                value = float(entry.get())
                from_unit = from_var.get()
                to_unit = to_var.get()

                # If the same units are selected, result remains the same
                if from_unit == to_unit:
                    result_text = f"{int(value)} {to_unit}"
                    result_label.config(text=f"Result: {result_text}", fg="blue")
                    return

                if from_unit == "Kilogram":
                    if to_unit == "Gram":
                        result = value * 1000
                    elif to_unit == "Pound":
                        result = value * 2.20462
                    elif to_unit == "Ounce":
                        result = value * 35.274
                elif from_unit == "Gram":
                    if to_unit == "Kilogram":
                        result = value / 1000
                    elif to_unit == "Pound":
                        result = value * 0.00220462
                    elif to_unit == "Ounce":
                        result = value * 0.035274
                elif from_unit == "Pound":
                    if to_unit == "Kilogram":
                        result = value * 0.453592
                    elif to_unit == "Gram":
                        result = value * 453.592
                    elif to_unit == "Ounce":
                        result = value * 16
                elif from_unit == "Ounce":
                    if to_unit == "Kilogram":
                        result = value * 0.0283495
                    elif to_unit == "Gram":
                        result = value * 28.3495
                    elif to_unit == "Pound":
                        result = value * 0.0625
                else:
                    result = value

                result_text = f"{result:.0f} {to_unit}" if result.is_integer() else f"{result:.2f} {to_unit}"
                result_label.config(text=f"Result: {result_text}", fg="blue")
            except ValueError:
                result_label.config(text="Result: Invalid input", fg="red")

        entry = tk.Entry(window, font=("Arial", 12))
        entry.pack(pady=10)

        from_var = tk.StringVar(window)
        from_var.set("Kilogram")
        from_menu = tk.OptionMenu(window, from_var, "Kilogram", "Gram", "Pound", "Ounce")
        from_menu.config(font=("Arial", 12))
        from_menu.pack(pady=5)

        to_var = tk.StringVar(window)
        to_var.set("Gram")
        to_menu = tk.OptionMenu(window, to_var, "Kilogram", "Gram", "Pound", "Ounce")
        to_menu.config(font=("Arial", 12))
        to_menu.pack(pady=5)

        convert_button = tk.Button(window, text="Convert Weight", command=convert_weight, font=("Arial", 12), bg="#FF9F0C", fg="white")
        convert_button.pack(pady=5)

        result_label = tk.Label(window, text="Result: ", font=("Arial", 14))
        result_label.pack(pady=10)


if __name__ == "__main__":
    calc = Calculator()
    calc.run()
