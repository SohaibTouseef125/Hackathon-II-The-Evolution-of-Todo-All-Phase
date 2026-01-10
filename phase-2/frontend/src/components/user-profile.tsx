'use client';

import { useState, useEffect } from 'react';

interface UserProfileProps {
  userId: string;
  userEmail: string;
  userName?: string;
}

export default function UserProfile({ userId, userEmail, userName }: UserProfileProps) {
  const [profile, setProfile] = useState({
    id: userId,
    email: userEmail,
    name: userName || 'User',
  });

  // In a real app, you would fetch user profile data from an API
  useEffect(() => {
    // This would be an API call to fetch user profile
    // const fetchProfile = async () => {
    //   const response = await fetch(`/api/users/${userId}`);
    //   if (response.ok) {
    //     const data = await response.json();
    //     setProfile(data);
    //   }
    // };
    // fetchProfile();
  }, [userId, userEmail, userName]);

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h2 className="text-xl font-bold text-gray-900 mb-4">User Profile</h2>
      <div className="space-y-2">
        <div>
          <label className="block text-sm font-medium text-gray-700">Name</label>
          <p className="mt-1 text-sm text-gray-900">{profile.name}</p>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Email</label>
          <p className="mt-1 text-sm text-gray-900">{profile.email}</p>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">User ID</label>
          <p className="mt-1 text-sm text-gray-900">{profile.id}</p>
        </div>
      </div>
    </div>
  );
}