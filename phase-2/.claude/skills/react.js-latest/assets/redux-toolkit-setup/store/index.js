// Redux Store Setup
// store/index.js
import { configureStore } from '@reduxjs/toolkit';
import { userSlice } from './userSlice';
import { postsSlice } from './postsSlice';

export const store = configureStore({
  reducer: {
    user: userSlice.reducer,
    posts: postsSlice.reducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;