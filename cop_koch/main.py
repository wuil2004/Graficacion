# main.py

import io
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
import matplotlib.pyplot as plt

# --- Inicialización de la API ---
app = FastAPI(
    title="API del Copo de Nieve de Koch",
    description="Una API para generar las coordenadas o una imagen de la mitad del copo de nieve de Koch.",
)

# --- ENDPOINT PARA SERVIR EL HTML ---
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

# --- Lógica para generar el fractal ---
def koch_snowflake_half(order, scale=10):
    def koch_curve(p1, p2, order):
        if order == 0:
            return [p1, p2]
        x1, y1 = p1
        x2, y2 = p2
        vx = (x2 - x1) / 3.0
        vy = (y2 - y1) / 3.0
        pA = (x1 + vx, y1 + vy)
        pB = (x1 + 2 * vx, y1 + 2 * vy)
        
        # --- FÓRMULA MATEMÁTICA DEFINITIVA (HACIA ABAJO) ---
        # Este método calcula el punto medio de la base (pA a pB) y le suma un vector perpendicular
        mid_x = (pA[0] + pB[0]) / 2
        mid_y = (pA[1] + pB[1]) / 2
        
        # El valor sqrt(3)/2 es aprox 0.866
        px = mid_x - 0.866 * (pA[1] - pB[1])
        py = mid_y - 0.866 * (pB[0] - pA[0])
        p_mid = (px, py)
        # --- FIN DE LA CORRECCIÓN ---
        
        points = []
        points.extend(koch_curve(p1, pA, order - 1))
        points.extend(koch_curve(pA, p_mid, order - 1))
        points.extend(koch_curve(p_mid, pB, order - 1))
        points.extend(koch_curve(pB, p2, order - 1))
        
        final_points = [points[0]]
        for point in points[1:]:
            if point != final_points[-1]:
                final_points.append(point)
        return final_points

    p1_start = (0, 0)
    p2_start = (scale, 0)
    return koch_curve(p1_start, p2_start, order)

# --- Endpoints de la API (sin cambios) ---
@app.get("/koch-curve/coordinates")
def get_koch_coordinates(order: int = 4, scale: float = 100):
    points = koch_snowflake_half(order, scale)
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    return {"order": order, "scale": scale, "x_coordinates": x_coords, "y_coordinates": y_coords}

@app.get("/koch-curve/image")
def get_koch_image(order: int = 4, scale: float = 100):
    points = koch_snowflake_half(order, scale)
    x, y = zip(*points)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x, y, 'b-')
    ax.set_title(f'Mitad del Copo de Nieve de Koch (Orden {order})')
    ax.axis('equal')
    ax.axis('off')
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return StreamingResponse(buf, media_type="image/png")