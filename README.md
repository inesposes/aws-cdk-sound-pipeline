# 🔊 Simulación de un Pipeline ETL de audio con AWS CDK y LocalStack



## 📋 Descripción
Este proyecto forma parte de unas clases impartidas durante un periodo formativo en NTT Data por Napoleón Lazardi.

El objetivo es simular el proceso de ETL de audios para un proyecto que consiste en el mantenimiento predictivo con IA de equipos industriales mediante sensorización acústica. La base principal será:
  - LocalStack: simulación de los servicios de AWS gratuitamente
  - AWS CDK: programación de la infraestructura (IaC)
  - Makefile: automatización de los procesos

Simularemos audios de máquinas industriales que seguirán todo nuestro flujo de datos:

![AWS](/img/aws-diagram.png)

---
## ✅ Servicios utilizados y su propósito

| Servicio AWS Simulado | Uso en el Proyecto |
|------------------------|---------------------|
| **S3**                | Almacena archivos subidos por la Lambda |
| **Lambda**            | Recibe un payload, crea un archivo y lo guarda en S3 |
| **IAM**               | Permite a la Lambda subir a S3 (grant_put) |
| **SSM**               | Necesario para el `cdk bootstrap` |
| **CloudFormation**    | CDK lo usa para desplegar stacks |
| **Glue**              | Transforma los datos|
| **SNS**               | Servicio de notificaciones|
| **SQS**               | Gestiona mensajes entre componentes del sistema|

---

## 🛠️ Requisitos previos

Asegúrate de tener lo siguiente instalado:

- Python 3.9+
- Docker + Docker Compose
- Node.js >= 18.x (¡Evita v23 por warning de JSII!)

---

## ⚙️ Instalación paso a paso

### 1. Preparación CDK

**Variables de entorno**  
Copia el archivo .env.example y reemplaza el valor de IP_ADDRESS por localhost

Si en lo siguientes pasos ves que con localhost no funciona, reemplázalo con la IP de tu máquina. En entornos WSL puede dar priblemas.


**AWS CDK**
```bash
cd cdk
python3 -m venv .venv # Si trabajas en Ubuntu asegura tener instalado python3-env (sudo apt install python3.12-venv) 
source .venv/bin/activate
pip3 install -r requirements.txt
sudo apt install ffmpeg 
npm install -g aws-cdk-local aws-cdk
```
Configuracón AWS: 
```bash
aws configure
```
Rellena con los siguientes datos:   
![Config aws](/img/aws-configuration.png)
### 2. Iniciar LocalStack

```bash
make start-localstack
```

### 3. Bootstrap del entorno local (solo 1 vez)

```bash
make bootstrap
```

### 4. Desplegar Lambda + S3

```bash
make deploy
```
### 5. Abrir el servidor local donde se genera el audio
```bash
make audio-generator
```
Accede en tu navegador a http://localhost:8080 y pulsa en audio.html
### 6. Simulación ETL

❗ **Limitación técnica**

Este proyecto incluye una Lambda de procesamiento ETL, que normalmente se desplegaría con el siguiente comando:

```bash
make deploy-etl
```
Está función se subscribiría con SQS automaticamente al topic al que publica el SNS y cada vez que llegase una notificación ejecutaría el ETL para el nuevo audio entrante.

Sin embargo, debido a que estamos trabajando con LocalStack y una cuenta AWS simulada, esta Lambda no puede instalar correctamente las dependencias externas necesarias.



✅ **Solución alternativa**

Para evitar este problema, se ha creado un script local en Python (simulate_glue.py) que simula el comportamiento de la Lambda ETL. 


Abre una nueva terminal y accede al entorno virtual previamente creado. Ejecuta el siguiente comando:


```bash
make simulate
```
El resultado esperado:    
![Expected result](/img/example.png)


### 7. Probar que todo funciona
```bash
make list-bucket    # Verifica que se han recibido audios en el bucket de entrada
make list-output-bucket    # Verifica que se guarden los audios procesados en el audio de salida
```

---


## 👥 Autores

**Martín Amor**  
**Noelia Sánchez**  
**Inés Poses**  
**Celia Incera**   
