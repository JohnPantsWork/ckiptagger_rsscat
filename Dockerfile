# Base image
FROM tensorflow/tensorflow:latest

# install dependence for ckiptagger
RUN pip3 install ckiptagger
RUN pip3 install gdown
RUN pip3 install numpy

# install dependence for server
RUN pip3 install Flask
RUN pip3 install Flask[async]
RUN pip3 install fs

COPY . /ckiptagger_rsscat
WORKDIR /ckiptagger_rsscat
EXPOSE 5000

CMD ["python3","-u","server.py"]