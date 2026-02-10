# Hospital Management App Workspace

This directory isolates hospital product development from the core `clip` library package.

## Structure

- `backend/` — API services, authentication, authorization, and database models.
- `frontend/` — UI routes, screens, and form workflows.
- `infra/` — environment configuration, deployment manifests, and operational tooling.

## Development Notes

- Keep all hospital product code inside this directory tree.
- Integrations with CLIP should be introduced only through explicit AI feature modules.
