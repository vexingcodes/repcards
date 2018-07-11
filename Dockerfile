FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
WORKDIR /repcards
RUN apt-get update \
 && apt-get install --yes \
      libcairo2 \
      libffi-dev \
      libgdk-pixbuf2.0-0 \
      libpango-1.0-0 \
      libpangocairo-1.0-0 \
      python3-pip \
      shared-mime-info \
 && pip3 install pipenv
ADD https://theunitedstates.io/congress-legislators/legislators-current.json ./
COPY Pipfile Pipfile.lock gen_cards.py ./
RUN pipenv install
CMD ["/usr/local/bin/pipenv", "run", "python", "gen_cards.py"]
