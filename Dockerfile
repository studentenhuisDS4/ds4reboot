FROM python:3.7.3
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Libraries & db driver
RUN pip install --upgrade pip \
	&& pip install pipenv
RUN apt update && apt -y upgrade \
 	&& pip install psycopg2
COPY Pipfile /app/Pipfile
RUN pipenv install --skip-lock --system --dev 
# --verbose

COPY ./ /app
