const { DataTypes } = require("sequelize");
const { getPublicPredictions } = require("../controllers/PredictionController");

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
        type: DataTypes.STRING,
        allowNull: false,
    },
    predictedData: {
        type: DataTypes.STRING,
        allowNull: false,
    },
};

module.exports = {
    initialize: (sequelize) => {
        this.model = sequelize.define("Prediction", Prediction);
        this.model.belongsTo(User);
        User.hasMany(this.model);
    },

    postPrediction: (owner, companyName, baseData, predictedData) => {
        return this.model.create({
            userId: owner.id,
            companyName: companyName,
            baseData: baseData,
            predictedData: predictedData,
        });
    },

    getPublicPredictions: () => {
        return this.model.findAll({ 
            where: {
                userId: null,
            }
        });
    },

    getPredictionsOf: (user) => {
        return this.model.findAll({
            where: {
                userId: user.id,
            },
        });
    },
};