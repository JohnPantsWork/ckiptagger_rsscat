# Base image
FROM tensorflow/tensorflow:latest

# install dependence for ckiptagger
RUN pip3 install ckiptagger
RUN pip3 install gdown
RUN pip3 install numpy

# install dependence for server
RUN pip3 install Flask
RUN pip3 install fs

CMD ["python3","./ckiptagger_rsscat/server/server.py"]