CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE TABLE IF NOT EXISTS commerce_quotes (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id uuid NOT NULL,
 customer_id uuid NOT NULL, cart_id uuid NOT NULL, quote_version integer NOT NULL DEFAULT 1,
 currency char(3) NOT NULL DEFAULT 'VND', subtotal_minor bigint NOT NULL CHECK(subtotal_minor>=0),
 discount_minor bigint NOT NULL DEFAULT 0 CHECK(discount_minor>=0),
 shipping_minor bigint NOT NULL DEFAULT 0 CHECK(shipping_minor>=0),
 tax_minor bigint NOT NULL DEFAULT 0 CHECK(tax_minor>=0),
 total_minor bigint NOT NULL CHECK(total_minor>=0),
 fingerprint varchar(128) NOT NULL, expires_at timestamptz NOT NULL,
 created_at timestamptz NOT NULL DEFAULT now(),
 UNIQUE (tenant_id,id,quote_version),
 CHECK (total_minor=subtotal_minor-discount_minor+shipping_minor+tax_minor)
);
CREATE TABLE IF NOT EXISTS commerce_idempotency (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id uuid NOT NULL,
 actor_id uuid NOT NULL, operation varchar(96) NOT NULL,
 request_key varchar(160) NOT NULL, request_hash char(64) NOT NULL,
 http_status integer, response_json jsonb, status varchar(20) NOT NULL,
 created_at timestamptz NOT NULL DEFAULT now(), expires_at timestamptz NOT NULL,
 UNIQUE(tenant_id,actor_id,operation,request_key)
);
CREATE TABLE IF NOT EXISTS commerce_payment_events (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id uuid NOT NULL,
 provider varchar(60) NOT NULL, provider_event_id varchar(180) NOT NULL,
 payload_sha256 char(64) NOT NULL, signature_verified boolean NOT NULL DEFAULT false,
 processed_at timestamptz, received_at timestamptz NOT NULL DEFAULT now(),
 UNIQUE(provider,provider_event_id)
);
CREATE TABLE IF NOT EXISTS commerce_inventory_reservations (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id uuid NOT NULL,
 quote_id uuid NOT NULL REFERENCES commerce_quotes(id), sku_id uuid NOT NULL,
 warehouse_id uuid NOT NULL, qty integer NOT NULL CHECK(qty>0),
 status varchar(20) NOT NULL CHECK(status IN('ACTIVE','CONSUMED','RELEASED','EXPIRED')),
 expires_at timestamptz NOT NULL, created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_reservations_active
 ON commerce_inventory_reservations(tenant_id,sku_id,warehouse_id,expires_at)
 WHERE status='ACTIVE';
CREATE TABLE IF NOT EXISTS commerce_outbox (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id uuid NOT NULL,
 aggregate_type varchar(64) NOT NULL, aggregate_id uuid NOT NULL,
 event_type varchar(120) NOT NULL, schema_version integer NOT NULL,
 payload jsonb NOT NULL, occurred_at timestamptz NOT NULL DEFAULT now(),
 dispatched_at timestamptz, attempts integer NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_outbox_pending ON commerce_outbox(occurred_at)
 WHERE dispatched_at IS NULL;
CREATE TABLE IF NOT EXISTS ai_action_approvals (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), tenant_id uuid NOT NULL,
 actor_id uuid NOT NULL, agent_run_id uuid NOT NULL,
 tool_name varchar(100) NOT NULL, action_hash char(64) NOT NULL,
 payload_json jsonb NOT NULL, status varchar(20) NOT NULL,
 expires_at timestamptz NOT NULL, decided_by uuid,
 decided_at timestamptz, created_at timestamptz NOT NULL DEFAULT now(),
 CHECK(status IN ('PENDING','APPROVED','REJECTED','EXPIRED','CONSUMED'))
);
CREATE INDEX IF NOT EXISTS idx_approval_pending ON ai_action_approvals(tenant_id,actor_id,expires_at)
 WHERE status='PENDING';