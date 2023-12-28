from math import radians, cos, sin, asin, sqrt
from shapely.geometry import Point

def compute_haversine(lon1, lat1, lon2, lat2, conv=1):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r * conv

def haversine(*args, unidad="km"):
    conv = 1 if unidad == "km" else 1 / 1.852

    if len(args) == 2 and all(isinstance(arg, (Point, list, tuple)) for arg in args):
        points = args
    elif len(args) == 4 and all(isinstance(arg, (int, float)) for arg in args):
        points = [(args[0], args[1]), (args[2], args[3])]
    else:
        raise ValueError("Los argumentos deben ser dos puntos de Shapely, dos listas/tuplas de coordenadas, o cuatro números individuales de longitud y latitud")

    def extract_coordinates(p):
        if isinstance(p, Point):
            return p.x, p.y
        elif isinstance(p, list) or isinstance(p, tuple):
            return p
        else:
            raise ValueError("El punto debe ser de tipo shapely.geometry.Point o una lista/tupla [lon, lat]")

    lon1, lat1 = extract_coordinates(points[0])
    lon2, lat2 = extract_coordinates(points[1])

    return compute_haversine(lon1, lat1, lon2, lat2, conv)

    
def distancia_linea(punto, linestring, unidad="km"):
    punto_cercano = linestring.interpolate(linestring.project(punto))

    return haversine(
        punto, 
        punto_cercano,
        unidad=unidad
    )