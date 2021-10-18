<template>
  <div>
    <div class="text-center">
      <h3>Welcome to the chat, {{ username }}</h3>
      <p>Click on a name to start chatting</p>
    </div>
    <div class="ms-auto" style="width: 80%">
      <span>List of active users:</span>
      <ul>
        <li v-for="user in activeUsers" v-bind:key="user" @click="startChat(user)">{{ user }}</li>
      </ul>
      <button type="submit" @submit.prevent>GET USERS</button>
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
    }
  },
  data() {
    return {
      activeUsers: []
    }
  },
  methods: {
    startChat(user) {
      this.$emit('newChat', user);
    }
  },
  mounted() {
    this.socket.emit('get_users');
    this.socket.on('users', (data) => {
      this.activeUsers = data.data;
    });
  }
}
</script>

<style scoped>

</style>