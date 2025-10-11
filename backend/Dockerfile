# use official python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app
# copy files
COPY ./requirements.txt /app/requirements.txt

# Install dependecies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . /app

# Expose post
EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["uvicorn","app.main:app", "--host","0.0.0.0","--port","8000"]
