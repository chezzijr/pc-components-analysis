-- Create GPU table
CREATE TABLE gpu (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    manufacturer TEXT NOT NULL,
    memory TEXT NOT NULL,
    memory_type TEXT NOT NULL,
    memory_bandwidth TEXT NOT NULL,
    memory_clock TEXT NOT NULL,
    core_clock TEXT NOT NULL,
    boost_clock TEXT NOT NULL,
    core_config TEXT NOT NULL,
    output TEXT NOT NULL,
    interface TEXT NOT NULL,
    tdp TEXT NOT NULL,
    price TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
