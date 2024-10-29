# lumu-backend-test

Este proyecto incluye dos ejercicios: un seguimiento de direcciones IP utilizando Kafka y una función de análisis de marcas de tiempo. A continuación se describen las instrucciones para ejecutar estas soluciones.

## Requisitos
- Python 3.12
- Docker

## Instalación

1. **Clona el repositorio:**

   ```bash
   git clone git@github.com:JhonSoto99/lumu-backend-test.git
   cd lumu-backend-test

2. **Crea un entorno virtual (opcional, pero recomendado), se recomienda usar la versión Python 3.12:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa: venv\Scripts\activate

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt

# Ejercicio 1: Timestamp Parsing Function
El **Timestamp Analyzer** es una herramienta en Python que permite analizar y convertir diversas representaciones de marcas de tiempo (timestamps) en formato UNIX y en formato ISO 8601. Puede manejar timestamps como enteros, flotantes y cadenas, y los convierte a un formato ISO 8601 con precisión de milisegundos, utilizando la zona horaria UTC.

## Uso

Para utilizar la herramienta, simplemente ejecuta el script en Python.
### Ejemplo

```bash
$ cd app/ 
$ python -m timestamp.timestamp_parsing_function
```

# Ejercicio 2:  Unique IP Tracker

### Descripción
Este ejercicio consiste en una aplicación de seguimiento de direcciones IP que utiliza Kafka para el procesamiento de mensajes. Además sirve el conteo de IPs únicas en una API desarrollada con el framework FastAPI. 

### Uso

1. **Levantar el contenedor Docker con está el servicio Kafka:**
```bash
$ # en la raíz del proyecto
$ sudo docker-compose up -d
```

2. **Ejecutar el productor de mensajes que se comunica con Kafka:**
```bash
$ cd app/
$ python -m ip_tracker.producer
```

3. **Ejecutar el consumidor de mensajes que se comunica con Kafka:**
```bash
$ cd app/
$ python -m ip_tracker.consumer
```
Este comando disponibiliza una api a la cual se puede acceder a la documentación Swagger OpenApi:
http://0.0.0.0:8000/api/docs/, desde esta documentación se puede consumir la api de manera interactiva.

también es posible llamar la API derectamente: http://0.0.0.0:8000/api/v1/unique_ip_count



## Tests

Para ejecutar los tests:
```bash
$ cd app/ 
$ python -m unittest discover -s tests
```


## Resumen de la Implementación

**Parte 1**: Función de Análisis de Tiempos La función que se desarrolló para analizar los timestamps recibe un valor
que puede ser una cadena o un número, y lo convierte a un formato UTC estándar.
Para lograr esto, se realizan las siguientes comprobaciones:

1. **Formato ISO 8601**: Se valida si el timestamp está en un formato ISO 8601 y se ajusta para incluir la "Z" al final si no está presente.
###**Timestamp Unix**: Si el valor es un número, se determina si está en segundos o milisegundos y se convierte a un formato ISO 8601 correspondiente.
2. **Errores de conversión**: Se manejan excepciones para asegurarse de que cualquier valor no válido se gestione adecuadamente, devolviendo un mensaje de error claro.

A medida que la cantidad de mensajes de dispositivos aumenta, el procesamiento de timestamps puede volverse un cuello de botella.
En este caso se podría considerar implementar un sistema de procesamiento en varios hilos o procesos para que estos se encargen de analizar timestamps de manera simultánea,
esto puede mejorar la eficencia y reducir tiempos de respuesta.

**Parte 2**: Rastreador de IP Únicas para rastrear direcciones IP únicas de mensajes recibidos de un tema de Kafka,
Este sistema incluye dos componentes principales: un consumidor que recibe mensajes de Kafka y un productor que genera y envía mensajes a un tema de Kafka.

Se implementó un endpoint API REST para exponer el conteo global de direcciones IP únicas.

A medida que la cantidad de mensajes aumenta, puede considerarse aumentar el número de particiones en el tema de Kafka para distribuir la carga de trabajo.
También se puede optimizar la configuración del consumidor y productor, aumentando el tamaño del lote o ajustando la configuración de tiempo de espera.

