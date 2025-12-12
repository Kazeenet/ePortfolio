const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const itemRoutes = require('./routes/itemRoutes');
const authRoutes = require('./routes/authRoutes');

const app = express();
app.use(express.json());
app.use(cors());

// Connect to Mongo
mongoose.connect('mongodb://127.0.0.1:27017/inventoryApp')
    .then(() => console.log('MongoDB connected'))
    .catch(err => console.log(err));

// ROUTES
app.use('/api/items', itemRoutes);
app.use('/api/auth', authRoutes);

const PORT = 5000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
