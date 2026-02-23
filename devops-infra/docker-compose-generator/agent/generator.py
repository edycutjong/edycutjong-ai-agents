"""Docker Compose generator — scaffold docker-compose.yml from service templates."""
from __future__ import annotations
import json
from dataclasses import dataclass, field

@dataclass
class Service:
    name: str
    image: str
    ports: list[str] = field(default_factory=list)
    environment: dict[str, str] = field(default_factory=dict)
    volumes: list[str] = field(default_factory=list)
    depends_on: list[str] = field(default_factory=list)
    restart: str = "unless-stopped"
    healthcheck: dict | None = None
    networks: list[str] = field(default_factory=list)
    def to_dict(self) -> dict:
        d = {"image": self.image}
        if self.ports: d["ports"] = self.ports
        if self.environment: d["environment"] = self.environment
        if self.volumes: d["volumes"] = self.volumes
        if self.depends_on: d["depends_on"] = self.depends_on
        if self.restart: d["restart"] = self.restart
        if self.healthcheck: d["healthcheck"] = self.healthcheck
        if self.networks: d["networks"] = self.networks
        return d

SERVICE_TEMPLATES = {
    "postgres": Service(name="postgres", image="postgres:16-alpine", ports=["5432:5432"], environment={"POSTGRES_DB": "mydb", "POSTGRES_USER": "user", "POSTGRES_PASSWORD": "password"}, volumes=["postgres_data:/var/lib/postgresql/data"], healthcheck={"test": ["CMD-SHELL", "pg_isready -U user"], "interval": "10s", "retries": 5}),
    "redis": Service(name="redis", image="redis:7-alpine", ports=["6379:6379"], volumes=["redis_data:/data"], healthcheck={"test": ["CMD", "redis-cli", "ping"], "interval": "10s", "retries": 5}),
    "mysql": Service(name="mysql", image="mysql:8", ports=["3306:3306"], environment={"MYSQL_ROOT_PASSWORD": "root", "MYSQL_DATABASE": "mydb"}, volumes=["mysql_data:/var/lib/mysql"]),
    "mongo": Service(name="mongo", image="mongo:7", ports=["27017:27017"], volumes=["mongo_data:/data/db"], environment={"MONGO_INITDB_ROOT_USERNAME": "root", "MONGO_INITDB_ROOT_PASSWORD": "password"}),
    "nginx": Service(name="nginx", image="nginx:alpine", ports=["80:80", "443:443"], volumes=["./nginx.conf:/etc/nginx/nginx.conf:ro"]),
    "rabbitmq": Service(name="rabbitmq", image="rabbitmq:3-management-alpine", ports=["5672:5672", "15672:15672"], environment={"RABBITMQ_DEFAULT_USER": "guest", "RABBITMQ_DEFAULT_PASS": "guest"}),
    "minio": Service(name="minio", image="minio/minio:latest", ports=["9000:9000", "9001:9001"], volumes=["minio_data:/data"], environment={"MINIO_ROOT_USER": "admin", "MINIO_ROOT_PASSWORD": "password123"}),
    "mailhog": Service(name="mailhog", image="mailhog/mailhog:latest", ports=["1025:1025", "8025:8025"]),
}

def yaml_serialize(data: dict, indent: int = 0) -> str:
    """Simple YAML serializer."""
    lines = []
    pad = "  " * indent
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{pad}{key}:")
            lines.append(yaml_serialize(value, indent + 1))
        elif isinstance(value, list):
            lines.append(f"{pad}{key}:")
            for item in value:
                if isinstance(item, str):
                    lines.append(f"{pad}  - {item}")
                elif isinstance(item, dict):
                    items = list(item.items())
                    first_k, first_v = items[0]
                    lines.append(f"{pad}  - {first_k}: {first_v}")
                    for k, v in items[1:]:
                        lines.append(f"{pad}    {k}: {v}")
        elif value is None:
            lines.append(f"{pad}{key}:")
        else:
            lines.append(f"{pad}{key}: {value}")
    return "\n".join(lines)

def generate_compose(service_names: list[str], version: str = "3.8") -> str:
    services = {}
    volumes = {}
    for name in service_names:
        template = SERVICE_TEMPLATES.get(name.lower())
        if template:
            services[template.name] = template.to_dict()
            for v in template.volumes:
                vol_name = v.split(":")[0]
                if not vol_name.startswith(".") and not vol_name.startswith("/"):
                    volumes[vol_name] = None
    compose = {"version": f'"{version}"', "services": services}
    if volumes: compose["volumes"] = volumes
    return yaml_serialize(compose)

def list_templates() -> list[str]:
    return sorted(SERVICE_TEMPLATES.keys())

def get_template(name: str) -> Service | None:
    return SERVICE_TEMPLATES.get(name.lower())
