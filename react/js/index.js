import React from 'react';
import ReactDOM from 'react-dom';

function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}

const element = <Welcome name="React" />;
ReactDOM.render(
  element,
  document.getElementById('container')
);
