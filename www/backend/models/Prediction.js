const { DataTypes } = require("sequelize");

const Prediction = {
    id: {
        type: DataTypes.INTEGER,
        autoIncrement: true,
        primaryKey: true,
    },
    companyName: {
        type: DataTypes.STRING,
        allowNull: false,
    },
    baseData: {
        type: DataTypes.JSON,
        allowNull: false,
    },
    predictedData: {
        type: DataTypes.JSON,
        allowNull: false,
    },
};

module.exports = {
    initialize(sequelize) {
        this.model = sequelize.define("Prediction", Prediction);
        return this.model;
    },

    postPrediction(owner, companyName, baseData, predictedData) {
        return this.model.create({
            UserId: owner.id,
            companyName: companyName,
            baseData: baseData,
            predictedData: predictedData,
        });
    },

    getPublicPredictions() {
        return this.model.findAll({ 
            where: {
                UserId: null,
            }
        });
    },

    getPredictionsOf(user) {
        return this.model.findAll({
            where: {
                UserId: user.id,
            },
        });
    },
};