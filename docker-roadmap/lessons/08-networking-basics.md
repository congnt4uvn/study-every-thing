# Lesson 08 — Networking: ports, DNS, bridge networks

## Goals
- Understand port publishing and container-to-container networking
- Create a user-defined bridge network
- Use Docker DNS for service discovery

## Port publishing
Containers have their own network namespace. Publishing ports exposes a container port to the host.

```powershell
# host:8080 -> container:80
docker run -d --name web -p 8080:80 nginx:latest
```

Notes:
- `-p 8080:80` is explicit
- `-p 80` (without host port) publishes to a random host port

## Container-to-container networking
By default, Docker creates a `bridge` network. Containers on the same user-defined network can resolve each other by name.

### Create a network
```powershell
docker network create appnet
docker network ls
```

### Run two containers on that network
```powershell
docker run -d --name api --network appnet nginx:latest

docker run --rm -it --name client --network appnet alpine:3.19 sh
# inside client:
# (install curl)
apk add --no-cache curl
curl -I http://api
exit
```

If `curl http://api` works, Docker DNS is resolving `api` to the container IP.

### Inspect network
```powershell
docker network inspect appnet
```

## Why user-defined networks are better than default bridge
- Automatic DNS resolution by container name
- Better isolation
- More predictable for multi-service apps

## Hands-on lab
1. Publish ports and confirm mapping:
```powershell
docker run -d --name web2 -p 8081:80 nginx:latest
docker port web2
```

2. Service discovery via container name (use the `appnet` lab above).

3. Cleanup:
```powershell
docker rm -f web web2 api
docker network rm appnet
```

## Checklist
- I can explain host vs container ports
- I can create a network and connect containers
- I understand name-based service discovery inside Docker networks

## Common pitfalls
- **Trying to use `localhost` between containers**: inside a container, `localhost` refers to itself. Use the other container name.
- **Port conflicts**: only one process can bind a given host port.
