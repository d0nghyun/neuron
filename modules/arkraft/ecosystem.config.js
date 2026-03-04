module.exports = {
  apps: [
    // === Default (local dev) ===
    {
      name: "infra",
      script: "docker",
      args: "compose -f arkraft-api/docker-compose.yml up postgres redis minio minio-init pgweb",
      cwd: __dirname,
      interpreter: "none",
      autorestart: false,
    },
    {
      name: "api",
      script: "bash",
      args: "-c 'uv run uvicorn main:app --reload --port 3002'",
      cwd: `${__dirname}/arkraft-api`,
      interpreter: "none",
    },
    {
      name: "web",
      script: "pnpm",
      args: "dev -p 3000",
      cwd: `${__dirname}/arkraft-web`,
      interpreter: "none",
    },

    // === Prod (opt-in: ./pm2.sh prod) ===
    {
      name: "ssm-rds",
      script: "./scripts/ssm-rds.sh",
      cwd: __dirname,
      interpreter: "bash",
      autorestart: true,
      max_restarts: 5,
      restart_delay: 5000,
    },
    {
      name: "pgweb-prod",
      script: "./scripts/pgweb-prod.sh",
      cwd: __dirname,
      interpreter: "bash",
      autorestart: true,
      max_restarts: 10,
      restart_delay: 3000,
    },
  ],
};
