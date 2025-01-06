const User = require("./User");
const Prediction = require("./Prediction");
const Favorites = require("./Favorites");
const DailyPrediction = require("./DailyPrediction");

module.exports = {
    initialize(sequelize) {
        const userModel = User.initialize(sequelize);
        const predictionModel = Prediction.initialize(sequelize);
        const favoritesModel = Favorites.initialize(sequelize);
        const dailyPredictionModel = DailyPrediction.initialize(sequelize);

        userModel.hasMany(predictionModel);
        predictionModel.belongsTo(userModel);

        userModel.hasMany(favoritesModel, { foreignKey: 'userId', onDelete: 'CASCADE' });
        favoritesModel.belongsTo(userModel, { foreignKey: 'userId' });

        dailyPredictionModel.belongsTo(userModel);
        userModel.hasMany(dailyPredictionModel);

        return {
            userModel,
            predictionModel,
            favoritesModel,
            dailyPredictionModel,
        };
    },
};
