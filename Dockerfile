# Используйте базовый образ Python
FROM python:3.11

# Установите переменную среды для отключения режима буферизации вывода Python
ENV PYTHONUNBUFFERED 1

# Установите рабочую директорию в /app
WORKDIR /app

# Скопируйте файл зависимостей в рабочий каталог
COPY requirements.txt /app/

# Установите зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте текущий каталог в рабочий каталог контейнера
COPY . /app/
