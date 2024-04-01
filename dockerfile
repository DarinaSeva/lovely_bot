FROM python:3.12.2-slim
ENV TOKEN="6974873059:AAGHCq0oo2WEd0TOqR2yOHEd_M0WBZvVLtk"
COPY . . 
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "bot.py" ]