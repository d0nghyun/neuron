/**
 * PM2 Ecosystem Configuration for Arkraft
 *
 * Usage:
 *   pm2 start ecosystem.config.js            # Start all (infra + apps)
 *   pm2 start ecosystem.config.js --only web,api  # Start specific apps
 *   pm2 logs                                 # View all logs
 *   pm2 restart all                          # Restart all
 *   pm2 stop all && docker compose down      # Stop all
 *   pm2 delete all                           # Remove all from PM2
 *
 * Services:
 *   - infra: Docker Compose (Redis, PostgreSQL, MinIO)
 *   - web: Next.js frontend (port 3000)
 *   - api: FastAPI backend (port 3002)
 *   - agent-manager: AI Agent Management System (arq worker)
 *   - arq-ui: Queue dashboard (port 3003)
 */

module.exports = {
  apps: [
    {
      name: 'infra',
      script: 'docker',
      args: 'compose up -d',
      autorestart: false,
      watch: false,
    },
    {
      name: 'web',
      cwd: './arkraft-web',
      script: 'pnpm',
      args: 'dev -p 3000',
      env: {
        NODE_ENV: 'development',
      },
      watch: false,
    },
    {
      name: 'api',
      cwd: './arkraft-api',
      script: 'uv',
      args: 'run uvicorn main:app --reload --port 3002',
      env: {
        PYTHONUNBUFFERED: '1',
      },
      watch: false,
    },
    {
      name: 'agent-manager',
      cwd: './arkraft-agent-manager',
      script: 'uv',
      args: 'run watchfiles "python -m src.main" src',
      env: {
        PYTHONUNBUFFERED: '1',
        LOCAL_MODE: 'true',
      },
      watch: false,
    },
    {
      name: 'arq-ui',
      script: 'docker',
      args: 'run --rm --name arq-ui --network arkraft_default -p 3003:8000 -e REDIS_HOST=redis -e REDIS_PORT=6379 antonk0/arq-ui',
      autorestart: true,
      watch: false,
    },
  ],
};
