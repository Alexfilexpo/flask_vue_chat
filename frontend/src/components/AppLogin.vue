<template>
  <div class="register-form d-flex justify-content-center">
    <form @submit.prevent>
      <input v-model="username" type="text" id="username" placeholder="Type your nickname here...">
      <button @click="registerUser" type="submit" id="login-button">Register</button>
    </form>
  </div>
</template>

<script>

export default {
  name: "AppLogin",
  props: ['socket'],
  data() {
    return {
      username: '',
      isAuth: false
    }
  },
  methods: {
    registerUser() {
      this.isAuth = true
      this.socket.emit('authorize', this.username);
      this.socket.emit('get_open_sessions');
      this.$emit('register', this.username, this.isAuth);
    }
  }
}
</script>

<style scoped>
#username {
  border: 2px solid black;
  margin-right: 10px;
  padding-left: 10px;
}
#login-button {
  width: 100px;
  height: 30px;
  border: 2px solid black;
}
</style>