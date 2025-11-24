FROM python:3.9-slim

ENV HOME=/app

WORKDIR $HOME
ADD requirements.txt $HOME/

RUN pip install --no-cache-dir -r requirements.txt

ADD main.py $HOME/
ADD themoviedb $HOME/themoviedb
ADD watchlist $HOME/watchlist

CMD [ "python3" , "/app/main.py" ]
