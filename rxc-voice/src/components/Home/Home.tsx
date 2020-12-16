import React, { useEffect } from "react";
// import { Link } from "react-router-dom";
import Header from "../Header";
import logo from '../../assets/logo.svg';
import { BgColor } from "../../models/BgColor";

import "./Home.scss";

function Home(props: any) {

  useEffect(() => {
    props.changeColor(BgColor.Yellow);

   // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="home">
    </div>
  );
}

export default Home;