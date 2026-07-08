---
ADR-017: Traefik over Nginx, Envoy, and Kong
Status: Accepted
Date: 2026-07-06

Context:
DhruvaOS dynamic plugin framework registers routing prefixes and domains automatically at boot time. The platform ingress gateway must automatically discover new API service routes and let tenant subdomains maps dynamically without requiring server reload downtime. We need a routing gateway with a low configuration footprint that integrates directly with both local Docker socket environments and production Kubernetes clusters.

Decision:
We chose Traefik as our primary ingress gateway and reverse proxy.

Alternatives Considered:
- Nginx: Rejected because it lacks direct dynamic configuration APIs, requiring manual file templates rendering and server reloads (`nginx -s reload`) to expose newly provisioned tenant subdomains.
- Envoy Proxy: Rejected due to its complex static YAML control-plane configurations, which are difficult for a small engineering team to configure and debug locally.
- Kong Gateway: Rejected because it requires a separate database store (PostgreSQL or Cassandra) to maintain routing state, adding operational infrastructure footprint to local dev environments.

Consequences:
We commit to configuring ingress routing via Traefik labels in Docker Compose or CRD ingress annotations in Kubernetes. We accept the tradeoff that Traefik has fewer advanced request transformation/scripting capabilities (e.g. Lua extensions) than Nginx or Kong, meaning custom request logic must be executed inside our Core API gateway middleware.

Revisit Triggers:
- If we require complex edge script execution or request-body mutations that cannot be handled efficiently within the Python application middleware layer.
- If gateway routing configuration bottlenecks Traefik's dynamic auto-discovery loop under thousands of transient subdomains.
---
