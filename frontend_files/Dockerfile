FROM python:3.9-slim

#set the working directory
WORKDIR /app

#Copy all files
COPY . .

#install Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define the command to start the application using Gunicorn with
CMD ["streamlit","run","app.py","--server.port=8502","--server.address=0.0.0.0", "server.enableXsrfProtection=false"]
