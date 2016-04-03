import Actions from "./actions";


const HEARTBEAT_INTERVAL = 1000;

export default class {

  constructor(path, handler) {
    this.raw = new WebSocket("wss://" + window.location.hostname + "/ws" + path);
    this.raw.onmessage = this._wrap_json_handler(handler);
    this.raw.onopen = () => {
      setInterval(
        () => this.heartbeat({"random":"shit"}),
        HEARTBEAT_INTERVAL);

      // for testing:
      this.subscribe({channel_id: "0000"});
      setInterval(
        () => this.publish({channel_id: "0000", body: "poop"}),
        5000);
    };
  }

  _wrap_json_handler(handler_func) {
    return (raw) =>
      handler_func(JSON.parse(raw.data))
  }

  send_message(action, content) {
    let msg = JSON.stringify({
      action,
      content
    });
    this.raw.send(msg);
  }

  heartbeat(content) {
    this.send_message(Actions.HEARTBEAT, content);
  }

  subscribe(content) {
    this.send_message(Actions.SUBSCRIBE, content);
  }

  publish(content) {
    this.send_message(Actions.MESSAGE, content);
  }

}
