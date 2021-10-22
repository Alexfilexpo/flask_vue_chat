<template>
  <div class="chat-view">
    <span>Users in this chat:</span>
    <ul class="connected-users">
      <li class="d-inline-flex">{{ username }}</li>
      <li class="d-inline-flex">{{ messageTo }}</li>
    </ul>
    <div class="chat-area border border-5" style="width: 350px;">
      <ul>
        <li v-for="message in messages" :key="message">{{ message }}</li>
      </ul>
    </div>
    <input type="text" v-model="messageInput" @keyup.enter="sendMessage" placeholder="Type your message here...">
    <button type="submit" @submit.prevent.stop @click="sendMessage">Send</button>
    <button>Leave chat</button>
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
      messageInput: null
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
    }
  }
}
</script>

<style scoped>

</style>