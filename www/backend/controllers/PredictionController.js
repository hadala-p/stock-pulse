const axios = require('axios');
const Prediction = require('../models/Prediction');
const DailyPrediction = require('../models/DailyPrediction');
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

    postDailyPrediction: (req, res) => {
        const token = req.headers.authorization;
        const user = jwt.decode(token);
        const { companyName } = req.body;

        // get yahoo data and update it
    },

    getDailyPredictionData(companyName) {
        // get yahoo finance data an post/put it
    },

    getMyDailyPredictions: (req, res) => {
        const token = req.headers.authorization;
        const user = jwt.decode(token);

        DailyPrediction.getDailyPredictionsOf(user)
            .then(async (predictions) => {
                let dailyPredictions = [];
                await predictions.forEach(async (prediction) => {
                    if (new Date() - prediction.lastPredictionUpdate > 12 * 60 * 60 * 1000) {
                        await getDailyPredictionData(prediction.companyName);
                    }
                });

                let publicPredictions = await Prediction.getPublicPredictions();
                publicPredictions.forEach((publicPrediction) => {
                    dailyPredictions.push(publicPredictions.find((prediction) => prediction.companyName === publicPrediction.companyName));
                });

                return res.status(200).json({
                    status: true,
                    result: dailyPredictions,
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
        
        axios({
            method: 'post',
            url: predictURL,
            data: {
              days: predictionDays,
              offset: predictionStartOffset,
              showPlot: false,
              data: baseData,
              flipData: true,
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
