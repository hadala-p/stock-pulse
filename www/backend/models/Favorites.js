const { DataTypes } = require("sequelize");

const Favorites = {
    id: {
        type: DataTypes.INTEGER,
        autoIncrement: true,
        primaryKey: true,
    },
    userId: {
        type: DataTypes.INTEGER,
        allowNull: false,
    },
    stockId: {
        type: DataTypes.INTEGER,
        allowNull: false,
    },
};

module.exports = {
    initialize(sequelize) {
        this.model = sequelize.define("Favorites", Favorites);
        return this.model;
    },

    addFavourite(favourite) {
        return this.model.create(favourite);
    },

    removeFavouriteById(id) {
        return this.model.destroy({
            where: {
                id: id,
            },
        });
    },

    removeFavouriteByUserAndStock(userId, stockId) {
        return this.model.destroy({
            where: {
                userId: userId,
                stockId: stockId,
            },
        });
    },

    findFavoritesByUser(userId) {
        return this.model.findAll({
            where: {
                userId: userId,
            },
        });
    },

    isFavourite(userId, stockId) {
        return this.model.findOne({
            where: {
                userId: userId,
                stockId: stockId,
            },
        });
    },
};
