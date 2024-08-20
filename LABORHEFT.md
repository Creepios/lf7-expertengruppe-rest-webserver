# Installieren des ReST-Webservers

### Vorbereitung
Installieren der benötigten Basispakete:

```bash
sudo apt install git python3-flask
```

### Installieren des Webservers
Herunterladen der Applikation durch Git (Versionierungssystem):

```bash
git clone https://github.com/Creepios/lf7-expertengruppe-rest-webserver.git
```

### Starten des Webservers
1. In das Verzeichnis des Webservers wechseln.

```bash
cd lf7-expertengruppe-rest-webserver/
```

(TAB kann genutzt werden um den Pfad zu vervollständigen)


2. Starten des Webservers

```bash
python3 webserver.py
```

### Nutzung der API

Wenn der Webserver läuft, können nun auch Daten geschrieben und ausgelesen werden.
Nach dem Starten sollte eine öffentliche IP angezeigt werden. Diese kann für die Aufrufe verwendet werden.

Ein Beispiel für einen solchen Aufruf nutzt den API-Endpunkt `/read`

Der Befehl hierfür lautet: 

```bash
curl -X GET http://172.20.181.112:5001/read
```
Weitere Befehle sind in [Curl_Befehle.md](https://github.com/Creepios/lf7-expertengruppe-rest-webserver/blob/main/Curl_Befehle.md) aufgeführt.

### Stoppen des Webservers
Mit gestartetem Webserver kann man Strg + C drücken um den Webserver zu beenden.
