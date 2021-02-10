FROM continuumio/anaconda3

WORKDIR /rnamigos

COPY . .

RUN chmod +x boot.sh
RUN conda env create -f environment.yml
SHELL ["conda", "run", "-n", "rnamigos", "/bin/bash", "-c"]

EXPOSE 5003

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "rnamigos", "./boot.sh"]