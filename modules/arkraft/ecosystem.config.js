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
      args: 'dev',
      env: {
        NODE_ENV: 'development',
        PORT: 3000,
      },
      watch: false,
    },
    {
      name: 'api',
      cwd: './arkraft-api',
      script: 'uv',
      args: 'run uvicorn arkraft_api.main:app --reload --port 3002',
      env: {
        PYTHONUNBUFFERED: '1',
      },
      watch: false,
    },
    {
      name: 'agent-manager',
      cwd: './arkraft-agent-manager',
      script: 'uv',
      args: 'run python -m src.main',
      env: {
        PYTHONUNBUFFERED: '1',
      },
      watch: false,
    },
  ],
};
