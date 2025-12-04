const jwt = require('jsonwebtoken');
const SECRET = 'super-secret-key';

module.exports = function (req, res, next) {
    const authHeader = req.headers.authorization;

    if (!authHeader) {
        return res.status(401).json({ message: 'Missing Authorization header' });
    }

    const parts = authHeader.split(' ');
    if (parts.length !== 2 || parts[0] !== 'Bearer') {
        return res.status(401).json({ message: 'Malformed token' });
    }

    const token = parts[1];

    try {
        const decoded = jwt.verify(token, SECRET);
        req.user = decoded; // { userId: ... }
        next();
    } catch (err) {
        return res.status(403).json({ message: 'Invalid or expired token' });
    }
};
