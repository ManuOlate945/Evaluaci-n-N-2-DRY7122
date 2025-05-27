import sys
import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "c54c2fd1-b563-40d4-aa90-25638cad2dd7"

def geocoding(location, key):
    while location == "":
        location = input("Ingrese nuevamente la localización: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    replydata = requests.get(url)
    json_status = replydata.status_code
    json_data = replydata.json()

    if json_status == 200 and len(json_data["hits"]) != 0:
        json_data = requests.get(url).json()
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")

        new_loc = f"{name}, {state}, {country}" if state and country else f"{name}, {country}" if country else name

        print(f"API URL para {new_loc} (Location Type: {value})\n{url}")
    else:
        lat, lng, new_loc = "null", "null", location
        if json_status != 200:
            print(f"Estado de la API: {json_status}\nError message: {json_data['message']}")
    return json_status, lat, lng, new_loc

while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfil del vehículo en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    profile = ["car", "bike", "foot"]
    
    vehicle = input("Ingrese uno de los perfiles de transporte mostrados en la lista anterior: ")
    if vehicle.lower() in ["quit", "q"]:
        sys.exit()

    vehicle = vehicle if vehicle in profile else "car"
    if vehicle == "car":
        print("No se ha ingresado ningún perfil válido. Se usará el perfil car.")

    loc1 = input("Localización de inicio: ")
    if loc1.lower() in ["quit", "q"]:
        sys.exit()
    orig = geocoding(loc1, key)

    loc2 = input("Destino: ")
    if loc2.lower() in ["quit", "q"]:
        sys.exit()
    dest = geocoding(loc2, key)

    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op = f"&point={orig[1]}%2C{orig[2]}"
        dp = f"&point={dest[1]}%2C{dest[2]}"
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()

        print(f"Estado de la API de enrutamiento: {paths_status}\nRouting API URL:\n{paths_url}")
        print("=================================================")
        print(f"Indicaciones desde {orig[3]} hasta {dest[3]} mediante {vehicle}")
        print("=================================================")

        if paths_status == 200:
            miles = paths_data["paths"][0]["distance"] / 1000 / 1.61
            km = paths_data["paths"][0]["distance"] / 1000
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)

            print(f"Distancia viajada: {miles:.1f} millas / {km:.1f} km")
            print(f"Duración del viaje: {hr:02d}:{min:02d}:{sec:02d}")
            print("=================================================")
        else:
            print(f"Mensaje de Error: {paths_data['message']}")
            print("*************************************************")

    def input_con_salida(mensaje):
        entrada = input(f"{mensaje} (o 'quit' para salir): ")
        if entrada.lower() == "q":
            print("Saliendo del programa.")
            exit()
        return entrada

