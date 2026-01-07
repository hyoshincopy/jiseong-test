from flask import Flask, request, jsonify
import logging
from logging.handlers import RotatingFileHandler
import os
import psycopg2

app = Flask(__name__)

# 작업 디렉토리 내에 로그 저장
log_dir = "/app/logs"
data = "1234"
try:
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, "app.log")
    file_handler = RotatingFileHandler(log_file, maxBytes=10240000, backupCount=5)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d] sdfdsfdsfdsfdsfdsfdsfsdfdsfsddsfsdfasdasdasdasdasdasdasdsadsdfdsfdsfdsfdsfdsfdsfsdfdsfsddsfsdfasdasdasdasdasdasdasdsadsdfdsfdsfdsfdsfdsfdsfsdfdsfsddsfsdfasdasdasdasdasdasdasdsadsdfdsfdsfdsfdsfdsfdsfsdfdsfsddsfsdfasdasdasdasdasdasdasdsad"
        )
    )
    app.logger.addHandler(file_handler)
except (OSError, PermissionError) as e:
    # 로그 디렉토리 생성 실패 시 콘솔 로깅만 사용
    app.logger.warning(
        f"Could not create log directory {log_dir}: {e}. Using console logging only."
    )

app.logger.setLevel(logging.INFO)
app.logger.info("Flask app startup")


# 모든 요청 전에 로깅
@app.before_request
def log_request_info():
    app.logger.info("=" * 80)
    app.logger.info(f"Request Method: {request.method}")
    app.logger.info(f"Request URL: {request.url}")
    app.logger.info(f"Request Path: {request.path}")
    app.logger.info(f"Client IP: {request.remote_addr}")
    app.logger.info(f"Headers: {dict(request.headers)}")

    # Request Body 로깅
    if request.method in ["POST", "PUT", "PATCH"]:
        if request.is_json:
            app.logger.info(f"Request Body (JSON): {request.get_json()}")
        else:
            body = request.get_data(as_text=True)
            # Body가 너무 길 수 있으므로 일부만 로깅 (최대 1000자)
            app.logger.info(f"Request Body (Raw): {body[:1000]}")
    app.logger.info("=" * 80)


@app.route("/")
def hello():
    app.logger.info("Home page accessed")
    return "Hello from Azure App Service!"


@app.route("/health")
def health():
    app.logger.info("Health check accessed")
    return "OK", 200


@app.route("/path/to/ping")
def ping():
    app.logger.info("Ping endpoint accessed")
    return "pong", 200


@app.route("/db-test")
def db_test():
    try:
        app.logger.info("DB connection test started")
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"),
            database=os.environ.get("DB_NAME", "postgres"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            port=os.environ.get("DB_PORT", "5432"),
            sslmode="require",
        )
        conn.close()
        app.logger.info("DB connection successful")
        return "Database connection successful!", 200
    except Exception as e:
        app.logger.error(f"DB connection failed: {str(e)}")
        return f"Database connection failed: {str(e)}", 500


@app.route("/test-post", methods=["POST"])
def test_post():
    try:
        app.logger.info("POST request received")

        # JSON 데이터 받기
        data = request.get_json() if request.is_json else {}

        # 요청 데이터 로깅
        app.logger.info(f"Received data: {data}")

        # 응답 데이터 구성
        response_data = {
            "status": "success",
            "message": "POST request received successfully",
            "received_data": data,
            "method": request.method,
        }

        return jsonify(response_data), 200
    except Exception as e:
        app.logger.error(f"POST request failed: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
