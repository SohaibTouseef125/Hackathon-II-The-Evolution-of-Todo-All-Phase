// tests/unit/userService.test.js
const { MongoMemoryServer } = require('mongodb-memory-server');
const mongoose = require('mongoose');
const User = require('../../src/models/User');
const UserService = require('../../src/services/userService');

describe('UserService', () => {
  let mongoServer;
  let userId;

  beforeAll(async () => {
    // Setup in-memory MongoDB
    mongoServer = await MongoMemoryServer.create();
    await mongoose.connect(mongoServer.getUri());
  });

  afterAll(async () => {
    // Cleanup
    await mongoose.disconnect();
    await mongoServer.stop();
  });

  beforeEach(async () => {
    // Clear collections before each test
    await User.deleteMany({});

    // Create a test user
    const user = new User({
      email: 'test@example.com',
      password: 'Password123',
      firstName: 'John',
      lastName: 'Doe'
    });
    await user.save();
    userId = user._id;
  });

  afterEach(async () => {
    // Clean up after each test if needed
    jest.clearAllMocks();
  });

  describe('getUserById', () => {
    it('should return user by ID', async () => {
      const result = await UserService.getUserById(userId);

      expect(result).toBeDefined();
      expect(result.email).toBe('test@example.com');
      expect(result.firstName).toBe('John');
      expect(result.lastName).toBe('Doe');
      expect(result.password).toBeUndefined(); // Should be excluded
    });

    it('should return null for non-existent user', async () => {
      const result = await UserService.getUserById('507f1f77bcf86cd799439011');

      expect(result).toBeNull();
    });

    it('should throw error for invalid ID format', async () => {
      await expect(UserService.getUserById('invalid-id'))
        .rejects
        .toThrow('Invalid user ID format');
    });
  });

  describe('createUser', () => {
    it('should create a new user successfully', async () => {
      const userData = {
        email: 'newuser@example.com',
        password: 'NewPassword123',
        firstName: 'Jane',
        lastName: 'Doe'
      };

      const result = await UserService.createUser(userData);

      expect(result).toBeDefined();
      expect(result.email).toBe(userData.email);
      expect(result.firstName).toBe(userData.firstName);
      expect(result.lastName).toBe(userData.lastName);
      expect(result.password).toBeUndefined(); // Should be excluded
    });

    it('should throw error when email already exists', async () => {
      const userData = {
        email: 'test@example.com', // Already exists
        password: 'NewPassword123',
        firstName: 'Jane',
        lastName: 'Doe'
      };

      await expect(UserService.createUser(userData))
        .rejects
        .toThrow('User with this email already exists');
    });

    it('should throw error for invalid email format', async () => {
      const userData = {
        email: 'invalid-email',
        password: 'NewPassword123',
        firstName: 'Jane',
        lastName: 'Doe'
      };

      await expect(UserService.createUser(userData))
        .rejects
        .toThrow();
    });
  });

  describe('updateUser', () => {
    it('should update user successfully', async () => {
      const updateData = {
        firstName: 'Updated',
        lastName: 'Name'
      };

      const result = await UserService.updateUser(userId, updateData);

      expect(result).toBeDefined();
      expect(result.firstName).toBe('Updated');
      expect(result.lastName).toBe('Name');
    });

    it('should return null for non-existent user', async () => {
      const result = await UserService.updateUser('507f1f77bcf86cd799439011', { firstName: 'Updated' });

      expect(result).toBeNull();
    });
  });

  describe('deleteUser', () => {
    it('should delete user successfully', async () => {
      const result = await UserService.deleteUser(userId);

      expect(result).toBe(true);

      // Verify user is deleted
      const deletedUser = await User.findById(userId);
      expect(deletedUser).toBeNull();
    });

    it('should return false for non-existent user', async () => {
      const result = await UserService.deleteUser('507f1f77bcf86cd799439011');

      expect(result).toBe(false);
    });
  });

  describe('getUsers', () => {
    beforeEach(async () => {
      // Create additional users for pagination tests
      await User.create([
        {
          email: 'user2@example.com',
          password: 'Password123',
          firstName: 'User',
          lastName: 'Two'
        },
        {
          email: 'user3@example.com',
          password: 'Password123',
          firstName: 'User',
          lastName: 'Three'
        }
      ]);
    });

    it('should return paginated users', async () => {
      const result = await UserService.getUsers(1, 2);

      expect(result.users).toHaveLength(2);
      expect(result.pagination.total).toBe(3);
      expect(result.pagination.pages).toBe(2);
    });

    it('should return users with specific fields only', async () => {
      const result = await UserService.getUsers(1, 10);

      const user = result.users[0];
      expect(user).toHaveProperty('email');
      expect(user).toHaveProperty('firstName');
      expect(user).toHaveProperty('lastName');
      expect(user).not.toHaveProperty('password'); // Should be excluded
    });
  });

  describe('searchUsers', () => {
    beforeEach(async () => {
      // Create additional users for search tests
      await User.create([
        {
          email: 'john.doe@example.com',
          password: 'Password123',
          firstName: 'John',
          lastName: 'Doe'
        },
        {
          email: 'jane.smith@example.com',
          password: 'Password123',
          firstName: 'Jane',
          lastName: 'Smith'
        }
      ]);
    });

    it('should find users by first name', async () => {
      const result = await UserService.searchUsers('John');

      expect(result).toHaveLength(2); // Original John + John Doe
      expect(result).toEqual(
        expect.arrayContaining([
          expect.objectContaining({ firstName: 'John' })
        ])
      );
    });

    it('should return empty array for no matches', async () => {
      const result = await UserService.searchUsers('NonExistent');

      expect(result).toHaveLength(0);
    });
  });

  describe('user validation', () => {
    it('should validate strong password', async () => {
      const weakUserData = {
        email: 'weak@example.com',
        password: 'weak', // Too short and not strong
        firstName: 'Weak',
        lastName: 'Password'
      };

      await expect(UserService.createUser(weakUserData))
        .rejects
        .toThrow();
    });

    it('should validate email format', async () => {
      const invalidUserData = {
        email: 'invalid-email-format',
        password: 'ValidPassword123',
        firstName: 'Invalid',
        lastName: 'Email'
      };

      await expect(UserService.createUser(invalidUserData))
        .rejects
        .toThrow();
    });
  });
});

