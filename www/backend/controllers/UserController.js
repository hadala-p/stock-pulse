module.exports = {
    getAllUsers: (req, res) => {
        User.findAllUsers({})
            .then((users) => {
                return res.status(200).json({
                status: true,
                data: users,
                });
            })
            .catch((err) => {
                return res.status(500).json({
                status: false,
                error: err,
                });
            });
    }
};
