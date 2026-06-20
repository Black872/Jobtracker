# JobTracker Technical Specification v3

## Goal
Build a web application for tracking job applications.

## MVP Features
- Add vacancy
- Edit vacancy
- Delete vacancy
- View vacancy list
- Search by company
- Search by position
- Filter by status
- Dashboard

## Vacancy Fields
- Company Name
- Position Title
- Job URL
- Location
- Employment Type
- Salary Min
- Salary Max
- Application Date
- Status
- Contact Person
- Contact Email
- Contact Phone
- Notes

## Calculated Fields
- Days Since Application
- Days In Current Status

## Vacancy Statuses
- Wishlist
- Applied
- Response Received
- Interview Scheduled
- Technical Interview
- Final Interview
- Offer
- Accepted
- Rejected
- Withdrawn

## Technology Stack
Frontend: React + TypeScript
Backend: FastAPI
Database: PostgreSQL

## Explicitly Out Of Scope
- Docker
- Kubernetes
- Terraform
- Ansible
- ArgoCD
- GitOps
- Monitoring
- Infrastructure provisioning
