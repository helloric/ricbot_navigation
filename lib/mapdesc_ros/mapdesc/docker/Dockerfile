FROM hdgigante/python-opencv:4.9.0-alpine

WORKDIR /app
COPY . /app/

RUN pip3 install pytest coverage
RUN pip3 install -e .