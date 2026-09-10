# Bitácora del Proyecto: Monitor de Enlaces (Zabbix + Grafana)

## Estado Actual (Cierre de Sesión)
**Componentes Activos:**
- **Zabbix 7.0** (Server + Web + PostgreSQL)
- **Grafana 10.4.5** (Fijado en esta versión para mayor estabilidad)
- **Plugin AlexanderZobnin-Zabbix:** Fijado en versión `4.6.1` (Evita errores de incompatibilidad de React y `dateMath`).

**Hitos Alcanzados Hoy:**
1. **Migración a SNMP:** El script `importar_hosts.py` fue reescrito para utilizar la interfaz SNMP v2c (Comunidad `PJCH`) y asignar automáticamente la plantilla "Generic by SNMP", permitiendo el auto-descubrimiento de todos los puertos físicos.
2. **Mapa de Grafana (Geomap):** 
   - Se configuró un proveedor XYZ gratuito (`tile.openstreetmap.org`) para erradicar el error de *API Key Required*.
   - Se demostró que la consulta SQL directa a PostgreSQL funciona renderizando los equipos en coordenadas fijas, aislando el problema de que el "Inventory Mode" de Zabbix 7.0 no estaba poblado.
3. **Rack Virtual de Switches:** Se eliminó la clásica tabla aburrida y se implementó un sistema de Filas Repetitivas (Repeating Rows). Ahora el Dashboard arma dinámicamente el panel frontal de cada dispositivo, dibujando sus bocas (ej. `ether1`, `port2`) en cuadraditos verdes/rojos que simulan el equipo físico.

## Pendientes para Mañana:
1. **Confirmación Visual:** Validar que la cuadrícula de puertos (Rack Virtual) se haya renderizado correctamente y los filtros Regex hayan limpiado los nombres de las bocas.
2. **Geolocalización Real:** Una vez que actualices las coordenadas de los equipos en Zabbix mediante *Mass update -> Inventory (Manual)*, modificaremos la consulta SQL del mapa para que deje de usar la coordenada estática de Resistencia y vuelva a leer la posición única de cada equipo.
3. **Ajustes Finos:** Revisar si hay falsos positivos o agregar alertas personalizadas.
