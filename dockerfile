FROM python:3.12.2-slim
ENV TOKEN=""
COPY . . 
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "bot.py" ]