import json

with open('grafana/dashboards/dashboard_principal.json', 'r') as f:
    data = json.load(f)

for panel in data.get('panels', []):
    if panel.get('type') == 'geomap':
        # Change datasource back to Zabbix
        panel['datasource'] = {"type": "alexanderzobnin-zabbix-datasource", "uid": "Zabbix"}
        
        # Change targets
        panel['targets'] = [{
            "datasource": {"type": "alexanderzobnin-zabbix-datasource", "uid": "Zabbix"},
            "group": {"filter": "/.*/"},
            "host": {"filter": "/.*/"},
            "item": {"filter": "/.*/"},
            "queryType": 2,
            "refId": "A",
            "trigger": {"filter": "/.*/"}
        }]

with open('grafana/dashboards/dashboard_principal.json', 'w') as f:
    json.dump(data, f, indent=2)

