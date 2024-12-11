# build stage
FROM node:20.18.0-alpine as build-stage
WORKDIR /app
COPY ./academic_journal_frontend/package*.json ./
RUN npm install
COPY ./academic_journal_frontend .
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]