const Favorites = require('../models/Favorites');
const axios = require('axios');
const jwt = require('jsonwebtoken');

const predictionEndpoint = 'http://localhost:3000/prediction/my';

module.exports = {
    async addFavourite(req, res) {
        try {
            const { stockId } = req.body;
            const userId = req.user.id;

            const favourite = await Favorites.model.create({ userId, stockId });
            res.status(201).json({ message: "Added to favorites", favourite });
        } catch (err) {
            res.status(500).json({ error: "Failed to add to favorites", details: err });
        }
    },

    async removeFavourite(req, res) {
        try {
            const { id } = req.params;

            const deleted = await Favorites.model.destroy({ where: { id } });

            if (deleted) {
                res.status(200).json({ message: "Removed from favorites" });
            } else {
                res.status(404).json({ error: "Favourite not found" });
            }
        } catch (err) {
            res.status(500).json({ error: "Failed to remove favourite", details: err });
        }
    },

    async getFavorites(req, res) {
        try {
            const favorites = await Favorites.model.findAll({
                where: { userId: req.user.id },
            });

            const token = req.headers.authorization;

            const detailedFavorites = await Promise.all(favorites.map(async (fav) => {
                try {
                    const predictionResponse = await axios.get(predictionEndpoint, {
                        headers: {
                            Authorization: token,
                        },
                    });

                    // Find predictions for the current stockId
                    const predictions = predictionResponse.data.result.filter(
                        (prediction) => prediction.id === fav.stockId
                    );

                    if (predictions.length > 0) {
                        return {
                            id: fav.id,
                            stockId: fav.stockId,
                            userId: fav.userId,
                            predictions: predictions.map((pred) => ({
                                companyName: pred.companyName,
                                averageLoss: pred.averageLoss,
                                predictionStartIndex: pred.predictionStartIndex,
                                baseData: pred.baseData,
                                predictedData: pred.predictedData,
                                createdAt: pred.createdAt,
                                updatedAt: pred.updatedAt,
                            })),
                        };
                    } else {
                        return {
                            id: fav.id,
                            stockId: fav.stockId,
                            userId: fav.userId,
                            predictions: [],
                        };
                    }
                } catch (err) {
                    return {
                        id: fav.id,
                        stockId: fav.stockId,
                        userId: fav.userId,
                        error: "Failed to fetch prediction",
                        details: err.message,
                    };
                }
            }));

            res.status(200).json({
                status: true,
                favorites: detailedFavorites,
            });
        } catch (err) {
            res.status(500).json({
                status: false,
                error: "Failed to fetch favorites",
                details: err,
            });
        }
    },
};
