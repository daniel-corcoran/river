FROM ubuntu:22.04
RUN echo 'APT::Install-Suggests "0";' >> /etc/apt/apt.conf.d/00-docker
RUN echo 'APT::Install-Recommends "0";' >> /etc/apt/apt.conf.d/00-docker
RUN DEBIAN_FRONTEND=noninteractive
COPY . /
COPY interpreter/ lib/rIDE/interpreter
RUN ["/bin/sh", "apt-get update"]
RUN apt-get -y install python3-dev
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 80
WORKDIR /lib/rIDE/
ENTRYPOINT ["python", "main.py"]