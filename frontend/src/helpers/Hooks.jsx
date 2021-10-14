import React, { useState, useEffect } from 'react';
import { Auth } from '@aws-amplify/auth';


export function useUser() {
  const [user, setUser] = useState(null);

  const checkAuthState = async () => {
    try {
      const current_user = await Auth.currentAuthenticatedUser();
      setUser(current_user);
    } catch (err) {
      setUser(null);
    }
  }

  useEffect(() => {
    checkAuthState();
  }, []);

  const signUserOut = () => {
    setUser(null);
  }

  return [user, signUserOut]
}