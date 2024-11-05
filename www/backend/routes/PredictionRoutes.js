const router = require("express").Router();
const PredictionController = require("../controllers/PredictionController");

router.get( "/my", PredictionController.getMyPredictions);
router.get( "/public", PredictionController.getPublicPredictions);
router.post( "/post", PredictionController.postPrediction);
module.exports = router;