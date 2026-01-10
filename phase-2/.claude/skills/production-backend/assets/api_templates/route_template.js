// routes/users.js
const express = require('express');
const { body, param } = require('express-validator');
const auth = require('../middleware/auth');
const rateLimit = require('express-rate-limit');
const UsersController = require('../controllers/UsersController');

const router = express.Router();

// Rate limiting for authentication-related endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // Limit each IP to 5 requests per windowMs
  message: 'Too many authentication attempts, please try again later.'
});

// Validation rules
const validateUser = [
  body('email')
    .isEmail()
    .normalizeEmail()
    .withMessage('Must be a valid email'),
  body('password')
    .isLength({ min: 8 })
    .withMessage('Password must be at least 8 characters long')
    .matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/)
    .withMessage('Password must contain at least one uppercase, lowercase, and number'),
  body('firstName')
    .trim()
    .isLength({ min: 1, max: 50 })
    .withMessage('First name must be between 1 and 50 characters'),
  body('lastName')
    .trim()
    .isLength({ min: 1, max: 50 })
    .withMessage('Last name must be between 1 and 50 characters')
];

const validateUserId = [
  param('id')
    .isMongoId()
    .withMessage('Invalid user ID format')
];

// Routes
// GET /api/users - Get all users (admin only)
router.get('/', auth, (req, res) => {
  // Check if user is admin
  if (req.user.role !== 'admin') {
    return res.status(403).json({
      success: false,
      message: 'Access denied. Admin role required.'
    });
  }
  UsersController.getAll(req, res);
});

// GET /api/users/:id - Get user by ID
router.get('/:id', validateUserId, auth, UsersController.getById);

// POST /api/users - Create new user
router.post('/', validateUser, UsersController.create);

// PUT /api/users/:id - Update user
router.put('/:id', validateUserId, validateUser, auth, UsersController.update);

// DELETE /api/users/:id - Delete user
router.delete('/:id', validateUserId, auth, (req, res) => {
  // Check if user is admin or trying to delete themselves
  if (req.user.role !== 'admin' && req.user.id.toString() !== req.params.id) {
    return res.status(403).json({
      success: false,
      message: 'Access denied. Cannot delete other users.'
    });
  }
  UsersController.delete(req, res);
});

// GET /api/users/profile - Get current user profile
router.get('/profile', auth, (req, res) => {
  res.json({
    success: true,
    data: {
      id: req.user.id,
      email: req.user.email,
      firstName: req.user.firstName,
      lastName: req.user.lastName,
      role: req.user.role,
      createdAt: req.user.createdAt
    }
  });
});

// PUT /api/users/profile - Update current user profile
router.put('/profile', auth, [
  body('firstName')
    .optional()
    .trim()
    .isLength({ min: 1, max: 50 })
    .withMessage('First name must be between 1 and 50 characters'),
  body('lastName')
    .optional()
    .trim()
    .isLength({ min: 1, max: 50 })
    .withMessage('Last name must be between 1 and 50 characters'),
  body('email')
    .optional()
    .isEmail()
    .normalizeEmail()
    .withMessage('Must be a valid email')
], UsersController.update);

module.exports = router;