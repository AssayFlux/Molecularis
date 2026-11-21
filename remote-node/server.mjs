import { spawn } from "node:child_process";
import { timingSafeEqual } from "node:crypto";
import { readFileSync } from "node:fs";
import http from "node:http";
import https from "node:https";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
const RUNNER = path.join(ROOT, "scripts", "run_vina_node_job.py");
const MAX_BODY_BYTES = 20 * 1024 * 1024;
const MAX_STDOUT_BYTES = 32 * 1024 * 1024;
const MAX_STDERR_BYTES = 8 * 1024;
const JOB_TIMEOUT_MS = 15 * 60 * 1000;

export function isLoopbackHost(host) {
  return host === "localhost" || host === "127.0.0.1" || host === "::1";
}

export function constantTimeTokenMatch(expected, supplied) {
  if (typeof expected !== "string" || expected.length < 32 || typeof supplied !== "string") {
    return false;
  }
  const left = Buffer.from(expected, "utf8");
  const right = Buffer.from(supplied, "utf8");
  return left.length === right.length && timingSafeEqual(left, right);
}

export function readConfig(env = process.env) {
  // Prefer Molecularis names; retain KINETICS_* aliases for existing deployments.
  const setting = (name) => env[name.replace(/^KINETICS_/, "MOLECULARIS_")] ?? env[name];
  const host = setting("KINETICS_NODE_HOST") || "127.0.0.1";
  const port = Number(setting("KINETICS_NODE_PORT") || "8765");
  const enabled = setting("KINETICS_NODE_ALLOW_DOCKING") === "true";
  const token = setting("KINETICS_NODE_AUTH_TOKEN") || "";
  const remote = !isLoopbackHost(host);
  if (!Number.isInteger(port) || port < 1 || port > 65535) {
    throw new Error("KINETICS_NODE_PORT must be an integer from 1 to 65535");
  }
  if (enabled && token.length < 32) {
    throw new Error("A 32-character KINETICS_NODE_AUTH_TOKEN is required when docking is enabled");
  }
  if (remote && (!setting("KINETICS_NODE_TLS_CERT") || !setting("KINETICS_NODE_TLS_KEY"))) {
    throw new Error("Non-loopback binding requires TLS certificate and key paths");
  }
  return { host, port, enabled, token, remote };
}

function jsonResponse(res, status, body) {
  const bytes = Buffer.from(JSON.stringify(body));
  res.writeHead(status, {
    "content-type": "application/json; charset=utf-8",
    "content-length": bytes.length,
    "cache-control": "no-store",
    "x-content-type-options": "nosniff",
    "referrer-policy": "no-referrer",
  });
  res.end(bytes);
}

async function readBoundedBody(req) {
  const chunks = [];
  let total = 0;
  for await (const chunk of req) {
    total += chunk.length;
    if (total > MAX_BODY_BYTES) {
      const error = new Error("Request exceeds the 20 MiB worker limit");
      error.statusCode = 413;
      throw error;
    }
    chunks.push(chunk);
  }
  return Buffer.concat(chunks, total);
}

