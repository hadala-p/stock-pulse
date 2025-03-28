const express = require('express');
const cors = require('cors');
const app = express();
app.use(express.json())
app.use(cors());

const port = process.env.PORT || 3000;

app.listen(port, () => {
  console.log("Server Listening on PORT:", port);
});

const { Sequelize } = require('sequelize');
const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: './db.sqlite',
})

const models = require('./models/index.js');
models.initialize(sequelize);
sequelize.sync({ force: false });

const routes = require('./routes/index.js');
routes.initialize(app);