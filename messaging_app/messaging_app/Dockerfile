# Step 1: Use a base Python image
FROM python:3.10

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the Django project into the container
COPY . /app/

# Step 5: Expose port 8000
EXPOSE 8000

# Step 6: Set the command to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
