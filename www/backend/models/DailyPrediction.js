const { DataTypes } = require("sequelize");

const DailyPrediction = {
    id: {
        type: DataTypes.INTEGER,
        autoIncrement: true,
        primaryKey: true,
    },
    companyName: {
        type: DataTypes.STRING,
        allowNull: false,
    },
    lastPredictionUpdate: {
        type: DataTypes.DATE,
        allowNull: false,
    }
};

module.exports = {
    initialize(sequelize) {
        this.model = sequelize.define("DailyPrediction", Prediction);
        return this.model;
    },

    postDailyPrediction(owner, companyName) {
        return this.model.create({
            UserId: owner.id,
            companyName: companyName,
            lastPredictionUpdate: new Date(),
        });
    },

    putDailyPrediction(id, lastPredictionUpdate) {
        return this.model.update({
            lastPredictionUpdate: lastPredictionUpdate,
        }, {
            where: {
                id: id,
            },
        });
    },

    getDailyPredictionsOf(user) {
        return this.model.findAll({
            where: {
                UserId: user.id,
            },
        });
    },
};