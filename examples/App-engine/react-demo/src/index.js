import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

function _defineProperty(obj, key, value) {if (key in obj) {Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true });} else {obj[key] = value;}return obj;}

class NavBar extends React.Component {constructor(...args) {super(...args);_defineProperty(this, "state",
    {
      content: [
      { id: 1, description: '<ul><li>We can help you build your website.</li><li>Have good connections with your clients.</li><li>Build a strong customers data base.</li></ul>' },
      { id: 2, description: "<iframe src='https://sadasystems.looker.com/embed/public/8RK9QQF9HjfrfbS3zQHzsMs6R7PzC9Ns?type=table' width='600' height='338' frameborder='0'></iframe>" },
      { id: 3, description: "<iframe src='https://sadasystems.looker.com/embed/public/8RK9QQF9HjfrfbS3zQHzsMs6R7PzC9Ns' width='600' height='338' frameborder='0'></iframe>" },
      { id: 4, description: '<h1>About is here</h1>' }],

      listItems: [
      { id: 1, name: 'Home', active: false },
      { id: 2, name: 'table', active: false },
      { id: 3, name: 'visual', active: false },
      { id: 4, name: 'About Us', active: false }],

      body: null });_defineProperty(this, "showContentHandler",






    id => {
      const body = { ...this.state.body };
      this.state.content.map(item => {
        if (item.id == id) {
          this.setState({ body: item.description });
        }
      });

      const listItems = [...this.state.listItems];
      for (let item of listItems) {
        item.active = false;
      }

      const listIndex = this.state.listItems.findIndex(item => {
        return item.id === id;
      });
      const listItem = {
        ...this.state.listItems[listIndex] };

      listItem.active = true;
      listItems[listIndex] = listItem;
      this.setState({ listItems: listItems });
    });_defineProperty(this, "showSideDrawer",

    elename => {
      let element = document.getElementById(elename);
      element.className === 'NavList' ? element.className += ' responsive' : element.className = 'NavList';
    });}componentDidMount() {this.showContentHandler(1);}

  render() {
    return /*#__PURE__*/(
      React.createElement("div", null, /*#__PURE__*/
      React.createElement("div", { className: "NavList", id: "NavBar" },
      this.state.listItems.map(item => {
        return /*#__PURE__*/(
          React.createElement("a", { onClick: () => this.showContentHandler(item.id), key: item.id, href: "#", className: item.active ? 'active' : '' }, item.name));
      }), /*#__PURE__*/
      React.createElement("a", { className: "icon", onClick: () => this.showSideDrawer("NavBar"), href: "#" }, /*#__PURE__*/React.createElement("i", { className: "fa fa-bars" }))), /*#__PURE__*/

      React.createElement("div", { className: "contentDivClass", dangerouslySetInnerHTML: { __html: this.state.body } })));



  }}



class App extends React.Component {
  render() {
    return /*#__PURE__*/(
      React.createElement("div", null, /*#__PURE__*/
      React.createElement(NavBar, null)));


  }}


ReactDOM.render( /*#__PURE__*/React.createElement(App, null), document.getElementById('root'));