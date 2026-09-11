sed -i '' 's/GF_INSTALL_PLUGINS=alexanderzobnin-zabbix-app 4.6.1/GF_INSTALL_PLUGINS=alexanderzobnin-zabbix-app 4.6.1,marcusolsson-network-graph-panel/g' docker-compose.yml
sed -i '' 's/alexanderzobnin-zabbix-problems-panel/alexanderzobnin-zabbix-triggers-panel/g' grafana/dashboards/dashboard_principal.json
