<template>
  <div>
    <div class="text-center">
      <h3>Welcome to the chat, {{ username }}</h3>
      <p>Click on a name to start chatting</p>
    </div>
    <div class="ms-auto" style="width: 80%">
      <span>List of active users:</span>
      <ul>
        <li v-for="user in activeUsers" v-bind:key="user" @click="startChat(user)">{{ user }}
          <span v-if="user in messagesCounter"> [{{ messagesCounter[user] }} new messages]</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "AppUsersList",
  props: {
    username: {
      type: String,
      required: true
    },
    socket: {
      required: true
    },
    messages: {
      required: false
    }
  },
  data() {
    return {
      activeUsers: null,
      messagesCounter: {}
    }
  },
  methods: {
    startChat(user) {
      this.$emit('newChat', user);
    },
    countMessages() {
      let rawMessagesCounter = {}
      this.messages.forEach((message) => {
        let messageData = message.split(':')
        let messageFromName = messageData[0]
        if (messageFromName in rawMessagesCounter) {
          rawMessagesCounter[messageFromName] += 1
        } else {
          rawMessagesCounter[messageFromName] = 1
        }
      })
      this.messagesCounter = rawMessagesCounter
    }
  },
  mounted() {
    this.socket.emit('get_users');
    this.socket.on('users', (data) => {
      this.activeUsers = data.data;
      this.$emit('sendUsersList', this.activeUsers);
    });
  }
}
</script>

<style scoped>

</style>