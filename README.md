# Net Monitor Stack

Proyecto de monitoreo de red basado en contenedores para desplegar **Zabbix 7.0 LTS** (backend y GUI) y **Grafana 11** (visualización) integrados automáticamente.

## Despliegue

Para desplegar el entorno, ejecuta:
```bash
docker compose up -d
```

- **Grafana**: http://localhost:3000 (admin / admin)
- **Zabbix Web**: http://localhost:8080 (Admin / zabbix)

Licencia: Apache 2.0
