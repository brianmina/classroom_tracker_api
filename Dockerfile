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


CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--reload", "--port", "8080"]
