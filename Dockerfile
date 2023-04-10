ARG PYTHON_VERSION=3.9.7
FROM python:$PYTHON_VERSION

ENV BASE_DIR=stock

RUN echo "Installing system deps" \
    && apt-get update \
    && apt-get install -y build-essential \
#     && apt-get install -y python3-venv \
    && apt-get install -y unixodbc unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install --upgrade pip setuptools

# install pyodbc
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && apt-get install openssl \
    && sed -i 's,^\(MinProtocol[ ]*=\).*,\1'TLSv1.0',g' /etc/ssl/openssl.cnf \
    && sed -i 's,^\(CipherString[ ]*=\).*,\1'DEFAULT@SECLEVEL=1',g' /etc/ssl/openssl.cnf\
    && apt-get install ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Setup workdir
RUN mkdir $BASE_DIR
WORKDIR $BASE_DIR

# Setup
RUN echo "Copy setup file to $BASE_DIR"
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

ADD ./src ./src
ADD ./.env ./.env
ADD ./server.py ./server.py

CMD ["python3", "server.py"]
