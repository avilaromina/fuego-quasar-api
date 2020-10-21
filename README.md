# Operación Fuego de Quasar

Han Solo ha sido recientemente nombrado General de la Alianza
Rebelde y busca dar un gran golpe contra el Imperio Galáctico para
reavivar la llama de la resistencia. El servicio de inteligencia rebelde ha detectado un llamado de auxilio de
una nave portacarga imperial a la deriva en un campo de asteroides. El
manifiesto de la nave es ultra clasificado, pero se rumorea que
transporta raciones y armamento para una legión entera.

**Desafio:** Como jefe de comunicaciones rebelde, tu misión es crear un programa en Golang que retorne
la fuente y contenido del mensaje de auxilio. Para esto, cuentas con tres satélites que te
permitirán triangular la posición, ¡pero cuidado! el mensaje puede no llegar completo a cada
satélite debido al campo de asteroides frente a la nave.


## API:

* /api/transmission/topsecret/  
  http://127.0.0.1:8000/api/transmission/topsecret/

  * Tipo: POST
  * Respuesta para **mensaje y coordenadas correctas: 200 (OK)**
  * Respuesta para **mensaje incompleto: 400 (Bad request)**
  * Respuesta para **coordenada incalculable: 400 (Bad request)**
  * Acciones: analiza tanto las distancias para calcular las coordenadas del emisor con el metodo GetLocation , como los arrays recibidos para calcular el mensaje con el metodo GetMessage.
  * Formato esperado (JSON): Objeto que contiene un Array de diccionarios por satelite cuyas keys son el nombre, la distancia del mismo hacia el emisor y un array de strings que se corresponde con el mensaje recibido.

    Ej mensaje y coordenada correctas:
    ```json
    {
      "position":{
          "x":-100.0,
          "y":75.5
      },
      "message":"este es un mensaje secreto"
    }
    ```
  
  * Ejemplos
    ```json
    POST /api/transmission/topsecret/ (VALID RESPONSE)
    {
      "satellites":[
        {
          "name":"kenobi",
          "distance":838.08,
          "message":["", "May", "", "", "be", "", "you"]
        },
        {
          "name":"skywalker",
          "distance":311.1,
          "message":["", "", "", "", "", "the", "", "", "", "you"]
        },
        {
          "name":"sato",
          "distance":259.2,
          "message":["", "", "", "the", "force", "", "with", ""]
        }
      ]
    }
    
    POST /api/transmission/topsecret/ (VALID RESPONSE)
    {
      "satellites":[
        {
          "name":"kenobi",
          "distance":515.39,
          "message":["", "have", "a", "", "feeling", "", "this"]
        },
        {
          "name":"skywalker",
          "distance":406.97,
          "message":["", "", "", "", "have", "", "bad", "", "about", ""]
        },
        {
          "name":"sato",
          "distance":682.37,
          "message":[ "", "I", "", "a", "bad", "", "about", "this"]
        }
      ]
    }

    POST /api/transmission/topsecret/ (INVALID RESPONSE)
    {
      "satellites":[
        {
          "name":"kenobi",
          "distance":100.0,
          "message":["este", "", "", "mensaje", ""]
        },
        {
          "name":"skywalker",
          "distance":115.5,
          "message":["", "es", "", "", "secreto"]
        },
        {
          "name":"sato",
          "distance":142.7,
          "message":["este", "", "un", "", ""]
        }
    ]
    }
    ```

* /api/transmission/topsecret_split/{name}  
  http://127.0.0.1:8000/api/transmission/topsecret_split/kenobi

  * Tipo: POST
  * Respuesta para **mensaje y distancia en formato correcto: 200 OK**
  * Acciones: almacena temporalmente la informacion obtenida del satelite indicado en la url.
  * Formato esperado (JSON): Objeto con la informacion correspondiente al satelite: nombre, distancia y mensaje.

    Ej mensaje y coordenada correctas:
    ```json
    {
      "name": "kenobi"
      "distance": 100,
      "message": ["", "es", "", "mensaje", "secreto"]
    }
    ```
  * Ejemplos para testear el endpoint
    ```json
    POST /api/transmission/topsecret_split/kenobi
    {
      "distance":838.08,
      "message":["", "May", "", "", "be", "", "you"]
    }

    POST /api/transmission/topsecret_split/skywalker
    {
      "distance":311.1,
      "message":["", "", "", "", "", "the", "", "", "", "you"]
    }

    POST /api/transmission/topsecret_split/sato
    {
      "distance":259.2,
      "message":["", "", "", "the", "force", "", "with", ""]
    }
    ```

  * Tipo: GET
  * Respuesta para **mensaje y coordenadas correctas: 200 (OK)**
  * Respuesta para **mensaje incompleto: 400 (Bad request)**
  * Respuesta para **coordenada incalculable: 400 (Bad request)**
  * Acciones: analiza los valores almacenados temporalmente con el metodo POST del mismo endpoint y realiza la misma logica del endpoint topsecret para calcular la coordenada.
  * Formato esperado (JSON): Objeto con la informacion correspondiente al satelite: nombre, distancia y mensaje.

    Ej mensaje y coordenada correctas:
    ```json
    {
      "name": "kenobi"
      "position":{
          "x":-100,
          "y":75
      },
      "message": ["", "es", "", "mensaje", "secreto"]
    }
    ```


## Como correrlo en un entorno local

1. Instalar python 3.7 
2. Instalar docker
3. clonar el repositorio
    ```
    git clone https://github.com/avilaromina/fuego-quasar-api.git
    ```
4. Para levantar el projecto ejecutar 
    ```
    docker-compose up
    ```
5. Acceder a las siguientes urls, para los endpoints  
    http://127.0.0.1:8000/api/transmission/topsecret/  
    http://127.0.0.1:8000/api/transmission/topsecret_split/kenobi


### Autor
Romina Avila Luque
* [mail](mailto:romina.avila.luque@outlook.com)
* [linkedin](https://www.linkedin.com/in/rominic29/)

---

## Extras

* [Documento](https://docs.google.com/document/d/18sxlvXxaQc1GLLNtY6dm4C6sjxhZULyC9Id9vvzMrgM/edit?usp=sharing) con el detalle de las decisiones tomadas en cada momento del proceso del desarrolo de este ejercicio.
* [Planilla](https://docs.google.com/spreadsheets/d/1Co_eCKnmSDfRzUgrIYautIs_SNLvGRytnTDhCUDGmYQ/edit?usp=sharing) para calcular los valores a utilizar en las llamadas a la API.
