FROM cgr.dev/chainguard/nginx:latest-dev

COPY nginx.conf /etc/nginx/nginx.conf
COPY cert.pem /etc/nginx/conf.d/cert.pem
COPY key.pem /etc/nginx/conf.d/key.pem

USER root
# Ensure nginx user can read the cert files
RUN chown nginx:nginx /etc/nginx/conf.d/cert.pem /etc/nginx/conf.d/key.pem && chmod 400 /etc/nginx/conf.d/cert.pem /etc/nginx/conf.d/key.pem

USER nginx