FROM python:3.10
COPY . /app
WORKDIR /app
RUN useradd -ms /bin/bash myuser
USER myuser
RUN pip install pymongo==3.12.0 flask requests bson==0.5.10 Flask & pip install --upgrade pymongo flask 
CMD ["python", "api.py"]
EXPOSE 300