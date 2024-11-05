const User = require('../models/User.js');
const jwt = require('jsonwebtoken');

module.exports = {
    check: (req, res, next) => {
        const token = req.headers.authorization;
        const user = jwt.decode(token);
        console.log(user)
        if (user === null || user.exp < Date.now() / 1000) 
        {
            return res.status(401).json({
                status: false,
                error: "Unauthorized",
            });
        }

        User.findUserByID(user.id).then((user) => {
            if (!user) {
              return res.status(403).json({
                status: false,
                error: "Invalid access token provided, please login again.",
              });
            }
            else {
                next();
            }
        });
    }
};