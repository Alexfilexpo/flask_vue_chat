<template>
  <div class="chat-view">
    <div class="connected-users">
      <span class="d-inline-flex">Chat between {{ username }} and {{ chatWith }}:</span>
    </div>
    <div class="chat-area border border-5 border-dark mb-2">
      <div :class="message.includes(username)?'bg-primary float-start':'bg-secondary float-end'"
           class="chat-msg border border-1 rounded px-2 text-white p-2"
           v-for="message in this.messages[this.username+'-'+this.chatWith]"
           :key="message">{{ message }}</div>
    </div>
    <input type="text" id="chat-message" v-model="messageInput" @keyup.enter="sendMessage" placeholder="Type your message here...">
    <button type="submit" class="chat-button" @submit.prevent.stop @click="sendMessage">Send</button>
    <button type="submit" class="chat-button" @submit.prevent.stop @click="leaveChat">Leave chat</button>
  </div>
</template>

<script>
export default {
  name: "AppChat",
  props: ['socket', 'username', 'chatWith', 'messages'],
  data() {
    return {
      messageInput: null,
      messagesHistory: []
    }
  },
  methods: {
    sendMessage() {
      if (this.messageInput != null) {
        this.socket.emit('send_message', {
        'messageFrom': this.username,
        'messageTo': this.chatWith,
        'message': this.messageInput
        });
        this.$emit('newMessage', {
          'messageFrom': this.username,
          'messageTo': this.chatWith,
          'message': this.username + ':' + this.messageInput
        })
        this.messageInput = null
      }
    },
    leaveChat() {
      this.$emit('leaveChat', this.username, this.chatWith);
    }
  }
}
</script>

<style scoped>
.chat-area {
  width: 350px;
  height: 400px;
  overflow-y: auto;
}
.chat-msg {
  width: 200px;
  height: 50px;
}
#chat-message {
  border: 2px solid black;
}
.chat-button {
  border: 2px solid black;
  margin-left: 5px;
  padding: 0 5px;
}
</style>