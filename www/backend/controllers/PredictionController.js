const User = require('../models/Prediction');
const jwt = require('jsonwebtoken');

module.exports = {
    getPublicPredictions: (req, res) => { 
        const token = req.headers.authorization;
        const user = jwt.decode(token);

        if (user === null || user === undefined || user.exp < Date.now()) 
        {
            return res.status(401).json({
                status: false,
                error: "Unauthorized",
            });
        }

        Prediction.getPublicPredictions()
            .then((predictions) => {
                return res.status(200).json({
                    status: true,
                    result: predictions,
                });
            })
            .catch((err) => {
                return res.status(500).json({
                    status: false,
                    error: err,
                });
            });
    },

    getMyPredictions: (req, res) => {
        const token = req.headers.authorization;
        const user = jwt.decode(token);

        if (user === null || user === undefined || user.exp < Date.now()) 
        {
            return res.status(401).json({
                status: false,
                error: "Unauthorized",
            });
        }

        Prediction.getPredictionsOf(user)
            .then((predictions) => {
                return res.status(200).json({
                    status: true,
                    result: predictions,
                });
            })
            .catch((err) => {
                return res.status(500).json({
                    status: false,
                    error: err,
                });
            });
    },

    postPrediction: (req, res) => {
        const token = req.headers.authorization;
        const user = jwt.decode(token);

        if (user === null || user.exp < Date.now()) 
        {
            return res.status(401).json({
                status: false,
                error: "Unauthorized",
            });
        }

        const { companyName, baseData, predictedData } = req.body;

        Prediction.postPrediction(user, companyName, baseData, predictedData)
            .then((prediction) => {
                return res.status(200).json({
                    status: true,
                    result: prediction,
                });
            })
            .catch((err) => {
                return res.status(500).json({
                    status: false,
                    error: err,
                });
            });
    },
};
