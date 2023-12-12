FROM python:3-alpine AS runner
 
WORKDIR /app
 
COPY --from=builder /app/venv venv
COPY app.py app.py
 
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV FLASK_APP=app/app.py
 
EXPOSE 8080
 
CMD ["gunicorn", "--bind" , ":8080", "--workers", "2", "app:app"]
