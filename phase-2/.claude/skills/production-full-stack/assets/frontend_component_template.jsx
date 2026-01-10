// components/UserProfile/UserProfile.jsx
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { getUserProfile } from '../../services/userService';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorBoundary from '../common/ErrorBoundary';
import './UserProfile.css';

const UserProfile = ({ userId, showEdit = false }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        setLoading(true);
        setError(null);
        const userData = await getUserProfile(userId);
        setUser(userData);
      } catch (err) {
        setError(err.message || 'Failed to load user profile');
        console.error('Error fetching user profile:', err);
      } finally {
        setLoading(false);
      }
    };

    if (userId) {
      fetchUserProfile();
    }
  }, [userId]);

  const handleUpdateProfile = async (updatedData) => {
    try {
      setLoading(true);
      const updatedUser = await updateUserProfile(userId, updatedData);
      setUser(updatedUser);
    } catch (err) {
      setError(err.message || 'Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="error-message">Error: {error}</div>;
  if (!user) return <div className="no-user">User not found</div>;

  return (
    <ErrorBoundary>
      <div className="user-profile">
        <div className="user-avatar">
          <img
            src={user.avatar || '/default-avatar.png'}
            alt={`${user.firstName} ${user.lastName}`}
            className="avatar-image"
          />
        </div>

        <div className="user-info">
          <h2 className="user-name">
            {user.firstName} {user.lastName}
          </h2>

          <div className="user-details">
            <p className="user-email">
              <strong>Email:</strong> {user.email}
            </p>

            <p className="user-role">
              <strong>Role:</strong> {user.role}
            </p>

            <p className="user-joined">
              <strong>Member since:</strong> {new Date(user.createdAt).toLocaleDateString()}
            </p>
          </div>

          {user.profile && (
            <div className="user-bio">
              <h3>About</h3>
              <p>{user.profile.bio}</p>
            </div>
          )}
        </div>

        {showEdit && (
          <div className="user-actions">
            <button
              className="edit-button"
              onClick={() => handleEditProfile(user)}
            >
              Edit Profile
            </button>
          </div>
        )}
      </div>
    </ErrorBoundary>
  );
};

UserProfile.propTypes = {
  userId: PropTypes.string.isRequired,
  showEdit: PropTypes.bool
};

export default UserProfile;