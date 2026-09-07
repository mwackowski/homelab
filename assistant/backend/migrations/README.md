# Database migrations

Numbered SQL files define the PostgreSQL schema. Apply them once, in filename
order. Each file runs in a transaction; these migrations are manual and do not
yet have an automatic migration runner or version-tracking table.

## Initial schema

`001_initial_schema.sql` creates:

- `users`: identities with a display name and a `human` or `bot` kind. These are
  application identities, not PostgreSQL login accounts or authentication records.
- `conversations`: conversations linked to their creator through `created_by`.
- `messages`: ordered conversation history, including assistant tool calls and
  tool results. `author_id` optionally links a message to a human or bot identity;
  `role` describes its role in the model conversation and is separate from user kind.

Load history using `WHERE conversation_id = ... ORDER BY id`. Tool calls are
stored as JSONB; tool output is stored as text, including serialized `ToolResult`
JSON. Tool-result messages use `tool_call_id` to identify the call they answer.
The application must preserve that pairing and serialize writes within a
conversation; generated IDs alone do not coordinate concurrent agent runs.

Deleting a conversation deletes its messages. User deletion is blocked while
conversations or messages reference that user. Conversation membership and access
control are not implemented by this schema; a participants table can be added when
multiple users need to share conversations.

Keep generating the system prompt from code for now. Persist user, assistant,
and tool messages; the schema also permits system messages for future use.

## Apply

With PostgreSQL running, execute from the repository root:

```bash
docker compose --env-file .env -f assistant/compose.yaml exec -T assistant-postgres \
  psql -U assistant -d assistant -v ON_ERROR_STOP=1 \
  < assistant/backend/migrations/001_initial_schema.sql
```

The migration creates tables only; it does not create a placeholder user or
conversation. Insert a human user first, then create the test conversation using
that user's ID as `created_by`. UUID defaults generate IDs automatically, or the
application can supply a fixed conversation UUID during development.

Do not rerun an applied migration or edit it after deployment; add the next
numbered migration for subsequent schema changes.
