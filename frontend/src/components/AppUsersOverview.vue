<template>
  <div class="row justify-content-center py-4">
    <div class="graph-view col-md-6">
      <img src="https://www.amcharts.com/wp-content/uploads/2013/12/demo_910_none-1.png" style="width: 100%">
    </div>
    <div class="users-view col-md-4">
      <app-chat
          v-if="chatOnline"
          :username="username"
          :messageTo="messageTo"
          :socket="socket"
          :messages="messages"
          @newMessage="newMessage"
      />
      <app-users-list
          v-else
          :username="username"
          :socket="socket"
          @newChat="openChat"
      />
    </div>
  </div>
</template>

<script>
import AppUsersList from "@/components/AppUsersList";
import AppChat from "@/components/AppChat";

export default {
  components: {
    AppUsersList,
    AppChat
  },
  name: "AppUsersOverview",
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
      chatOnline: false,
      messageTo: null,
      messages: []
    }
  },
  methods: {
    openChat(user) {
      this.chatOnline = true;
      this.messageTo = user;
    },
    newMessage(message) {
      this.messages.push(message);
    }
  },
  created() {
    this.socket.on('receiveMessage', (data) => {
      this.newMessage(data.message);
      this.openChat(data.messageFrom);
    })
  }
}
</script>

<style scoped>

</style>