const bcrypt = require('bcrypt');
const User = require("../models/User");

module.exports = {
    async getAllUsers(req, res) {
        try {
            const users = await User.model.findAll();
            res.json(users);
        } catch (error) {
            console.error(error);
            res.status(500).json({ error: "Internal Server Error" });
        }
    },

    async getCurrentUser(req, res) {
        try {
            const user = await User.findUserByID(req.user.id);
            if (!user) {
                return res.status(404).json({ error: "User not found" });
            }
            res.json({
                id: user.id,
                nickname: user.nickname,
                email: user.email,
            });
        } catch (error) {
            console.error(error);
            res.status(500).json({ error: "Internal Server Error" });
        }
    },

    async updateCurrentUser(req, res) {
        try {
            const user = await User.findUserByID(req.user.id);
            if (!user) {
                return res.status(404).json({ error: "User not found" });
            }

            const { email, password, currentPassword } = req.body;

            if (password) {
                if (!currentPassword) {
                    return res.status(400).json({ error: "Current password is required to change password." });
                }

                const isMatch = await bcrypt.compare(currentPassword, user.password);
                if (!isMatch) {
                    return res.status(401).json({ error: "Current password is incorrect." });
                }

                user.password = await bcrypt.hash(password, 10);
            }

            if (email) {
                user.email = email;
            }

            await user.save();

            res.json({
                id: user.id,
                nickname: user.nickname,
                email: user.email
            });
        } catch (error) {
            console.error(error);
            res.status(500).json({ error: "Internal Server Error" });
        }
    }

};
