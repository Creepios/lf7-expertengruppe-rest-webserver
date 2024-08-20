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

### Stoppen des Webservers
Mit gestartetem Webserver kann man Strg + C drücken um den Webserver zu beenden.
