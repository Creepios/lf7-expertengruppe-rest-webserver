- [Curl Befehle für die API](#curl-befehle-für-die-api)
   * [Warum curl für APIs?](#warum-curl-für-apis)
   * [Information](#information)
   * [GET](#get)
   * [POST](#post)
   * [PUT](#put)
   * [DELETE](#delete)

<!-- TOC end -->

<!-- TOC --><a name="curl-befehle-für-die-api"></a>
# Curl Befehle für die API

curl ist ein leistungsstarkes Kommandozeilen-Tool, das zum Übertragen von Daten über verschiedene Netzwerkprotokolle eingesetzt wird.

<!-- TOC --><a name="warum-curl-für-apis"></a>
## Warum curl für APIs?

- Einfachheit: Mit wenigen Befehlen können komplexe API-Aufrufe ausgeführt werden.
- Flexibilität: curl unterstützt eine Vielzahl von HTTP-Methoden (GET, POST, PUT, DELETE) und ermöglicht die Übermittlung verschiedener Datenformate (JSON, XML, Form-Data).
- Debugging: curl ist ein unverzichtbares Werkzeug, um API-Anfragen zu testen und Fehler zu beheben.
- Automatisierung: curl kann in Skripten integriert werden, um automatisierte Aufgaben auszuführen, wie z.B. das regelmäßige Abrufen von Daten oder das Ausführen von Batch-Updates.

<!-- TOC --><a name="Informationen"></a>
## Information

In dieser Darstellung wird die IP `172.20.181.253:5001` genutzt.
Diese ist von Pi zu Pi unterschiedlich.

<!-- TOC --><a name="get"></a>
## GET

**GET-Anfragen**: Holen von Daten von einer API, z.B. um Informationen über einen Benutzer oder ein Produkt abzurufen

```bash
curl -X GET http://172.20.181.253:5001/read
curl -X GET http://172.20.181.253:5001/last
```

<!-- TOC --><a name="post"></a>
## POST

**POST-Anfragen**: Senden von Daten an eine API, z.B. um einen neuen Benutzer zu erstellen oder eine Bestellung aufzugeben

```bash
curl -X POST -H "Content-Type: application/json" -d '{"value": 40}' http://172.20.181.112:5001/create
```

<!-- TOC --><a name="put"></a>
## PUT

**PUT-Anfragen**: Aktualisieren bestehender Daten in einer API

```bash
curl -X PUT -H "Content-Type: application/json" -d '{"key": "Tue Aug 20 11:40:29 2024", "value": 70}' http://172.20.181.253:5001/update
```

<!-- TOC --><a name="delete"></a>
## DELETE

**DELETE-Anfragen**: Löschen von Daten aus einer API

```bash
curl -X DELETE http://172.20.181.253:5001/delete
curl -X DELETE http://172.20.181.253:5001/delete?n=1
```
