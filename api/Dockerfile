FROM python:3.13
WORKDIR app
COPY . .
RUN pip install -r requirements.txt
CMD alembic upgrade head && fastapi run main.py