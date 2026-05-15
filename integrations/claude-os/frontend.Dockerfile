FROM node:22-slim

ARG CLAUDE_OS_REPO=https://github.com/brobertsaz/claude-os.git
ARG CLAUDE_OS_COMMIT=ee7b62bc5bf36541018a1c14592bcac2b59022f9

ENV NODE_ENV=development

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        git \
        python3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt
RUN git clone "${CLAUDE_OS_REPO}" claude-os \
    && cd claude-os \
    && git checkout "${CLAUDE_OS_COMMIT}"

WORKDIR /opt/claude-os/frontend
RUN npm ci

COPY frontend-entrypoint.sh /usr/local/bin/claude-os-frontend-entrypoint
RUN chmod +x /usr/local/bin/claude-os-frontend-entrypoint

ENV CLAUDE_OS_API_INTERNAL_URL=http://claude-os:8051
ENV VITE_API_URL=http://localhost:8051

EXPOSE 5173

ENTRYPOINT ["claude-os-frontend-entrypoint"]
