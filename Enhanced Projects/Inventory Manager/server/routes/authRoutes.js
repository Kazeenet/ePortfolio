const express = require('express');
const router = express.Router();
const User = require('../models/User');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

// REGISTER
router.post('/register', async (req, res) => {
    try {
        const { username, password } = req.body;

        if (!username || !password)
            return res.status(400).json({ message: 'Missing fields' });

        // Check duplicate user
        const existing = await User.findOne({ username });
        if (existing)
            return res.status(400).json({ message: 'User already exists' });

        // Hash password
        const hashed = await bcrypt.hash(password, 10);

        // Save
        const newUser = new User({ username, password: hashed });
        await newUser.save();

        return res.json({ message: 'User registered successfully' });

    } catch (err) {
        console.error(err);
        return res.status(500).json({ message: 'Server error' });
    }
});

// LOGIN
router.post('/login', async (req, res) => {
    try {
        const { username, password } = req.body;

        const user = await User.findOne({ username });
        if (!user)
            return res.status(400).json({ message: 'Invalid username or password' });

        const valid = await bcrypt.compare(password, user.password);
        if (!valid)
            return res.status(400).json({ message: 'Invalid username or password' });

        // Create JWT
        const token = jwt.sign(
            { id: user._id },
            "MY_SUPER_SECRET_KEY",  // change later
            { expiresIn: "7d" }
        );

        return res.json({
            message: 'Login successful',
            token
        });

    } catch (err) {
        console.error(err);
        res.status(500).json({ message: 'Server error' });
    }
});

module.exports = router;
