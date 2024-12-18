const axios = require('axios');
const Prediction = require('../models/Prediction');
const DailyPrediction = require('../models/DailyPrediction');
const jwt = require('jsonwebtoken');
const yahooFinance = require('yahoo-finance2').default;
const predictURL = 'http://localhost:5000/predict';

const calculateDailyPredictionData = async (companyName) => {
    const today = new Date();
    const threeMonthsAgo = new Date();
    threeMonthsAgo.setMonth(today.getMonth() - 3);
    const queryOptions = {
        period1: threeMonthsAgo.toISOString().split('T')[0],
        interval: '1d',
    };
    try {
        const quotes = await yahooFinance.historical(companyName, queryOptions);
        const closingPrices = quotes.map(quote => quote.close);
        if (closingPrices.length < 62) {
            throw new Error('Not enough data points. Need at least 62 closing prices.');
        }
        const validClosingPrices = closingPrices.reverse().slice(0, 62);
        const response = await getLSTMPrediction(validClosingPrices, 30, 0, false, false);
        return {
            baseData: validClosingPrices,
            predictedData: response,
        };
    } catch (err) {
        console.error(`Error fetching data for ${companyName}:`, err);
        throw err;
    }
};

const updatePrediction = async (companyName, data) => {
    try {
        const publicPredictions = await Prediction.getPublicPredictions();
        const foundPrediction = publicPredictions.find(prediction => prediction.companyName === companyName);
        if (foundPrediction) {
            await Prediction.putPrediction(foundPrediction.id, data.baseData, data.predictedData);
        } else {
            await Prediction.postPrediction(null, companyName, 0, 0, data.baseData, data.predictedData);
        }
        return true;
    } catch (err) {
        console.error(`Error updating prediction for ${companyName}:`, err);
        return false;
    }
};

const postDailyPrediction = async (req, res) => {
    const token = req.headers.authorization;
    const user = jwt.decode(token);
    const { companyName } = req.body;

    try {
        const data = await calculateDailyPredictionData(companyName);
        const predictionUpdated = await updatePrediction(companyName, data);
        const dailyPredictionUpdated = await DailyPrediction.postDailyPrediction(user, companyName);

        if (predictionUpdated && dailyPredictionUpdated) {
            return res.status(200).json({
                status: true,
                result: 'Prediction created successfully.',
            });
        } else {
            return res.status(500).json({
                status: false,
                error: 'Prediction creation failed.',
            });
        }
    } catch (err) {
        return res.status(500).json({
            status: false,
            error: err.message,
        });
    }
};

const getLSTMPrediction = (data, days, offset, showPlot, flipData) => 
    {
        return axios({
            method: 'post',
            url: predictURL,
            data: {
              days: days,
              offset: offset,
              showPlot: showPlot,
              data: data,
              flipData: flipData,
            }
        }).then(response => {
            if (response.status !== 200) 
            {
                throw new Error('Prediction failed.');
            }
            return response.data;
        }).catch((err) => {
            throw new Error(err);
        });
    };

module.exports = {
    calculateDailyPredictionData,
    postDailyPrediction,
    getLSTMPrediction,

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

    getMyDailyPredictions: (req, res) => {
        const token = req.headers.authorization;
        const user = jwt.decode(token);
        DailyPrediction.getDailyPredictionsOf(user)
            .then(async (predictions) => {
                await predictions.forEach(async (prediction) => {
                    if (new Date() - prediction.lastPredictionUpdate > 12 * 60 * 60 * 1000) {
                        let predictedData = await calculateDailyPredictionData(prediction.companyName);
                        let putPredictionResponse = await Prediction.putPrediction(prediction.id, predictedData.baseData, predictedData.predictedData);
                        if (!putPredictionResponse) {
                            return res.status(500).json({
                                status: false,
                                error: 'Failed to update daily prediction.',
                        });
                    }
                };
                
                let dailyPredictions = [];
                let publicPredictions = await Prediction.getPublicPredictions();
                publicPredictions.forEach((publicPrediction) => {
                    predictions.forEach((dailyPrediction) => {
                        if (publicPrediction.companyName === dailyPrediction.companyName) {
                            dailyPredictions.push(publicPrediction);
                        }
                    });
                });

                return res.status(200).json({
                    status: true,
                    result: dailyPredictions,
                });
            }).catch((err) => {
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

    postPrediction: (req, res) => {
        const token = req.headers.authorization;
        const user = jwt.decode(token);
        const { companyName, baseData, predictionStartOffset, predictionDays } = req.body;
        getLSTMPrediction(baseData, predictionDays, predictionStartOffset, false, true)
        .then(response => {
            let predictionStartIndex = baseData.length - predictionStartOffset;
            Prediction.postPrediction(user, companyName, response.averageLoss, predictionStartIndex, baseData, response.data)
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
