import requests

def obtener_tasa_bcv():
    
    tasa_por_defecto = 766.86 
    
    try:
        
        respuesta = requests.get("https://ve.dolarapi.com/v1/dolares/oficial", timeout=5)
        
        if respuesta.status_code == 200: #codigo de exitoso
            datos = respuesta.json() # Convertimos la respuesta en un diccionario de Python
            return float(datos['promedio']) # Extraemos el valor numérico
        else:
            return tasa_por_defecto
            
    except Exception as e:
        # 4. Si ocurre cualquier error (Sin internet, error de servidor, etc.)
        print(f"Aviso: Usando tasa por defecto debido a: {e}")
        return tasa_por_defecto



def validar_reserva(num_jugadores):
    if num_jugadores >= 10:
        return True # si puede continuar
    else:
        return False # no puede, te faltan jugadores

def calcular_precio_bs(precio_usd, tasa):
    return precio_usd * tasa