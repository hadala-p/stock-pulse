const User = require("./User");
const Prediction = require("./Prediction");

module.exports = {
    initialize(sequelize) {
        const userModel = User.initialize(sequelize);
        const predictionModel = Prediction.initialize(sequelize);

        userModel.hasMany(predictionModel);
        predictionModel.belongsTo(userModel);
    }
};