# openbudgetsac.org

## Development Environment Setup

1. Make sure Ruby is installed (tested on 2.4.0).
2. Install `bundler` and dependencies, then deploy the static site to localhost:
  ```bash
  gem install bundler --version 1.15.3
  bundle install
  bundle exec jekyll serve
  ```
