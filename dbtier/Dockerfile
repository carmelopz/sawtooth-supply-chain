FROM python:2
WORKDIR /dbtier
ADD . /dbtier
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "./dbtier.py"]
