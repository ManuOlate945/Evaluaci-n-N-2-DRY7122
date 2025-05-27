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
        lat = (json_data["hits"][0]["point"]["lat"])
        lng = (json_data["hits"][0]["point"]["lng"])
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country = ""

        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state = ""

        if len(state) != 0 and len(country) != 0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) != 0:
            new_loc = name + ", " + country
        else:
            new_loc = name

        print("API URL para " + new_loc + " (Location Type: " + value + ")\n" + url)
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Estado de la API: " + str(json_status) + "\nError message: " + json_data["message"])
    return json_status, lat, lng, new_loc

while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfil del vehículo en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    profile = ["car", "bike", "foot"]
    vehicle = input("Ingrese uno de los perfiles de transporte mostrados en la lista anterior: ")
    if vehicle == "quit" or vehicle == "q":
        break
    elif vehicle in profile:
        vehicle = vehicle
    else:
        vehicle = "car"
        print("No se ha ingresado ningún perfil válido. Se usará el perfil car.")

    loc1 = input("Localización de inicio: ")
    if loc1 == "quit" or loc1 == "q":
        break
    orig = geocoding(loc1, key)
    loc2 = input("Destino: ")
    if loc2 == "quit" or loc2 == "q":
        break
    dest = geocoding(loc2, key)
    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print("Estado de la API de enrutamiento: " + str(paths_status) + "\nRouting API URL:\n" + paths_url)
        print("=================================================")
        print("Indicaciones desde " + orig[3] + " hasta " + dest[3] + " mediante " + vehicle)
        print("=================================================")
        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"]) / 1000 / 1.61
            km = (paths_data["paths"][0]["distance"]) / 1000
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            print("Distancia viajada: {0:.1f} millas / {1:.1f} km".format(miles, km))
            print("Duración del viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("=================================================")

            # --- Aquí pedimos el consumo promedio de combustible ---
            consumo_promedio = None
            while consumo_promedio is None:
                try:
                    consumo_promedio = float(input("Ingrese consumo promedio de combustible (litros por 100 km): "))
                    if consumo_promedio <= 0:
                        print("Por favor, ingrese un valor positivo.")
                        consumo_promedio = None
                except ValueError:
                    print("Entrada inválida. Ingrese un número válido.")

            combustible_total = (km * consumo_promedio) / 100
            print(f"Combustible total requerido para el viaje: {combustible_total:.2f} litros")
            print("=================================================")

            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.1f} km / {2:.1f} miles )".format(path, distance / 1000, distance / 1000 / 1.61))
            print("=============================================")
        else:
            print("Mensaje de Error: " + paths_data["message"])
            print("*************************************************")
        
    def input_con_salida(mensaje):
        entrada = input(f"{mensaje} (o 'quit' para salir): ")
        if entrada.lower() == "q":
            print("Saliendo del programa.")
            exit()
        return entrada

