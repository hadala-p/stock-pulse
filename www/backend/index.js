const express = require('express');
const app = express();
app.use(express.json())

const port = process.env.PORT || 3000;

app.listen(port, () => {
  console.log("Server Listening on PORT:", port);
});

const { Sequelize } = require('sequelize');
const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: './db.sqlite',
})

sequelize.sync({ alter: true });
const User = require("./models/User");
User.initialize(sequelize);

const UserRoutes = require("./routes/UserRoutes");
const AuthenticationRoutes = require("./routes/AuthenticationRoutes");
const PredictionRoutes = require("./routes/PredictionRoutes");
app.use("/user", UserRoutes);
app.use("/auth", AuthenticationRoutes);
app.use("/prediction", PredictionRoutes);