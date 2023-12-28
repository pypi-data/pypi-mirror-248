from scipy.interpolate import interp1d

def funcion_interpolacion(x, x_nuevos, y):
    f_interpolacion = interp1d(x, y)
    return f_interpolacion(x_nuevos)

def interpolar(
    timestamps,
    y,
    minutos_interpolacion=2.5
):
    timestamps.sort()

    pasos_timestamps = int(minutos_interpolacion*60*1000)
    timestamps_nuevos = range(timestamps[0], timestamps[-1], pasos_timestamps)

    return timestamps_nuevos, funcion_interpolacion(timestamps, timestamps_nuevos, y)

def interpolar_lista(
    timestamps,
    valores,
    minutos_interpolacion=2.5      
):
    timestamps.sort()

    pasos_timestamps = int(minutos_interpolacion*60*1000)
    timestamps_nuevos = range(timestamps[0], timestamps[-1], pasos_timestamps)

    valores_interpolados = [timestamps_nuevos]
    for y in valores:
        valores_interpolados.append(interpolar(timestamps, y, minutos_interpolacion))

    return valores_interpolados