FROM node:16

# throw errors if Gemfile has been modified since Gemfile.lock
# RUN bundle config --global frozen 1

WORKDIR /usr/src/app/

COPY _src/package*.json .
RUN npm install --force

# RUN ln -s _src/node_modules /
RUN node_modules/.bin/webpack --config _src/webpack.config.js -p

EXPOSE 8011

COPY . .

CMD ["npx", "npx @11ty/eleventy", "--serve", "--port", "8011"]
