CREATE TABLE IF NOT EXISTS user_wallet(
    id bigint primary key generated always as identity,
    user_id bigint not null unique,
    address text not null,
    public bool not null default false
);

CREATE TABLE IF NOT EXISTS NFTS(
    id bigint primary key generated always as identity,
    collection_address text not null unique,
    collection_name text not null
);

CREATE TABLE IF NOT EXISTS connected_servers(
    id bigint primary key generated always as identity,
    server_id bigint not null unique,
    role_id bigint not null,
    nft_id bigint not null references NFTS (id)
);