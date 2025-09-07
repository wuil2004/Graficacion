import turtle

def koch_half_turtle(t, order, size):
    """
    Dibuja la mitad de un copo de nieve de Koch usando turtle.
    """
    if order == 0:
        t.forward(size)
    else:
        # Divide el tamaño para la siguiente iteración
        new_size = size / 3.0
        
        # Dibuja los 4 segmentos de la curva
        koch_half_turtle(t, order - 1, new_size)
        t.left(60)
        koch_half_turtle(t, order - 1, new_size)
        t.right(120)
        koch_half_turtle(t, order - 1, new_size)
        t.left(60)
        koch_half_turtle(t, order - 1, new_size)

# --- Configuración y ejecución ---
# Configuración de la ventana
screen = turtle.Screen()
screen.bgcolor("white")
screen.title("Mitad del Copo de Nieve de Koch")

# Creación de la tortuga
t = turtle.Turtle()
t.color("blue")
t.speed(0)  # La velocidad más rápida

# Posicionar la tortuga para que el dibujo quede centrado
t.penup()
t.goto(-200, 0)
t.pendown()

# Nivel de detalle del fractal
order = 4 
# Tamaño inicial de la línea
size = 400

# ¡Dibujar!
koch_half_turtle(t, order, size)

# Finalizar
t.hideturtle()
screen.mainloop()