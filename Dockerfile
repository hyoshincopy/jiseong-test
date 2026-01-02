FROM python:3.11-slim

WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY app.py .

# 로그 디렉토리 생성
RUN mkdir -p /app/logs && chmod 755 /app/logs

# 포트 노출
EXPOSE 8000

# 환경변수로 포트 설정
ENV PORT=8000
ENV DB_HOST=deep-medi.postgres.database.azure.com
ENV DB_NAME=postgres
ENV DB_USER=deep_medi
ENV DB_PASSWORD='elqapel86$$'
ENV DB_PORT=5432

# Gunicorn으로 실행
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile /app/logs/access.log --error-logfile /app/logs/error.log app:app