# **************************
# Builder
# **************************

# pull official base image
FROM python:3-slim as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
#RUN apt update \
#    && apt postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# **************************
# Final
# **************************
FROM python:3-slim
# create directory for the app user
RUN mkdir -p /var/totalechaos

# create the totalechaos user
RUN addgroup --system totalechaos && adduser --system totalechaos --ingroup totalechaos

# create the appropriate directories
ENV HOME=/var/totalechaos
ENV APP_HOME=/var/totalechaos/app
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
WORKDIR $APP_HOME

# install dependencies
#RUN apt update && apt add libpq
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy entrypoint-prod.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R totalechaos:totalechaos $APP_HOME

# change to the app user
USER totalechaos

# run entrypoint.sh
ENTRYPOINT ["/var/totalechaos/app/entrypoint.sh"]
