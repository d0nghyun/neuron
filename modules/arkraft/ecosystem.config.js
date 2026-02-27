module.exports = {
  apps: [
    {
      name: "infra",
      script: "docker",
      args: "compose -f arkraft-api/docker-compose.yml up postgres redis minio minio-init pgweb",
      cwd: __dirname,
      interpreter: "none",
      autorestart: false,
    },
    {
      name: "web",
      script: "pnpm",
      args: "dev -p 3000",
      cwd: `${__dirname}/arkraft-web`,
      interpreter: "none",
    },
    {
      name: "api",
      script: "bash",
      args: "-c 'uv run uvicorn main:app --reload --port 3002'",
      cwd: `${__dirname}/arkraft-api`,
      interpreter: "none",
    },
  ],
};
