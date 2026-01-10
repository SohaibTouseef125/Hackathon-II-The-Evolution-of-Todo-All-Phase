// routes/users.js
const express = require('express');
const { body, param, query } = require('express-validator');
const { auth, authorize } = require('../middleware/auth');
const rateLimit = require('express-rate-limit');
const UserController = require('../controllers/UserController');

const router = express.Router();

// Rate limiting for user-related endpoints
const userLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again later.'
});

// Validation middleware
const validateUserId = [
  param('id').isMongoId().withMessage('Invalid user ID format')
];

const validateUserCreation = [
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

const validateUserUpdate = [
  body('email').optional().isEmail().normalizeEmail(),
  body('firstName').optional().trim().isLength({ min: 1, max: 50 }),
  body('lastName').optional().trim().isLength({ min: 1, max: 50 }),
  body('role').optional().isIn(['user', 'admin', 'moderator'])
];

// Routes
// GET /api/users - Get all users (admin only)
router.get('/', auth, authorize('admin'), userLimiter, UserController.getAll);

// GET /api/users/:id - Get user by ID (authenticated users)
router.get('/:id', validateUserId, auth, userLimiter, UserController.getById);

// POST /api/users - Create new user (public endpoint)
router.post('/', validateUserCreation, userLimiter, UserController.create);

// PUT /api/users/:id - Update user (authenticated users, admin can update any user)
router.put('/:id', validateUserId, validateUserUpdate, auth, userLimiter, UserController.update);

// DELETE /api/users/:id - Delete user (admin only)
router.delete('/:id', validateUserId, auth, authorize('admin'), userLimiter, UserController.delete);

// GET /api/users/profile - Get current user profile
router.get('/profile', auth, userLimiter, UserController.getProfile);

// PUT /api/users/profile - Update current user profile
router.put('/profile', auth, validateUserUpdate, userLimiter, UserController.updateProfile);

// GET /api/users/search - Search users (admin only)
router.get('/search', auth, authorize('admin'), [
  query('q').trim().escape().isLength({ min: 1 }).withMessage('Search query is required'),
  query('page').optional().isInt({ min: 1 }).withMessage('Page must be a positive integer'),
  query('limit').optional().isInt({ min: 1, max: 100 }).withMessage('Limit must be between 1 and 100')
], userLimiter, UserController.search);

module.exports = router;