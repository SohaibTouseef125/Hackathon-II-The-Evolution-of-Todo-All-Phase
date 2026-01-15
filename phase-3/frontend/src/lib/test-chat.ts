import { chatApiClient } from '../lib/api';

// Simple test to verify the chat functionality
async function testNaturalLanguageProcessing() {
  try {
    // Get user ID from localStorage (assuming user is logged in)
    const userStr = localStorage.getItem('user');
    if (!userStr) {
      throw new Error('No user found in localStorage. Please log in first.');
    }

    const user = JSON.parse(userStr);
    console.log('Testing with user:', user.email);

    // Test creating a task through natural language
    console.log('Testing task creation...');
    const response = await chatApiClient.sendMessage(
      user.id,
      "Add a task to buy groceries"
    );

    console.log('Response:', response);
    console.log('Task created successfully!');

    // Test listing tasks
    console.log('\nTesting task listing...');
    const listResponse = await chatApiClient.sendMessage(
      user.id,
      "Show me my tasks"
    );

    console.log('List response:', listResponse);

  } catch (error) {
    console.error('Test failed:', error);
  }
}

// Run the test
testNaturalLanguageProcessing();