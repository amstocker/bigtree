import React from 'react';

class MessageList extends React.Component {
  render() {
    return <h1>Hello World</h1>
  }
}

class App extends React.Component {
  constructor() {
    super();

    // init websocket
    this.ws = new WebSocket("wss://test.andrewstocker.net/ws/echo")
    this.ws.onopen = () => {
      this.ws.send("hello server")
    }
    this.ws.onmessage = this.handleMessage.bind(this)

    // init state
    this.state = {
      data: {
        messages: []
      }
    }
  }
  handleMessage(msg) {
    console.log(msg);
  }
  render() {
    return <MessageList messages={this.state.data.messages}/>
  }
}

React.render(<App/>, container);
