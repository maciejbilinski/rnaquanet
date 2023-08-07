# RNAQuANet

## Build and run docker image
**Info:** make sure that `docker-entrypoint.sh` file has correct line ending (must be **LF**, not **CRLF**) in order to work correctly under Linux.

```bash
docker compose up --build
```

it runs pipeline and monitor. To check progress visit http://127.0.0.1:8080
