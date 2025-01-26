name: Django CI

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: test_db
          MYSQL_USER: test_user
          MYSQL_PASSWORD: test_password
        ports:
          - 3306:3306
        options: >-
          --health-cmd="mysqladmin ping --silent"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=3

    steps:
    - name: Checkout Code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r messaging_app/requirements.txt

    - name: Run Migrations
      env:
        DATABASE_URL: mysql://test_user:test_password@127.0.0.1:3306/test_db
      run: |
        python manage.py makemigrations
        python manage.py migrate

    - name: Run Tests
      env:
        DATABASE_URL: mysql://test_user:test_password@127.0.0.1:3306/test_db
      run: |
        pytest
