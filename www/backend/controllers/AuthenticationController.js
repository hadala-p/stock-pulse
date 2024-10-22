const jsonWebTokenController = require('./JsonWebTokenController');
const bcryptController = require('./BcryptController');
const User = require('../models/User');

module.exports = {
    register: (req, res) => {
        const payload = req.body;
        bcryptController.encryptPassword(payload.password)
        .then((encryptedPassword) => {
            payload.password = encryptedPassword;
        })
        .then(() => {
            User.createUser(payload)
            .then((user) => {
                payload.id = user.id;
                const accessToken = jsonWebTokenController.generateToken(payload);

                return res.status(200).json({
                    status: true,
                    result: {
                        user: user.toJSON(),
                        token: accessToken,
                    },
                });
            }) 
            .catch((err) => {
                return res.status(500).json({
                    status: false,
                    error: err,
                });
            });
        });
    },
    login: (req, res) => {
        const payload = req.body;
        User.findUserByEmail(payload.email)
            .then(foundUser => {
                if (foundUser === null) {
                    return res.status(404).json({
                        status: false,
                        error: "Provided email has no associated account",
                    });
                }

                if (!bcryptController.verifyPassword(payload.password, foundUser.password)) {
                    return res.status(404).json({
                        status: false,
                        error: "Incorrect password",
                    });
                }
                
                payload.password = foundUser.password;
                payload.id = foundUser.id;
                const accessToken = jsonWebTokenController.generateToken(payload);
                return res.status(200).json({
                    status: true,
                    result: {
                        user: foundUser.toJSON(),
                        token: accessToken,
                    },
                });
            })
    },
};     