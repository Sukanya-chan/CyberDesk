# Security Requirements

## Authentication
Secure password hashing, protected sessions/tokens, login abuse controls where appropriate.

## Authorization
Roles: `student`, `admin`.
Authorization must be checked on the backend, never only in frontend routing.

## Input and web security
Account for XSS, CSRF where applicable, SQL injection, IDOR/broken access control, path traversal, unsafe uploads and sensitive-data exposure.

## CTF safety
Never execute arbitrary submissions on the main server. MVP challenges should use static flags, decoding, logs, packet-analysis files, configuration analysis or simulated logic.

## Secrets
Use environment variables. `.env` is never committed. Provide `.env.example`.

## Logging
Never log passwords, tokens, API keys or unnecessary personal data.