// Integration test example
describe('UserService Integration', () => {
  let mongoServer;

  beforeAll(async () => {
    mongoServer = await MongoMemoryServer.create();
    await mongoose.connect(mongoServer.getUri());
  });

  afterAll(async () => {
    await mongoose.disconnect();
    await mongoServer.stop();
  });

  beforeEach(async () => {
    await User.deleteMany({});
  });

  it('should create user and immediately retrieve it', async () => {
    const userData = {
      email: 'integration@example.com',
      password: 'Integration123',
      firstName: 'Integration',
      lastName: 'Test'
    };

    // Create user
    const createdUser = await UserService.createUser(userData);
    expect(createdUser).toBeDefined();
    expect(createdUser.email).toBe(userData.email);

    // Retrieve user
    const retrievedUser = await UserService.getUserById(createdUser._id);
    expect(retrievedUser).toBeDefined();
    expect(retrievedUser.email).toBe(userData.email);
    expect(retrievedUser.firstName).toBe(userData.firstName);
  });

  it('should update user and verify changes persist', async () => {
    const userData = {
      email: 'update@example.com',
      password: 'UpdatePassword123',
      firstName: 'Update',
      lastName: 'Original'
    };

    const user = await UserService.createUser(userData);
    expect(user.lastName).toBe('Original');

    const updatedUser = await UserService.updateUser(user._id, { lastName: 'Updated' });
    expect(updatedUser.lastName).toBe('Updated');

    // Verify the change persisted in the database
    const verifiedUser = await UserService.getUserById(user._id);
    expect(verifiedUser.lastName).toBe('Updated');
  });
});