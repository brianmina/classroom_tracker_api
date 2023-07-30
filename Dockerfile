#/avian-serenity-393711

FROM python:3.11



# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

COPY ./requirements.txt $APP_HOME/requirements.txt

# Install production dependencies.
RUN set -ex; \
    pip install -r requirements.txt




CMD {"uvicorn", "main:app", "--host=0.0.0.0", "--reload", "--port", "8000"}



## Copy application dependency manifests to the container image.
## Copying this separately prevents re-running pip install on every code change.
#COPY ./requirements.txt /code/requirements.txt
#
## Install production dependencies.
#RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# # Copy local code to the container image.
# ENV APP_HOME /app
# WORKDIR $APP_HOME
# COPY . ./

# # Run the web service on container startup. Here we use the gunicorn
# # webserver, with one worker process and 8 threads.
# # For environments with multiple CPU cores, increase the number of workers
# # to be equal to the cores available.
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 -k uvicorn.workers.UvicornWorker main:app
