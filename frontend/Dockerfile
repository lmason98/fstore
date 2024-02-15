FROM node:18

WORKDIR /frontend

COPY . /frontend
# COPY ./entrypoint.sh /frontend/entrypoint.sh

# RUN npm install

EXPOSE 3000

RUN chmod +x /frontend/entrypoint.sh

CMD ["/frontend/entrypoint.sh"]