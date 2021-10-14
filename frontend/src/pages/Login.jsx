import React, { useState, useEffect } from 'react';
import { Redirect } from "react-router-dom";
import {
  AmplifyAuthenticator,
  AmplifySignIn,
  AmplifySignUp,
} from '@aws-amplify/ui-react';
import {
  AuthState,
  onAuthUIStateChange
} from '@aws-amplify/ui-components';

const LogIn = () => {
  const [authState, setAuthState] = useState();
  const [user, setUser] = useState();

  useEffect(() => {
    return onAuthUIStateChange((nextAuthState, authData) => {
      setAuthState(nextAuthState);
      setUser(authData);
    });
  }, []);

  return authState === AuthState.SignedIn && user ? (
    // maybe here push to a "sucessfully logged in, welcome UserName" page?
    <Redirect to="/" />
  ) : (
    <>
      <AmplifyAuthenticator usernameAlias='email'>
        <AmplifySignUp
          slot='sign-up'
          usernameAlias='email'
          formFields={[{ type: 'email' }, { type: 'password' }]}
        />
        <AmplifySignIn slot='sign-in' usernameAlias='email' />
      </AmplifyAuthenticator>
    </>
  );
};

export default LogIn;
