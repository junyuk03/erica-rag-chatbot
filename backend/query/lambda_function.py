import json
import os

import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Lambda 컨테이너 재사용 시 클라이언트를 재활용하도록 핸들러 밖에서 생성
s3 = boto3.client("s3")


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "body": json.dumps(body, ensure_ascii=False),
    }


def _parse_body(event):
    """API Gateway 프록시 이벤트(body가 문자열)와 직접 호출(dict) 모두 지원."""
    body = event.get("body", event)
    if body is None:
        return {}
    if isinstance(body, str):
        return json.loads(body) if body.strip() else {}
    return body


def _check_bucket(bucket_name):
    """버킷의 파일 목록을 조회해 연결 여부를 반환."""
    if not bucket_name:
        return False, "RAW_BUCKET_NAME 환경변수가 설정되지 않았습니다."
    try:
        s3.list_objects_v2(Bucket=bucket_name, MaxKeys=1000)
        return True, None
    except (ClientError, BotoCoreError) as e:
        return False, str(e)


def lambda_handler(event, context):
    try:
        body = _parse_body(event)
    except json.JSONDecodeError:
        return _response(400, {"error": "요청 body가 올바른 JSON 형식이 아닙니다."})

    question = body.get("question") if isinstance(body, dict) else None
    if not question:
        return _response(400, {"error": "question 필드가 필요합니다."})

    bucket_connected, bucket_error = _check_bucket(os.environ.get("RAW_BUCKET_NAME"))

    result = {
        "status": "OK",
        "bucket_connected": bucket_connected,
        "question": question,
    }
    if bucket_error:
        result["bucket_error"] = bucket_error

    return _response(200, result)
