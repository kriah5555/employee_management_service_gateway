FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Configure non-root user.
ARG PUID=1000
ENV PUID ${PUID}
ARG PGID=1000
ENV PGID ${PGID}

RUN groupmod -o -g ${PGID} www-data && usermod -o -u ${PUID} -g www-data www-data

RUN chown -R www-data:www-data /app

USER www-data

# Expose the Gunicorn port
EXPOSE 8000

COPY ./docker/entrypoint.sh /

ENTRYPOINT ["sh", "/entrypoint.sh"]