import React, { useState } from 'react';
import { Redirect } from 'react-router-dom';
import axios from 'axios';
import { Auth } from '@aws-amplify/auth';
import { useUser } from '../helpers/Hooks'
import protectedRoute from '../helpers/ProtectedRoute';


const Home = () => {
  const [user, signUserOut] = useUser();
  const [result, setResult] = useState({})
  const [redirect, setRedirect] = useState(false)

  const signOut = () => {
    Auth.signOut();
    signUserOut()
    setRedirect(true)
  };

  const ping = () => {
    console.log(process.env.REACT_APP_API_SERVICE_URL)
      axios.get(`${process.env.REACT_APP_API_SERVICE_URL}/ping`).then(res => {
        console.log(res.data);
        setResult(res.data)
      }).catch(err => {
        console.log(err);
        setResult({"status":"error"})
      });
  }

  const pong = () => {
      axios.get(`${process.env.REACT_APP_API_SERVICE_URL}/pong`, {
        headers: {
          "Authorization": user.signInUserSession.idToken.jwtToken,
        },
      }).then(res => {
        console.log(res.data);
        setResult(res.data)
      }).catch(err => {
        console.log(err);
        setResult({"status":"error"})
      });
  }

  return redirect ? (
    <Redirect to="/login" />
  ) : (
    <section className="section">
      <div className="container">
        <h1 className="title">
          Hello World
        </h1>
        <p className="subtitle">
          Lorem ipsum dolor sit amet consectetur adipisicing elit.
        </p>
        <div className="buttons">
          <button className="button" onClick={ping}>Ping</button>
          <button className="button" onClick={pong}>Pong</button>
          <button className="button is-danger" onClick={signOut}>Sign out</button>
        </div>
        <pre>{JSON.stringify(result)}</pre>
      </div>
    </section>
  )
};

export default protectedRoute(Home);
