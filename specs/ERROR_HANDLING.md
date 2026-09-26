# Error Handling

Use a consistent JSON error shape such as:

{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable message",
    "details": {}
  }
}

Never expose stack traces, secrets, database internals or sensitive implementation details.
