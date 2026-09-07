BEGIN;

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    display_name TEXT NOT NULL CHECK (btrim(display_name) <> ''),
    kind TEXT NOT NULL CHECK (kind IN ('human', 'ai')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_by UUID NOT NULL REFERENCES users (id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX conversations_created_by_idx ON conversations (created_by);

CREATE TABLE messages (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    conversation_id UUID NOT NULL REFERENCES conversations (id) ON DELETE CASCADE,
    author_id UUID REFERENCES users (id),
    role TEXT NOT NULL CHECK (role IN ('system', 'user', 'assistant', 'tool')),
    content TEXT,
    tool_calls JSONB,
    tool_call_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- Assistant tool-call messages may have no text content.
    CONSTRAINT messages_payload_check CHECK (
        content IS NOT NULL OR tool_calls IS NOT NULL
    ),
    CONSTRAINT messages_tool_calls_check CHECK (
        tool_calls IS NULL OR (
            role = 'assistant' AND jsonb_typeof(tool_calls) = 'array'
        )
    ),
    CONSTRAINT messages_tool_call_id_check CHECK (
        (role = 'tool' AND tool_call_id IS NOT NULL AND btrim(tool_call_id) <> '')
        OR (role <> 'tool' AND tool_call_id IS NULL)
    )
);

CREATE INDEX messages_conversation_id_id_idx ON messages (conversation_id, id);
CREATE INDEX messages_author_id_idx ON messages (author_id);

COMMIT;
