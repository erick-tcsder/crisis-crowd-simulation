# Crisis Crowd Simulation for Building Evacuation.

## Integrantes:
- Erick A. Fonseca Pérez - **C312**   [@erick-tcsder](https://github.com/erick-tcsder)
- Deborah Famadas Rodríguez - **C312** [@dbyta](https://github.com/deborahfam)
- Gabriel Hernández Rodríguez - **C311** [@sour6ce](https://github.com/sour6ce)

## Descripción General:
Se nos plantea el siguiente problema. Supongamos que tenemos un edificio con personas en su interior; el objetivo es evaluar cuan vulnerable es el edificio ante ataques de bomba. Para esto utilizaremos algoritmos de inteligencia artificial para optimizar la localización donde una bomba produciría mas estragos conociendo sus características. Para elegir la "mejor peor" localización para la bomba (donde causaría mas estragos) simulamos el comportamiento de la multitud y su forma de evacuar el edificio. Luego de encontrar la "mejor peor" localización de una bomba se puede analizar como cubrir esa vulnerabilidad del edificio. 

## Especificaciones:
### Simulación:
En este proyecto **simularemos** el comportamiento de las **personas** dentro del edificio en cuestión después de la explosión de la bomba. En este caso cada persona quiere, por todos los medios salir del edificio y se habrá de evaluar como influye el comportamiento de las masas en las decisiones de un individuo en una situación de estrés. 

### Inteligencia Artificial:
Desde el punto de vista de la **IA** existen dos vertientes principales donde se podrían, por un lado generar por medio de la misma planos de edificios y determinar cuan seguros son; por otro lado utilizaremos algoritmos de **IA** para optimizar la posición donde la bomba resulta mas dañina. Esto nos arrojará resultados sobre la seguridad del edificio.

## Ejecución
Para ejecutar el proyecto es necesario iniciar el servidor de NodeJS para el frontend directamente en este directorio e iniciar el servidor Backend con Uvicorn dentro de `./backend`.
```bash
   npm start
```
```bash
   uvicorn main:app #En el directorio backend
```

+ [Informe Final](./docs/report.md)
+ [Guía de Instalación](./installation_guide.md)
+ [Issue relacionado](https://github.com/matcom/ia-sim-2022/issues/13)
