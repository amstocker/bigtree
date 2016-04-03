import React from 'react';
import update from 'react-addons-update';


class InfoBox extends React.Component {

  render() {
    let rendered_members = this.props.info.members.map((member) => {
      return <div>{member}</div>
    });
    return (
      <div>
        Members:
        {rendered_members}
      </div>
    );
  }

}


class Message extends React.Component {
  
  render() {
    return (
      <div>
        <div>{this.props.session_id + ' // ' + this.props.chan_id + ' // ' + this.props.id}</div>
        <div>{this.props.content.body}</div>
      </div>
    );
  }

}


class MessageList extends React.Component {
  
  render() {
    let rendered_messages = this.props.messages.map((msg) => {
      return <Message {...msg} key={msg.content.id} />
    });
    return (
      <div>
        {rendered_messages}
      </div>
    );
  }

}


class App extends React.Component {
  
  state = {
    socket_status: null,
    data: {
      info: {
        members: []
      },
      messages: []
    }
  }

  constructor() {
    super();

    // init websocket
    this.socket = new WebSocket("wss://test.andrewstocker.net/ws/main")
    this.socket.onopen = () => {
      this.socket.send('{"action":"subscribe", "chan_id":"0000"}');
      setInterval(
          () => this.socket.send('{"action":"message", "chan_id":"0000", "content": {"body":"poop"}}'),
          5000);
      setInterval(
          () => this.socket.send('{"action":"getinfo", "chan_id":"0000"}'),
          1000);
    }
    // fancy ES7 bind syntax...
    this.socket.onmessage = ::this.handleMessage
  }

  handleMessage(raw) {
    let msg = JSON.parse(raw.data);
    switch (msg.action) {
      case "message":
        console.log(msg);
        this.setState((state) => update(state, {
          data: {
            messages: {
              $push: [msg]
            }
          }
        }));
        break;
      case "getinfo":
        console.log(msg);
        this.setState((state) => update(state, {
          data: {
            info: {
              $set: msg.content
            }
          }
        }));
        break;
      default:
        console.error("invalid message: " + raw.data);
    }
  }
  
  render() {
    return (
      <div>
        <InfoBox info={this.state.data.info} />
        <MessageList messages={this.state.data.messages} />
      </div>
    );
  }

}

React.render(<App/>, container);
