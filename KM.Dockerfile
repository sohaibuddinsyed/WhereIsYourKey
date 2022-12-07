# start by pulling the python image
FROM python:3.10

RUN pip install --upgrade pip

# copy the requirements file into the image
COPY ./keyManager/requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY ./keyManager /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python", "-m" ]

CMD [ "flask", "run", "--host=0.0.0.0"]