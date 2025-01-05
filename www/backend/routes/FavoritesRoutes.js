const express = require('express');
const router = express.Router();
const FavoritesController = require('../controllers/FavoritesController');
const IsAuthenticatedMiddleware = require('../middleware/IsAuthenticatedMiddleware');


router.post('/', IsAuthenticatedMiddleware.check, FavoritesController.addFavourite);
router.delete('/:stockId', IsAuthenticatedMiddleware.check, FavoritesController.removeFavourite);
router.get('/', IsAuthenticatedMiddleware.check, FavoritesController.getFavorites);


module.exports = router;