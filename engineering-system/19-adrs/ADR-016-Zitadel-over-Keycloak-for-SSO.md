---
ADR-016: Zitadel over Keycloak, Auth0, and Okta
Status: Accepted
Date: 2026-07-06

Context:
DhruvaOS acts as a multi-tenant platform where each school customer (tenant) requires localized branding, custom user roles, OIDC/SAML configurations, and single sign-on (SSO). Running identity infrastructure inside local dev environments and client offline networks is a core constraint. High JVM memory footprints and complex multi-realm organization mappings restrict our database scaling parameters.

Decision:
We chose Zitadel as our primary OIDC Identity Provider and SSO system.

Alternatives Considered:
- Keycloak: Rejected because of its heavy JVM resource footprint (minimum 1GB RAM container overhead) and its performance degradation when maintaining thousands of separate tenant realms.
- Auth0 / Okta: Rejected because they are proprietary, cloud-only SaaS providers that prevent local dev offline operation and violate our data sovereignty and self-hosting constraints.
- Custom SSO: Rejected because security protocol engineering (OpenID Connect / OAuth2) is highly vulnerable to security bugs, requiring large developer support resources.

Consequences:
We commit to utilizing Zitadel's user management APIs and OIDC token claims. We accept the tradeoff that Zitadel has a younger ecosystem with fewer pre-built community dashboard templates than Keycloak, meaning we must construct client-facing tenant administrative screens manually.

Revisit Triggers:
- If Zitadel's Go-native core changes to a restrictive licensing model that conflicts with open SaaS distribution parameters.
- If an enterprise customer mandates an Okta-exclusive user federation configuration that cannot be mapped via Zitadel custom OIDC configurations.
---
