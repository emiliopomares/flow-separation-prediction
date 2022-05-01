FROM ubuntu:18.04
WORKDIR /app
COPY . .
RUN echo $(ls -lha) 
RUN apt-get update
RUN apt-get install -y python
RUN apt-get install -y python3-pip
RUN pip3 install numpy
RUN apt-get install -y wget
RUN apt-get install -y gnupg
RUN apt-get install -y software-properties-common
RUN pip3 install mysql-connector
RUN apt-get install -y git
RUN sh -c "wget -O - http://dl.openfoam.org/gpg.key | apt-key add -"
RUN add-apt-repository -y http://dl.openfoam.org/ubuntu
RUN apt-get update
RUN apt-get -y install openfoam5
WORKDIR /app/tools
RUN echo $(ls -lha)
CMD ["./start.sh"]
