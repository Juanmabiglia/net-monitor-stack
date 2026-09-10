#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
import sys

ZABBIX_URL = "http://localhost:8080/api_jsonrpc.php"
USER = "Admin"
PASSWORD = "zabbix"

# Coordenadas por defecto para el mapa (Resistencia/Barranqueras)
LATITUDE = "-27.4833"
LONGITUDE = "-58.9333"

HOSTS = [
    {"name": "MikroTik #1", "ip": "10.0.0.1"},
    {"name": "MikroTik #2", "ip": "10.150.1.1"},
    {"name": "MikroTik #3", "ip": "10.23.0.254"},
    {"name": "Aruba 8360 #1 (core)", "ip": "10.30.9.251"},
    {"name": "Aruba 8360 #2 (core)", "ip": "10.30.9.252"},
    {"name": "Aruba 6100/6200 #1", "ip": "10.30.9.3"},
    {"name": "Aruba 6100/6200 #2", "ip": "10.30.9.4"},
    {"name": "Aruba 6100/6200 #3", "ip": "10.30.9.5"},
    {"name": "Aruba 6100/6200 #4", "ip": "10.30.9.7"},
    {"name": "Aruba 6100/6200 #5", "ip": "10.30.9.9"},
    {"name": "Aruba 6100/6200 #6", "ip": "10.30.9.11"},
    {"name": "Aruba 6100/6200 #8", "ip": "10.30.9.12"},
    {"name": "Aruba 6100/6200 #9", "ip": "10.30.9.20"},
    {"name": "Aruba 6100/6200 #10 (12.1)", "ip": "192.168.12.1"},
    {"name": "Aruba 6100/6200 #10 (12.2)", "ip": "192.168.12.2"},
    {"name": "Aruba 6100/6200 #10 (12.6)", "ip": "192.168.12.6"},
    {"name": "HPE 1920/1930 #1", "ip": "10.0.10.5"},
    {"name": "HPE 1920/1930 #2", "ip": "10.0.20.1"},
    {"name": "Allied Telesis AT-SB4211", "ip": "10.0.0.251"}
]

request_id = 1

def zabbix_api(method, params, auth=None):
    global request_id
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": request_id
    }
    if auth:
        payload["auth"] = auth
    request_id += 1
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(ZABBIX_URL, data=data, headers={'Content-Type': 'application/json-rpc'})
    
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode('utf-8'))
        if "error" in result:
            print(f"Error Zabbix API ({method}): {result['error']['data']}")
            sys.exit(1)
        return result["result"]
    except Exception as e:
        print(f"Error de conexion HTTP: {e}")
        sys.exit(1)

def main():
    print("Autenticando en Zabbix...")
    token = zabbix_api("user.login", {"username": USER, "password": PASSWORD})
    print("Token obtenido con exito.")

    # 1. Obtener ID del Host Group "Templates/Network devices" o "Network devices"
    # Vamos a crear un grupo custom llamado "Enlaces de Red"
    print("Buscando o creando grupo de Hosts 'Enlaces de Red'...")
    groups = zabbix_api("hostgroup.get", {"filter": {"name": ["Enlaces de Red"]}}, token)
    if groups:
        group_id = groups[0]["groupid"]
    else:
        new_group = zabbix_api("hostgroup.create", {"name": "Enlaces de Red"}, token)
        group_id = new_group["groupids"][0]

    # 2. Obtener el ID del Template "Generic by SNMP"
    print("Buscando Template 'Generic by SNMP'...")
    templates = zabbix_api("template.get", {"filter": {"host": ["Generic by SNMP"]}}, token)
    if not templates:
        print("No se encontró el template 'Generic by SNMP'. Abortando.")
        sys.exit(1)
    template_id = templates[0]["templateid"]

    # 3. Crear Hosts
    for h in HOSTS:
        # El campo "host" (nombre tecnico) no permite caracteres especiales como # o ().
        tech_name = h['name'].replace('#', '').replace('(', '').replace(')', '').replace('/', '-').strip()
        
        print(f"Creando host {h['name']} ({h['ip']})...")
        host_params = {
            "host": tech_name,
            "name": h['name'],
            "interfaces": [
                {
                    "type": 2, # 2=SNMP
                    "main": 1,
                    "useip": 1,
                    "ip": h['ip'],
                    "dns": "",
                    "port": "161",
                    "details": {
                        "version": 2,
                        "community": "PJCH"
                    }
                }
            ],
            "groups": [{"groupid": group_id}],
            "templates": [{"templateid": template_id}],
            "inventory_mode": 0, # 0 = Manual
            "inventory": {
                "location_lat": LATITUDE,
                "location_lon": LONGITUDE
            }
        }
        
        # Comprobar si ya existe
        exists = zabbix_api("host.get", {"filter": {"host": [tech_name]}}, token)
        if exists:
            print(f"  -> El host {h['name']} ya existe. Omitiendo.")
            continue
            
        zabbix_api("host.create", host_params, token)
        print("  -> Creado exitosamente.")

    print("\nProceso finalizado. Todos los equipos fueron cargados en Zabbix.")

if __name__ == "__main__":
    main()
