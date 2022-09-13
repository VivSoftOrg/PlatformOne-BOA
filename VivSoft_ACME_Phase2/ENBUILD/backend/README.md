# vivsoft-ui
Repository for all platforms api

- ES6 support via [babel](https://babeljs.io)
- REST resources as middleware via [resource-router-middleware](https://github.com/developit/resource-router-middleware)
- CORS support via [cors](https://github.com/troygoode/node-cors)
- Body Parsing via [body-parser](https://github.com/expressjs/body-parser)

> Using [Mongoose](https://github.com/Automattic/mongoose), we can automatically expose your Models as REST resources using [restful-mongoose](https://git.io/restful-mongoose).


# Installation
1. Install nvm `curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.32.1/install.sh | bash`
2. Install Nodejs version v14.2 `nvm install 14.2.0`
3. Run `npm install`
4. Run `npm run dev`

# Docker
1. Install docker
2. Run `docker-compose -f docker-compose.yml up -d --build`
3. Navigate to `http://localhost:8080/api`

