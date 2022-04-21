CREATE TABLE IF NOT EXISTS user_wallet(
    id bigint primary key generated always as identity,
    user_id bigint not null unique,
    address text not null,
    public bool not null default false
);