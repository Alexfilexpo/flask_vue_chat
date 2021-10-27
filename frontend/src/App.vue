<template>
  <div class="container">
    <h1 class="text-center">FlaskVueChat</h1>
    <app-users-overview v-if="userAuthorized" :username="username" :socket="socket"/>
    <app-login v-else :socket="socket" @register="addUser"/>
  </div>
</template>

<script>
import AppLogin from "@/components/AppLogin";
import AppUsersOverview from "@/components/AppUsersOverview";
import io from 'socket.io-client'

export default {
  components: {
    AppLogin,
    AppUsersOverview,
  },
  name: "App",
  data() {
    return {
      username: '',
      userAuthorized: false,
      socket: null
    }
  },
  methods: {
    addUser(username, isAuth) {
      this.username = username
      this.userAuthorized = isAuth
    },
  },
  created() {
    this.socket = io('http://127.0.0.1:5000/private').connect()
  }
}
</script>

<style>
.container {
  padding: 25px 25px;
}
.text-center {
  cursor: default;
}
</style>