const bcrypt = require('bcrypt');

module.exports = {
    encryptPassword: (password) => bcrypt.genSalt(12)
                                       .then(salt => bcrypt.hash(password, salt))
                                       .then(hash => hash),

    verifyPassword: (password, encryptedPassword) => bcrypt.compare(password, encryptedPassword)
                                                           .then(resp => resp)
}