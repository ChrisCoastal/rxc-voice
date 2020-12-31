import React, { useEffect, useState } from "react";
import { BgColor } from "../../models/BgColor";
import { WebService } from "../../services";
// import logo from '../../assets/logo.svg';

import "./Login.scss";

function Login(props: any) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  useEffect(() => {
    props.changeColor(BgColor.White);

   // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const login = () => {
    if (email && password) {
      WebService.loginUser({
        username: email,
        password: password,
      }).subscribe(async (data) => {
        if (data.ok) {
          const user = await data.json();
          sessionStorage.setItem("user", JSON.stringify(user));
          props.setUser(() => user);
          console.log(user);
        } else {
          if (data.status === 400) {
            console.log("do function")
          }
          const error = await data.json();
          console.log(error);
        }
      });
    }
  };

  return (
    <div className="login">
      <label className="app-title">RxC Voice</label>
      <input
        type="text"
        placeholder="Email"
        className="login-input"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        className="login-input"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button
        type="button"
        className="login-button"
        onClick={() => login()}
        >
        sign in
      </button>
    </div>
  );
}

export default Login;
