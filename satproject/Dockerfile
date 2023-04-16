#Installs ubuntu 20.04 from Docker Hub
FROM ubuntu:20.04

RUN apt-get update

RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

#Declaring working directory in our container
WORKDIR /home/root/app/

#Copy requirements.txt to $WORKDIR
COPY requirements.txt .

RUN pip3 install -r requirements.txt


#Copy source files to $WORKDIR
COPY . .

ENV PORT=5000
EXPOSE 5000

CMD ["python3", "app.py"]