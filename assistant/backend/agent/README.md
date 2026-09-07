# Agent tools

`homelab.py` contains connectivity helpers for the edge host. Currently, `ssh()`
runs `hostname` to check remote command execution; container inspection is still
to be implemented. The SSH username is currently `pi`.

## SSH setup

Run these commands on your development machine, replacing `<edge-host>` with
the edge host's address:

```bash
mkdir -p ~/.ssh/homelab
ssh-keygen -t ed25519 -f ~/.ssh/homelab/homelab_agent
ssh-copy-id -i ~/.ssh/homelab/homelab_agent.pub pi@<edge-host>
ssh -i ~/.ssh/homelab/homelab_agent pi@<edge-host> hostname
```

For unattended use without an SSH agent, leave the key passphrase empty. Skip
key generation if you already have this key. Verify the server fingerprint
before accepting a new host when SSH prompts you.

- The private key stays on the connecting machine.
- `ssh-copy-id` adds the public key to the Pi's `~/.ssh/authorized_keys`, allowing
  the Pi to authenticate the client.
- The client's `~/.ssh/known_hosts` records the server's public host key, allowing
  the client to recognize the Pi.

After a trusted local connection, extract only this host's saved entry:

```bash
ssh-keygen -F <edge-host> -f ~/.ssh/known_hosts > ~/.ssh/homelab/known_hosts
```

Check that the extracted file contains an entry. Use the same address as
`EDGE_SSH_HOST` below.

## Configuration

Add these variables to the repository root's ignored `.env`, using your own
absolute paths (not `~`):

```dotenv
EDGE_SSH_HOST=<edge-host>
EDGE_SSH_KEY_PATH=/absolute/path/to/.ssh/homelab/homelab_agent
EDGE_SSH_KNOWN_HOSTS_PATH=/absolute/path/to/.ssh/homelab/known_hosts
```

For local Python execution, load this `.env` before calling the helpers. Local
SSH uses the key path above and reads the usual `~/.ssh/known_hosts` automatically.
Keep private keys and real environment values out of Git.

For Docker, ensure `assistant-api` in `assistant/compose.yaml` includes these
entries alongside its existing configuration:

```yaml
environment:
  EDGE_SSH_HOST: ${EDGE_SSH_HOST}
  EDGE_SSH_KEY_PATH: /run/ssh/homelab_agent
volumes:
  - ${EDGE_SSH_KEY_PATH}:/run/ssh/homelab_agent:ro
  - ${EDGE_SSH_KNOWN_HOSTS_PATH}:/root/.ssh/known_hosts:ro
```

The source files must exist on the machine running Docker. Both mounts are
read-only. The container currently runs as root, so SSH automatically reads
`/root/.ssh/known_hosts`. The Dockerfile installs the SSH client and copies the
`agent` module.

## Test in Docker

From the repository root:

```bash
docker compose --env-file .env -f assistant/compose.yaml up -d --build assistant-api
docker compose --env-file .env -f assistant/compose.yaml exec assistant-api \
  python -c "from agent.homelab import ssh; ssh()"
```

The test should print the edge host's hostname. SSH's `Permission denied` indicates
an authentication problem; `Host key verification failed` indicates a missing or
mismatched server entry in the container's `known_hosts` file.

## Docker permissions on the edge host

If SSH connects but `docker ps --all` reports permission denied for
`/var/run/docker.sock`, the remote user needs Docker access. Check its groups
from your development machine:

```bash
ssh -i ~/.ssh/homelab/homelab_agent pi@<edge-host> id
```

If `docker` is missing, run this **on the edge host** to grant access:

```bash
sudo usermod -aG docker pi
```

`-aG` adds the group without removing existing memberships. Docker group
membership grants full Docker control, effectively root-level access to the edge host.

Open a new SSH connection for the membership to take effect. Each SSH subprocess
in the notebook opens a fresh connection, so retry the call. To verify directly:

```bash
ssh -i ~/.ssh/homelab/homelab_agent pi@<edge-host> 'docker ps --all'
```
