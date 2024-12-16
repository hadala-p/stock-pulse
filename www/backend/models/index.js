const User = require("./User");
const Prediction = require("./Prediction");
const DailyPrediction = require("./DailyPrediction");

module.exports = {
    initialize(sequelize) {
        const userModel = User.initialize(sequelize);
        const predictionModel = Prediction.initialize(sequelize);
        const dailyPredictionModel = DailyPrediction.initialize(sequelize);

        userModel.hasMany(predictionModel);
        predictionModel.belongsTo(userModel);
        dailyPredictionModel.belongsTo(userModel);
    }
};