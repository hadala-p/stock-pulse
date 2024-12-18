const router = require("express").Router();
const PredictionController = require("../controllers/PredictionController");

router.get( "/my", PredictionController.getMyPredictions);
router.get( "/public", PredictionController.getPublicPredictions);
router.post( "/post", PredictionController.postPrediction);
router.post( "/postDaily", PredictionController.postDailyPrediction);
router.post( "/myDaily", PredictionController.getMyDailyPredictions);
module.exports = router;