FROM ubuntu:latest
WORKDIR /app
COPY . .
RUN apt-get update
RUN apt-get install -y python
RUN apt-get install -y pip
RUN pip3 install matplotlib
RUN apt-get install -y wget
RUN apt-get install -y gnupg
RUN apt-get install -y software-properties-common
RUN pip3 install mysql-connector
RUN apt-get install -y git
RUN sh -c "wget -O - http://dl.openfoam.org/gpg.key | apt-key add -"
RUN add-apt-repository -y http://dl.openfoam.org/ubuntu
RUN apt-get update
RUN apt-get -y install openfoam5
RUN source /opt/openfoam5/etc/bashrc
RUN git clone https://github.com/emiliopomares/flow-separation-prediction
CMD ["python3", "./flow-separation-prediction/tools/make_dataset.py"]
