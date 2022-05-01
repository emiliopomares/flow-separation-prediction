FROM ubuntu:latest
WORKDIR /app
COPY . .
RUN apt-get update
RUN apt-get install -y openfoam
RUN apt-get install -y python
RUN apt-get install -y pip
RUN pip3 install matplotlib
RUN pip3 install mysql-connector
RUN apt-get install -y git
RUN git clone https://github.com/emiliopomares/flow-separation-prediction
CMD ["python3", "./flow-separation-prediction/tools/make_dataset.py"]
