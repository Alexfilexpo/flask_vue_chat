<template>
  <div class="chat-view">
    <span>Users in this chat:</span>
    <ul class="connected-users">
      <li class="d-inline-flex">{{ username }}</li>
      <li class="d-inline-flex">{{ messageTo }}</li>
    </ul>
    <div class="chat-area border border-5" style="width: 350px;">
      <ul>
        <li v-for="message in messagesHistory" :key="message">{{ message }}</li>
      </ul>
    </div>
    <input type="text" v-model="messageInput" @keyup.enter="sendMessage" placeholder="Type your message here...">
    <button type="submit" @submit.prevent.stop @click="sendMessage">Send</button>
    <button type="submit" @submit.prevent.stop @click="leaveChat">Leave chat</button>
  </div>
</template>

<script>
export default {
  name: "AppChat",
  props: {
    socket: {
      required: true
    },
    username: {
      type: String
    },
    messageTo: {
      type: String
    },
    messages: {
      type: Array
    }
  },
  data() {
    return {
      messageInput: null,
      messagesHistory: []
    }
  },
  methods: {
    sendMessage() {
      this.socket.emit('send_message', {
        'messageFrom': this.username,
        'messageTo': this.messageTo,
        'message': this.messageInput
      });
      this.$emit('newMessage', this.username + ': ' + this.messageInput);
      this.messageInput = null
    },
    filterMessages() {
      this.messagesHistory.length = 0
      this.messages.forEach((message) => {
        let message_data = message.split(':')
        let message_name = message_data[0]
        if (message_name == this.messageTo || message_name == this.username) {
          this.messagesHistory.push(message);
        }
      })
    },
    leaveChat() {
      this.$emit('leaveChat', this.username, this.messageTo);
    }
  }
}
</script>

<style scoped>

</style>