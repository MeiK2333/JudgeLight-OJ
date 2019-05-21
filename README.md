# JudgeLight-OJ

- 标准评测
- Special Judge

## Usage

### celery

```
celery -A app.tasks worker --loglevel=info
```

### web

```
gunicorn run:app -b 0.0.0.0:8080
```

## Docker 部署

```
export token=token
export RABBITMQ_DEFAULT_HOST=192.168.31.110
export RABBITMQ_DEFAULT_USER=guest
export RABBITMQ_DEFAULT_PASS=guest
docker-compose up
```
