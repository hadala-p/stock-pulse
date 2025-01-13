const User = require("./User");
const Prediction = require("./Prediction");
const DailyPrediction = require("./DailyPrediction");
const Favorites = require("./Favorites");

module.exports = {
    initialize(sequelize) {
        const userModel = User.initialize(sequelize);
        const predictionModel = Prediction.initialize(sequelize);
        const dailyPredictionModel = DailyPrediction.initialize(sequelize);
        const favoritesModel = Favorites.initialize(sequelize);

        userModel.hasMany(predictionModel);
        predictionModel.belongsTo(userModel);
        dailyPredictionModel.belongsTo(userModel);
        userModel.hasMany(dailyPredictionModel);
        userModel.hasMany(favoritesModel, { foreignKey: 'userId', onDelete: 'CASCADE' });
        favoritesModel.belongsTo(userModel, { foreignKey: 'userId' });
    }
};