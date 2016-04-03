import React from 'react';
import update from 'react-addons-update';

import Socket from './socket';
import Actions from './actions';


class InfoBox extends React.Component {
  render() {
    let rendered_channels_info = this.props.info.map((channel_info) => {
      return <div>{channel_info.channel_id + ": " + channel_info.members.join(", ")}</div>
    });
    return (
      <div>
        Channel Info:
        {rendered_channels_info}
      </div>
    )
  }
}


class Message extends React.Component {
  render() {
    return (
      <div>
        <div>{this.props.author + ' // ' + this.props.channel_id + ' // ' + this.props.id}</div>
        <div>{this.props.body}</div>
      </div>
    )
  }
}


class MessageList extends React.Component {
  render() {
    let rendered_messages = this.props.messages.map((msg) => {
      return <Message {...msg} key={msg.id} />
    })
    return (
      <div>
        {rendered_messages}
      </div>
    )
  }
}


class App extends React.Component {
  
  state = {
    socket_status: null,
    data: {
      info: [],
      messages: []
    }
  }

  constructor() {
    super();
    this.socket = new Socket("/main", ::this.handleMessage);
  }

  handleMessage(msg) {
    switch (msg.action) {
      case Actions.MESSAGE:
        this.setState((state) => update(state, {
          data: {
            messages: {
              $push: [msg.content]
            }
          }
        }));
        break;
      case Actions.HEARTBEAT:
        this.setState((state) => update(state, {
          data: {
            info: {
              $set: msg.content
            }
          }
        }));
        break;
      case Actions.ERROR:
        console.error("ERROR: " + msg.content);
        break;
      default:
        console.error("invalid message: ");
        console.error(msg);
    }
  }
  
  render() {
    return (
      <div>
        <InfoBox info={this.state.data.info} />
        <MessageList messages={this.state.data.messages} />
      </div>
    )
  }

}

React.render(<App/>, container);
