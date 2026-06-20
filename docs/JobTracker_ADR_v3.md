# JobTracker ADR v3

## Purpose
JobTracker is a personal application for tracking job applications.

The primary goal is to build a maintainable web application.

Infrastructure and DevOps activities are intentionally handled separately by the project owner.

## ADR-001 Repository Structure
Use a monorepo.

frontend/
backend/
database/
docs/

## ADR-002 Frontend Technology
React + TypeScript

## ADR-003 Backend Technology
FastAPI

## ADR-004 Database
PostgreSQL

## ADR-005 API Style
REST API

## ADR-006 Local Development
Docker Compose may be used for local development.

## Out Of Scope For Codex
- Docker
- GitHub Actions
- Kubernetes
- Helm
- Terraform
- Ansible
- ArgoCD
- GitOps
- Monitoring
- Infrastructure provisioning
- VPS configuration
