FROM python
RUN pip install --upgrade pip
WORKDIR /app
COPY ./api/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api.src.main:app"]
