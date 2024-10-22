module.exports = {
    check: (req, res, next) => {
        const authHeader = req.headers['authorization'];
        if (!authHeader) {
            return res.status(401).json({
                status: false,
                error: {
                    message: 'Auth headers not provided in the request.'
                }
            });
        }

        const {
            user: { userId },
        } = req;

        UserModel.findUser({ id: userId }).then((user) => {
            if (!user) {
              return res.status(403).json({
                status: false,
                error: "Invalid access token provided, please login again.",
              });
            }
            else {
                return res.status(201).json({
                    status: true,
                });
            }
        });
    }
};