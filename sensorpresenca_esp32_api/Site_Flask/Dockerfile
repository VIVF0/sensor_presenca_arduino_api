FROM python:3.10
COPY . /app
WORKDIR /app
RUN useradd -ms /bin/bash myuser
USER myuser
RUN pip install flask requests flask_session 
CMD ["python", "site.py"]
EXPOSE 300