const jwt = require('jsonwebtoken');

const generateToken = (payload) => {
    const secretKey = 'J|WSi14Jn>VaUam&7&Z?=vG=HkquWe';
    const options = {
        expiresIn: '2h',
    };

    const token = jwt.sign(payload, secretKey, options);
    return token;
};

module.exports = {
    generateToken,
};