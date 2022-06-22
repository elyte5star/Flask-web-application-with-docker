FROM nginx:alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY ./conf/nginx.conf /etc/nginx
COPY ./ssl/ /etc/ssl_certs
WORKDIR /
RUN echo "hello"
