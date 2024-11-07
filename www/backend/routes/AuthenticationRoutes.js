const router = require("express").Router();
const AuthenticationController = require("../controllers/AuthenticationController");

router.post( "/signup", AuthenticationController.register);
router.post( "/login", AuthenticationController.login);
module.exports = router;