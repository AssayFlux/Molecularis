import assert from "node:assert/strict";
import test from "node:test";

import {
  constantTimeTokenMatch,
  createNodeServer,
  isLoopbackHost,
  readConfig,
} from "./server.mjs";

test("worker defaults to loopback and docking disabled", () => {
  const config = readConfig({});
  assert.equal(config.host, "127.0.0.1");
  assert.equal(config.enabled, false);
  assert.equal(config.remote, false);
});

test("remote bind requires TLS and valid port", () => {
  assert.throws(() => readConfig({ KINETICS_NODE_HOST: "0.0.0.0" }), /requires TLS/);
  assert.throws(() => readConfig({ KINETICS_NODE_PORT: "70000" }), /PORT/);
  assert.throws(
    () => readConfig({
      KINETICS_NODE_ALLOW_DOCKING: "true",
      KINETICS_NODE_AUTH_TOKEN: "short",
    }),
    /32-character/,
  );
});

test("remote bind accepts explicit TLS configuration", () => {
  const config = readConfig({
    KINETICS_NODE_HOST: "0.0.0.0",
    KINETICS_NODE_TLS_CERT: "/tmp/cert.pem",
    KINETICS_NODE_TLS_KEY: "/tmp/key.pem",
  });
  assert.equal(config.remote, true);
});

test("authentication comparison rejects missing, short and mismatched tokens", () => {
  const token = "a".repeat(48);
  assert.equal(constantTimeTokenMatch(token, token), true);
  assert.equal(constantTimeTokenMatch(token, "b".repeat(48)), false);
  assert.equal(constantTimeTokenMatch(token, "short"), false);
  assert.equal(constantTimeTokenMatch(token, undefined), false);
});

test("only loopback hostnames are accepted without TLS", () => {
  assert.equal(isLoopbackHost("127.0.0.1"), true);
  assert.equal(isLoopbackHost("::1"), true);
  assert.equal(isLoopbackHost("localhost"), true);
  assert.equal(isLoopbackHost("0.0.0.0"), false);
  assert.equal(isLoopbackHost("192.168.1.20"), false);
});

test("health route reports disabled docking and MD", async () => {
  const server = createNodeServer({
    env: {
      KINETICS_NODE_HOST: "127.0.0.1",
      KINETICS_NODE_ALLOW_DOCKING: "false",
    },
  });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  try {
    const address = server.address();
    const response = await fetch("http://127.0.0.1:" + address.port + "/health");
    const body = await response.json();
    assert.equal(response.status, 200);
    assert.equal(body.docking_enabled, false);
    assert.equal(body.md_enabled, false);
    assert.equal(body.bind_scope, "loopback_only");
  } finally {
    await new Promise((resolve, reject) => {
      server.close((error) => (error ? reject(error) : resolve()));
    });
  }
});

test("disabled worker refuses docking requests", async () => {
  const server = createNodeServer({
    env: {
      KINETICS_NODE_HOST: "127.0.0.1",
      KINETICS_NODE_ALLOW_DOCKING: "false",
    },
  });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  try {
    const address = server.address();
    const response = await fetch("http://127.0.0.1:" + address.port + "/v1/docking", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: "{}",
    });
    assert.equal(response.status, 503);
  } finally {
    await new Promise((resolve, reject) => {
      server.close((error) => (error ? reject(error) : resolve()));
    });
  }
});


test("enabled worker rejects unauthenticated docking requests before spawning", async () => {
  const server = createNodeServer({
    env: {
      KINETICS_NODE_HOST: "127.0.0.1",
      KINETICS_NODE_ALLOW_DOCKING: "true",
      KINETICS_NODE_AUTH_TOKEN: "x".repeat(48),
    },
    spawnProcess: () => {
      throw new Error("worker must not spawn without authentication");
    },
  });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  try {
    const address = server.address();
    const response = await fetch("http://127.0.0.1:" + address.port + "/v1/docking", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: "{}",
    });
    assert.equal(response.status, 401);
  } finally {
    await new Promise((resolve, reject) => {
      server.close((error) => (error ? reject(error) : resolve()));
    });
  }
});


test("Molecularis environment names take precedence while legacy names remain supported", () => {
  assert.equal(readConfig({ MOLECULARIS_NODE_PORT: "9001", KINETICS_NODE_PORT: "9002" }).port, 9001);
  assert.equal(readConfig({ KINETICS_NODE_PORT: "9002" }).port, 9002);
});
