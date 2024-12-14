const { DataTypes } = require("sequelize");

const User = {
    id: {
        type: DataTypes.INTEGER,
        autoIncrement: true,
        primaryKey: true,
    },
    nickname: {
        type: DataTypes.STRING,
        allowNull: true,
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
    model: null,
    initialize(sequelize) {
        this.model = sequelize.define("User", User);
        return this.model;
    },

    createUser(user) {
        return this.model.create(user);
    },

    findUserByEmail(email) {
        return this.model.findOne({
            where: {
                email: email,
            },
        });
    },

    findUserByID(id) { 
        return this.model.findOne({
            where: {
                id: id,
            },
        });
    },
};