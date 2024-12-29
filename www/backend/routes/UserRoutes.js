const router = require("express").Router();
const UserController = require("../controllers/UserController");

router.get("/", UserController.getAllUsers);
module.exports = router;