export function createNodeServer({ env = process.env, spawnProcess = spawn } = {}) {
  const config = readConfig(env);
  let activeJob = false;

  const handler = async (req, res) => {
    if (req.method === "GET" && req.url === "/health") {
      return jsonResponse(res, 200, {
        status: "ready",
        docking_enabled: config.enabled,
        md_enabled: false,
        bind_scope: config.remote ? "tls_remote" : "loopback_only",
      });
    }
    if (req.method !== "POST" || req.url !== "/v1/docking") {
      return jsonResponse(res, 404, { error: "not_found" });
    }
    if (!config.enabled) {
      return jsonResponse(res, 503, { error: "research_docking_worker_disabled" });
    }
    const authorization = req.headers.authorization || "";
    const supplied = authorization.startsWith("Bearer ")
      ? authorization.slice("Bearer ".length)
      : "";
    if (!constantTimeTokenMatch(config.token, supplied)) {
      return jsonResponse(res, 401, { error: "unauthorized" });
    }
    if (activeJob) {
      return jsonResponse(res, 429, { error: "worker_busy" });
    }
    const contentType = req.headers["content-type"] || "";
    if (!contentType.toLowerCase().startsWith("application/json")) {
      return jsonResponse(res, 415, { error: "application_json_required" });
    }
    const declaredLength = Number(req.headers["content-length"] || "0");
    if (declaredLength > MAX_BODY_BYTES) {
      return jsonResponse(res, 413, { error: "request_too_large" });
    }

    activeJob = true;
    let child;
    let finished = false;
    const finish = (status, body) => {
      if (finished) return;
      finished = true;
      activeJob = false;
      if (!res.writableEnded && !res.destroyed) jsonResponse(res, status, body);
    };
    req.on("aborted", () => {
      if (child && !child.killed) child.kill("SIGKILL");
      finish(499, { error: "client_disconnected" });
    });
    res.on("close", () => {
      if (!res.writableEnded && child && !child.killed) child.kill("SIGKILL");
    });

    try {
      const body = await readBoundedBody(req);
      JSON.parse(body.toString("utf8"));
      const python = setting("KINETICS_PYTHON") || "python3";
      child = spawnProcess(
        python,
        [RUNNER],
        {
          cwd: ROOT,
          shell: false,
          windowsHide: true,
          stdio: ["pipe", "pipe", "pipe"],
          env: {
            PATH: env.PATH || process.env.PATH || "",
            HOME: env.HOME || process.env.HOME || "",
            TMPDIR: env.TMPDIR || "/tmp",
            LANG: env.LANG || "C.UTF-8",
            VIRTUAL_ENV: env.VIRTUAL_ENV || "",
            LD_LIBRARY_PATH: env.LD_LIBRARY_PATH || "",
            PYTHONPATH: [path.join(ROOT, "python"), env.PYTHONPATH || ""].filter(Boolean).join(path.delimiter),
            PYTHONUNBUFFERED: "1",
          },
        },
      );
      const stdout = [];
      const stderr = [];
      let stdoutBytes = 0;
      let stderrBytes = 0;
      let timedOut = false;
      const timeout = setTimeout(() => {
        timedOut = true;
        child.kill("SIGKILL");
      }, JOB_TIMEOUT_MS);
      child.stdout.on("data", (chunk) => {
        stdoutBytes += chunk.length;
        if (stdoutBytes > MAX_STDOUT_BYTES) child.kill("SIGKILL");
        else stdout.push(chunk);
      });
      child.stderr.on("data", (chunk) => {
        if (stderrBytes < MAX_STDERR_BYTES) {
          const remaining = MAX_STDERR_BYTES - stderrBytes;
          const part = chunk.subarray(0, remaining);
          stderr.push(part);
          stderrBytes += part.length;
        }
      });
      child.on("error", (error) => {
        clearTimeout(timeout);
        finish(503, { error: "worker_process_unavailable", detail: error.message.slice(0, 300) });
      });
      child.on("close", (code) => {
        clearTimeout(timeout);
        if (finished) return;
        if (timedOut) return finish(504, { error: "worker_job_timeout" });
        if (stdoutBytes > MAX_STDOUT_BYTES) {
          return finish(502, { error: "worker_result_too_large" });
        }
        if (code !== 0) {
          const detail = Buffer.concat(stderr).toString("utf8").replace(/\s+/g, " ").slice(0, 1000);
          return finish(422, { error: "docking_job_failed", detail });
        }
        try {
          const result = JSON.parse(Buffer.concat(stdout).toString("utf8"));
          return finish(200, result);
        } catch {
          return finish(502, { error: "worker_returned_invalid_json" });
        }
      });
      child.stdin.on("error", () => {});
      child.stdin.end(body);
    } catch (error) {
      const status = Number.isInteger(error?.statusCode) ? error.statusCode : 400;
      finish(status, { error: "invalid_request", detail: String(error?.message || "Invalid request").slice(0, 300) });
    }
  };

  if (config.remote) {
    return https.createServer({
      cert: readFileSync(setting("KINETICS_NODE_TLS_CERT")),
      key: readFileSync(setting("KINETICS_NODE_TLS_KEY")),
    }, handler);
  }
  return http.createServer(handler);
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  const server = createNodeServer();
  const config = readConfig();
  server.listen(config.port, config.host, () => {
    process.stdout.write(
      "Molecularis private research worker listening on " +
      config.host + ":" + config.port + " (docking " +
      (config.enabled ? "enabled" : "disabled") + "; MD disabled)\n",
    );
  });
}
