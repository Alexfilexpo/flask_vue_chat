<template>
  <div class="register-form d-flex justify-content-center">
    <form @submit.prevent>
      <input v-model="username" type="text" id="username" placeholder="Type your nickname here...">
      <button @click="registerUser" type="submit">Register</button>
    </form>
<!--    remove after implementing example-->
    <example/>
<!--    remove after implementing example-->
  </div>
</template>

<script>
// remove after implementing example
import Example from "./Example";
// remove after implementing example

export default {
  name: "AppLogin",
  // remove after implementing example
  components: {Example},
  // remove after implementing example
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

</style>