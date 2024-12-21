const User = require('../models/User.js');
const jwt = require('jsonwebtoken');

module.exports = {
    check: async (req, res, next) => {
        try {
            const token = req.headers.authorization;

            if (!token) {
                return res.status(401).json({
                    status: false,
                    error: "Unauthorized: No token provided",
                });
            }

            const userData = jwt.decode(token);
            if (!userData || userData.exp < Date.now() / 1000) {
                return res.status(401).json({
                    status: false,
                    error: "Unauthorized: Token is expired or invalid",
                });
            }

            const user = await User.findUserByID(userData.id);
            if (!user) {
                return res.status(403).json({
                    status: false,
                    error: "Invalid access token provided, please login again.",
                });
            }

            // Ustawienie użytkownika w `req` dla dalszego użycia
            req.user = user;
            next();
        } catch (err) {
            return res.status(500).json({
                status: false,
                error: "Internal server error",
                details: err.message,
            });
        }
    },
};
