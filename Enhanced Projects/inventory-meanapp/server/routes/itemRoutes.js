const express = require('express');
const router = express.Router();
const Item = require('../models/Item');

// CREATE item
router.post('/', async (req, res) => {
    try {
        const item = new Item({
            name: req.body.name,
            quantity: req.body.quantity,
            dateAdded: req.body.dateAdded || Date.now()
        });

        const savedItem = await item.save();
        res.json(savedItem);
    } catch (err) {
        res.status(400).json({ message: err.message });
    }
});

// GET all items
router.get('/', async (req, res) => {
    try {
        const items = await Item.find();
        res.json(items);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// UPDATE item
router.put('/:id', async (req, res) => {
    try {
        const updatedItem = await Item.findByIdAndUpdate(
            req.params.id,
            {
                name: req.body.name,
                quantity: req.body.quantity
            },
            { new: true }
        );

        res.json(updatedItem);
    } catch (err) {
        res.status(400).json({ message: err.message });
    }
});

// DELETE item
router.delete('/:id', async (req, res) => {
    try {
        await Item.findByIdAndDelete(req.params.id);
        res.json({ message: 'Item deleted' });
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

module.exports = router;
