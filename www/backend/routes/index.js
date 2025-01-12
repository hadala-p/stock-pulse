const UserRoutes = require("./UserRoutes");
const AuthenticationRoutes = require("./AuthenticationRoutes");
const PredictionRoutes = require("./PredictionRoutes");
const IsAuthenticatedMiddleware = require('../middleware/IsAuthenticatedMiddleware');

module.exports = {
    initialize(app) {
        app.use("/user", UserRoutes);
        app.use("/auth", AuthenticationRoutes);
        app.use("/prediction", IsAuthenticatedMiddleware.check, PredictionRoutes);
    }
};
