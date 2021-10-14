import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from 'react-router-dom';
import { Auth } from '@aws-amplify/auth';
import Amplify from '@aws-amplify/core';
import Home from './pages/Home';
import Login from './pages/Login';


const awsconfig = {
  Auth: {        
    region: process.env.REACT_APP_COGNITO_REGION,
    userPoolId: process.env.REACT_APP_COGNITO_USERPOOL_ID,
    userPoolWebClientId: process.env.REACT_APP_COGNITO_APP_CLIENT_ID,
  }
}

Amplify.configure(awsconfig);

function App() {  
  return (
    <Router>
      <Switch>
        <Route exact path='/' component={Home} />
        <Route exact path='/login' component={Login} />
      </Switch>
    </Router>
  );
}

export default App;