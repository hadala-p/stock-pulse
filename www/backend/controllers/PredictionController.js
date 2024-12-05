const axios = require('axios');
const Prediction = require('../models/Prediction');
const jwt = require('jsonwebtoken');
const predictURL = 'http://localhost:5000/predict';

module.exports = {
    getPublicPredictions: (req, res) => { 
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
        const { companyName, baseData, predictionStartOffset, predictionDays } = req.body;
        baseData.reverse();
        
        axios({
            method: 'post',
            url: predictURL,
            data: {
              days: predictionDays,
              offset: predictionStartOffset,
              showPlot: false,
              data: baseData
            }
        }).then(response => {
            if (response.status !== 200) 
            {
                return res.status(500).json({
                    status: false,
                    error: 'Prediction failed',
                });
            }
            
            let predictionStartIndex = baseData.length - predictionStartOffset;
            Prediction.postPrediction(user, companyName, response.data.averageLoss, predictionStartIndex, baseData, response.data.data)
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
        }).catch((err) => {
            return res.status(500).json({
                status: false,
                error: err,
            });
        });
    },
};
