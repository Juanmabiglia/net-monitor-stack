# Instructivo: Carga de Dispositivos (Hosts) en Zabbix

Para que los equipos de red (routers, switches, antenas, etc.) sean monitoreados por Zabbix y **aparezcan correctamente ubicados en el mapa de Grafana**, debes seguir estos pasos:

## 1. Acceder a Zabbix
- Ingresa a la interfaz web de Zabbix: `http://<IP-DEL-SERVIDOR>:8080`
- Usuario por defecto: `Admin`
- Contraseña: `zabbix`

## 2. Crear un nuevo Host (Dispositivo)
1. En el menú lateral izquierdo, ve a **Data collection** (Recopilación de datos) -> **Hosts**.
2. Haz clic en el botón superior derecho **Create host** (Crear equipo).

## 3. Configurar los Datos Principales (Pestaña "Host")
- **Host name:** El nombre identificatorio del equipo (ej. `Router-Principal-Barranqueras`).
- **Templates:** Selecciona una plantilla según el tipo de monitoreo. Para un monitoreo básico de si el equipo está encendido o apagado, busca y selecciona `ICMP Ping`.
- **Host groups:** Agrupa el equipo (ej. puedes crear un grupo llamado `Enlaces` o `Nodos`).
- **Interfaces:** Haz clic en *Add* y selecciona la interfaz adecuada (por ejemplo `Agent` o `SNMP`). Coloca la **Dirección IP** del equipo a monitorear.

## 4. Configurar las Coordenadas para el Mapa (Pestaña "Inventory")
¡Este paso es **crítico** para que el dispositivo aparezca en el mapa de Grafana!
1. Cambia la pestaña superior a **Inventory** (Inventario).
2. Cambia el *Inventory mode* (Modo de inventario) de *Disabled* a **Manual**.
3. Baja hasta encontrar los campos de ubicación:
   - **Location latitude** (Latitud de ubicación): Ingresa la latitud (ej. `-27.4833`).
   - **Location longitude** (Longitud de ubicación): Ingresa la longitud (ej. `-58.9333`).

## 5. Guardar
Haz clic en el botón **Add** (Añadir) en la parte inferior para guardar el dispositivo.

---

### ¿Cómo funciona la integración con el Mapa en Grafana?
El mapa en Grafana (`Geomap`) lee los "Problemas" (Triggers activos) que detecta Zabbix.
Si un equipo pierde conexión (ej. falla el Ping), Zabbix genera una alerta. Grafana lee esa alerta, busca las coordenadas en el *Inventario* del host y dibuja un marcador en el mapa. 
- **Verde:** Funcionamiento normal (el equipo está en el mapa, si el panel está configurado para mostrar nodos sanos).
- **Naranja:** Alerta de nivel *Warning* o *Average*.
- **Rojo:** Alerta de nivel *High* o *Disaster* (Ej. equipo caído por completo).
