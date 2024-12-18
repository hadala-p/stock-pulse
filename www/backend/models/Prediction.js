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
    averageLoss: {
        type: DataTypes.FLOAT,
        allowNull: false,
        defaultValue: 0,
    },
    predictionStartIndex: {
        type: DataTypes.INTEGER,
        allowNull: false,
        defaultValue: 0,
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

    postPrediction(owner, companyName, averageLoss, predictionStartIndex, baseData, predictedData) {
        let userId = null;
        if (owner !== null) 
        {
            userId = owner.id;
        }
        
        return this.model.create({
            UserId: userId,
            companyName: companyName,
            averageLoss: averageLoss,
            predictionStartIndex: predictionStartIndex,
            baseData: baseData,
            predictedData: predictedData,
        });
    },

    putPrediction(id, baseData, predictedData) {
        let userId = null;
        if (owner !== null) {
            userId = owner.id;
        }

        return this.model.update(
            {
                baseData: baseData,
                predictedData: predictedData,
            },
            {
                where: {
                    id: id,
                },
            }
        );
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