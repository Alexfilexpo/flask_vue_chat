<template>
  <div>
    <div class="text-center">
      <h3>Welcome to the chat, {{ username }}</h3>
      <p>Click on a name to start chatting</p>
    </div>
    <div class="ms-auto users-list">
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
  props: ['username', 'socket', 'messages'],
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
      for (const [sessionName, messagesList] of Object.entries(this.messages)) {
        let userWith = sessionName.split('-')[1]
        rawMessagesCounter[userWith] = messagesList.length
      }
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
.users-list {
  width: 80%;
}
</style>