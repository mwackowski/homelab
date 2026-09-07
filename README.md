# Homelab

Docker Compose configuration for services running in the homelab.

## Services

- **Pi-hole** — network-wide DNS filtering and wildcard DNS for `home.arpa`.
- **Dashboard** — lightweight static homepage served by nginx.
- **Assistant** — chat frontend served by nginx with a FastAPI backend.

## Ports and endpoints

| Service | Exposed port | Address |
| --- | --- | --- |
| Pi-hole DNS | `53/tcp`, `53/udp` | Homelab host |
| Pi-hole web UI | `80`, `443` | `http://pihole.home.arpa/admin/` |
| Dashboard | `8080` | `http://dashboard.home.arpa:8080/` |
| Assistant UI | `8081` | `http://<assistant-server>:8081/` |
| Assistant chat API | Through `8081` | `POST /api/chat` |

The assistant backend listens on port `8000` inside its Docker network and is
not published directly to the LAN. nginx forwards `/api/` requests to it.

## Structure

```text
.
├── edge/             # Edge host stack
│   ├── compose.yaml
│   ├── pihole/       # Pi-hole configuration
│   └── dashboard/    # Homelab dashboard
└── assistant/        # Assistant frontend and backend
    ├── frontend/
    ├── backend/
    ├── compose.yaml
    └── nginx.conf
```

The `edge/compose.yaml` project runs Pi-hole and the dashboard on the edge host.
It retains the project name `homelab`. The assistant has its own Compose project
for the core host and can be deployed independently.

## Running the stacks

From the repository root on the appropriate host, supply the environment file
for that deployment:

```bash
# Edge host: Pi-hole and dashboard
docker compose --env-file .env -f edge/compose.yaml up -d

# Core host: assistant and data services
docker compose --env-file assistant/.env -f assistant/compose.yaml up -d --build
```

Use `edge/pihole/.env.example` and `assistant/.env.example` as configuration
references. SSH mount paths must point to files on the machine running Docker.

When updating an existing edge deployment, move its Pi-hole data directory from
`pihole/etc-pihole/` to `edge/pihole/etc-pihole/` before recreating containers.
The project name is unchanged, but bind mounts now use the new paths.
