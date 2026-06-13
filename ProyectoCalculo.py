import customtkinter as ctk
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

x = sp.Symbol("x")

app = ctk.CTk()
app.title("Analizador de Límites")
app.geometry("950x850")
app.configure(fg_color="#1E1E1E")

titulo = ctk.CTkLabel(
    app,
    text="Calculadora y Graficadora de Límites",
    font=("Arial", 24, "bold"),
    text_color="#FFFFFF"
)
titulo.pack(pady=15)

frame = ctk.CTkFrame(
    app,
    fg_color="#252526",
    border_width=1,
    border_color="#3C3C3C"
)
frame.pack(pady=10)

entrada_funcion = ctk.CTkEntry(
    frame,
    width=380,
    placeholder_text="Ejemplo: (x^3-8)/(x-2)",
    fg_color="#2D2D30",
    border_color="#555555",
    text_color="white"
)
entrada_funcion.grid(row=0, column=0, padx=10, pady=10)

entrada_h = ctk.CTkEntry(
    frame,
    width=180,
    placeholder_text="Valor h, ejemplo: 2",
    fg_color="#2D2D30",
    border_color="#555555",
    text_color="white"
)
entrada_h.grid(row=0, column=1, padx=10, pady=10)

resultado = ctk.CTkLabel(
    app,
    text="Resultado:",
    font=("Arial", 18),
    text_color="#E0E0E0"
)
resultado.pack(pady=10)

pasos_texto = ctk.CTkTextbox(
    app,
    width=850,
    height=200,
    font=("Consolas", 14),
    fg_color="#202020",
    text_color="#F0F0F0",
    border_width=1,
    border_color="#444444"
)
pasos_texto.pack(pady=10)

figura, ax = plt.subplots(figsize=(6, 3))
figura.patch.set_facecolor("#1E1E1E")
ax.set_facecolor("#252526")
canvas = FigureCanvasTkAgg(figura, master=app)

def calcular():
    try:
        ax.clear()
        ax.set_facecolor("#252526")
        pasos_texto.delete("1.0", "end")

        texto_funcion = entrada_funcion.get()
        texto_h = entrada_h.get()

        if texto_funcion == "" or texto_h == "":
            resultado.configure(text="Error: debes ingresar una función y un valor h")
            return

        texto_funcion = texto_funcion.replace("^", "**")

        funcion = sp.sympify(texto_funcion)
        h = sp.sympify(texto_h)

        numerador, denominador = sp.fraction(funcion)

        num_sust = numerador.subs(x, h)
        den_sust = denominador.subs(x, h)

        pasos = ""
        pasos += "RESOLUCIÓN PASO A PASO\n\n"

        pasos += "1) Escribimos el límite:\n"
        pasos += f"lim x→{h} {funcion}\n\n"

        pasos += "2) Sustituimos x por el valor:\n"
        pasos += f"({numerador}) / ({denominador})\n"
        pasos += f"({num_sust}) / ({den_sust})\n\n"

        if den_sust == 0 and num_sust == 0:
            pasos += "3) Obtenemos:\n"
            pasos += "0/0\n\n"
            pasos += "Esto es una indeterminación, por eso debemos simplificar.\n\n"

            num_factorizado = sp.factor(numerador)
            den_factorizado = sp.factor(denominador)

            pasos += "4) Factorizamos numerador y denominador:\n"
            pasos += f"{numerador} = {num_factorizado}\n"
            pasos += f"{denominador} = {den_factorizado}\n\n"

            pasos += "5) Reescribimos la fracción:\n"
            pasos += f"({num_factorizado}) / ({den_factorizado})\n\n"

            simplificada = sp.cancel(funcion)

            pasos += "6) Cancelamos factores iguales:\n"
            pasos += f"{simplificada}\n\n"

            pasos += "7) Sustituimos nuevamente x por el valor:\n"
            nuevo = simplificada.subs(x, h)
            pasos += f"{simplificada}\n"
            pasos += f"x = {h}\n"
            pasos += f"Resultado: {nuevo}\n\n"

        elif den_sust == 0:
            pasos += "3) El denominador queda 0.\n"
            pasos += "La función no está definida en ese punto.\n\n"

        else:
            pasos += "3) Como no aparece indeterminación, resolvemos directo:\n"
            pasos += f"{num_sust} / {den_sust} = {sp.simplify(num_sust / den_sust)}\n\n"

        limite = sp.limit(funcion, x, h)

        pasos += "RESPUESTA FINAL:\n"
        pasos += f"El límite es {limite}"

        pasos_texto.insert("end", pasos)
        resultado.configure(text=f"Resultado: {limite}")

        f = sp.lambdify(x, funcion, "math")

        valores_x = []
        valores_y = []

        inicio = float(h) - 5
        fin = float(h) + 5
        pasos_grafico = 200
        salto = (fin - inicio) / pasos_grafico

        i = 0
        while i <= pasos_grafico:
            valor_x = inicio + i * salto

            try:
                valor_y = f(valor_x)

                if valor_y < 1000 and valor_y > -1000:
                    valores_x.append(valor_x)
                    valores_y.append(valor_y)
            except:
                pass

            i += 1

        ax.plot(valores_x, valores_y, color="white")
        ax.axvline(float(h), linestyle="--", color="#BBBBBB")
        ax.set_title("Gráfica de la función")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True, color="#444444")

        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.title.set_color("white")

        for spine in ax.spines.values():
            spine.set_color("white")

        canvas.draw()

    except:
        resultado.configure(text="Error: función o valor h inválido")
        pasos_texto.delete("1.0", "end")
        pasos_texto.insert("end", "Ejemplo correcto:\nFunción: (x^3-8)/(x-2)\nValor h: 2")

boton = ctk.CTkButton(
    app,
    text="Calcular límite y graficar",
    command=calcular,
    width=250,
    height=40,
    fg_color="#3A3A3A",
    hover_color="#4A4A4A",
    text_color="white",
    corner_radius=8
)
boton.pack(pady=10)

canvas.get_tk_widget().pack(pady=10)

app.mainloop()