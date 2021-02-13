import React, { Component } from 'react';
//import logo from './logo.svg';
import './App.css';
import firebase, { auth, provider } from './firebase.js';

class App extends Component {
  constructor() {
    super();
    this.state = {
      currentItem: '',
      username: '',
      items: [],
      user: null 
    }
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this); 
    this.login = this.login.bind(this);
    this.logout = this.logout.bind(this); 
  }
  handleChange(e) {
    this.setState({
      [e.target.name]: e.target.value
    })
  }
  logout() {
    auth.signOut()
    .then(() => {
      this.setState({
        user: null
      });
    });
  }
  login() {
    auth.signInWithPopup(provider) 
      .then((result) => {
        const user = result.user;
        this.setState({
          user
        });
      });
  }
  handleSubmit(e) {
    e.preventDefault();
    const itemsRef = firebase.database().ref('items');
    const item = {
      title: this.state.currentItem,
      user: this.state.user.displayName || this.state.user.email
    }
    itemsRef.push(item);
    this.setState({
      currentItem: '',
      username: ''
    });
  }
  componentDidMount() {
    auth.onAuthStateChanged((user) => {
      if (user) {
        this.setState({ user });
      } 
    });
    const itemsRef = firebase.database().ref('items');
    itemsRef.on('value', (snapshot) => {
      let items = snapshot.val();
      let newState = [];
      for (let item in items) {
        newState.push({
          id: item,
          title: items[item].title,
          user: items[item].user
        });
      }
      this.setState({
        items: newState
      });
    });
  }
  removeItem(itemId) {
    const itemRef = firebase.database().ref(`/items/${itemId}`);
    itemRef.remove();
  }
  
  render() {
    return (
      <div className='app'>
      <header>
        <div className="wrapper">
          <h1>Fun Food Friends</h1>
          {this.state.user ?
            <button onClick={this.logout}>Logout</button>                
            :
            <button onClick={this.login}>Log In</button>              
          }
        </div>
      </header>
      {this.state.user ?
        <div>
          <div className='user-profile'>
            <img src={this.state.user.photoURL} />
          </div>
          <div className='container'>
            <section className='add-item'>
              <form onSubmit={this.handleSubmit}>
                <input type="text" name="username" placeholder="What's your name?" value={this.state.user.displayName || this.state.user.email} />
                <input type="text" name="currentItem" placeholder="What are you bringing?" onChange={this.handleChange} value={this.state.currentItem} />
                <button>Add Item</button>
              </form>
            </section>
            <section className='display-item'>
              <div className="wrapper">
                <ul>
                  {this.state.items.map((item) => {
                    return (
                      <li key={item.id}>
                        <h3>{item.title}</h3>
                        <p>brought by: {item.user}
                          {item.user === this.state.user.displayName || item.user === this.state.user.email ?
                            <button onClick={() => this.removeItem(item.id)}>Remove Item</button> : null}
                        </p>
                      </li>
                    )
                  })}
                </ul>
              </div>
            </section>
          </div>
        </div>
        :
        <div className='wrapper'>
          <p>You must be logged in to see the potluck list and submit to it.</p>
        </div>
      }
    </div>
    );    
       
  }
}
export default App;
