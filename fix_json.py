import json

with open('grafana/dashboards/dashboard_principal.json', 'r') as f:
    data = json.load(f)

for panel in data.get('panels', []):
    if panel.get('type') == 'geomap':
        # Change datasource to Postgres
        panel['datasource'] = {"type": "postgres", "uid": "Zabbix_DB"}
        
        # Change targets
        panel['targets'] = [{
            "datasource": {"type": "postgres", "uid": "Zabbix_DB"},
            "format": "table",
            "rawQuery": True,
            "rawSql": "SELECT h.name as host, COALESCE(NULLIF(hi.location_lat, ''), '-27.4833') as latitude, COALESCE(NULLIF(hi.location_lon, ''), '-58.9333') as longitude, COALESCE(MAX(t.priority), 0) as severity FROM hosts h LEFT JOIN host_inventory hi ON h.hostid = hi.hostid LEFT JOIN items i ON h.hostid = i.hostid LEFT JOIN functions f ON i.itemid = f.itemid LEFT JOIN triggers t ON f.triggerid = t.triggerid AND t.value = 1 AND t.status = 0 WHERE h.status = 0 GROUP BY h.name, hi.location_lat, hi.location_lon;",
            "refId": "A"
        }]
        
        # Fix field mapping for colors in geomap
        try:
            panel['options']['layers'][0]['config']['style']['color']['field'] = 'severity'
        except KeyError:
            pass
            
with open('grafana/dashboards/dashboard_principal.json', 'w') as f:
    json.dump(data, f, indent=2)

