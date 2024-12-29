const router = require("express").Router();
const UserController = require("../controllers/UserController");
const IsAuthenticatedMiddleware = require('../middleware/IsAuthenticatedMiddleware');

router.get("/", UserController.getAllUsers);
router.get("/me", IsAuthenticatedMiddleware.check, UserController.getCurrentUser);
router.put("/me", IsAuthenticatedMiddleware.check, UserController.updateCurrentUser);

module.exports = router;