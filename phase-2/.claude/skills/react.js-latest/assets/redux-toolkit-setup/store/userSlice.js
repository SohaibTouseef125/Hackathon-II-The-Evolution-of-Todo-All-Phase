// User Slice
// store/userSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Async thunk for fetching user
export const fetchUserById = createAsyncThunk(
  'users/fetchById',
  async (userId, { rejectWithValue }) => {
    try {
      const response = await fetch(`/api/users/${userId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch user');
      }
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const userSlice = createSlice({
  name: 'user',
  initialState: {
    entities: [],
    loading: 'idle',
    error: null,
  },
  reducers: {
    addUser: (state, action) => {
      state.entities.push(action.payload);
    },
    updateUser: (state, action) => {
      const index = state.entities.findIndex(user => user.id === action.payload.id);
      if (index !== -1) {
        state.entities[index] = action.payload;
      }
    },
    removeUser: (state, action) => {
      state.entities = state.entities.filter(user => user.id !== action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchUserById.pending, (state) => {
        state.loading = 'pending';
      })
      .addCase(fetchUserById.fulfilled, (state, action) => {
        state.loading = 'idle';
        state.entities.push(action.payload);
      })
      .addCase(fetchUserById.rejected, (state, action) => {
        state.loading = 'idle';
        state.error = action.payload;
      });
  },
});

export const { addUser, updateUser, removeUser } = userSlice.actions;

export default userSlice.reducer;