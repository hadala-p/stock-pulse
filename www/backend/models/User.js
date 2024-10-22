const { DataTypes } = require("sequelize");

const User = {
    id: {
        type: DataTypes.INTEGER,
        autoIncrement: true,
        primaryKey: true,
    },
    email: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true,
    },
    password: {
        type: DataTypes.STRING,
        allowNull: false,
    },
};

module.exports = {
    initialize: (sequelize) => {
        this.model = sequelize.define("User", User);
    },

    createUser: (user) => {
        return this.model.create(user);
    },

    findUserByEmail: (email) => {
        return this.model.findOne({
            where: {
                email: email,
            },
        });
    },
};