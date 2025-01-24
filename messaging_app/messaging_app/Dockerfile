# Step 1: Use Python 3.10 as the base image
FROM python:3.10

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy requirements.txt into the container
COPY requirements.txt /app/

# Step 4: Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the entire Django project into the container
COPY . /app/

# Step 6: Expose the port the app will run on
EXPOSE 8000

# Step 7: Set the default command to run the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
