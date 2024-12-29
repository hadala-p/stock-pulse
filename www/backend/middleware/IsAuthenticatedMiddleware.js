const User = require('../models/User.js');
const jwt = require('jsonwebtoken');

module.exports = {
    check: (req, res, next) => {
        const token = req.headers.authorization;
        const decodedUser = jwt.decode(token);

        if (decodedUser === null || decodedUser.exp < Date.now() / 1000) {
            return res.status(401).json({
                status: false,
                error: "Unauthorized",
            });
        }

        User.findUserByID(decodedUser.id).then((user) => {
            if (!user) {
                return res.status(403).json({
                  status: false,
                  error: "Invalid access token provided, please login again.",
                });
            } else {
                req.user = { id: user.id };
                next();
            }
        }).catch(err => {
            console.error(err);
            return res.status(500).json({
                status: false,
                error: "Internal Server Error",
            });
        });
    }
};
