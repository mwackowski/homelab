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
├── compose.yaml       # Core homelab stack
├── pihole/           # Pi-hole configuration
├── dashboard/        # Homelab dashboard
└── assistant/        # Assistant frontend and backend
    ├── frontend/
    ├── backend/
    ├── compose.yaml
    └── nginx.conf
```

The root Compose project runs Pi-hole and the dashboard. The assistant has its
own Compose project and can be deployed independently.
