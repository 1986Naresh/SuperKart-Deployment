FROM python:3.9-slim

#set the working directory
WORKDIR /app

#Copy all files
COPY . .

#install Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define the command to start the application using Gunicorn with 4 worker processes
# - `-w 4`: Uses 4 worker processes for handling requests
# - `-b 0.0.0.0:7860`: Binds the server to port 7860 on all network interfaces
# - `app:app`: Runs the Flask app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:app"]
