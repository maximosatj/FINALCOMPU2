# Usa una imagen de Python como base
FROM python:3.10

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el contenido actual del directorio al contenedor en /app
COPY server.py /app/

# Expone el puerto en el que la aplicación se ejecutará
EXPOSE 5000

# Comando para ejecutar la aplicación cuando el contenedor se inicia
CMD ["python", "server.py"]
