<template>
  <div class="row justify-content-center py-4">
    <app-connection-graph :activeUsersList="usersArray" :activeUsersLink="userLinks" ref="graphPointer"/>
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
          @sendUsersList="saveUsersList"
      />
    </div>
  </div>
</template>

<script>
import AppUsersList from "@/components/AppUsersList";
import AppChat from "@/components/AppChat";
import AppConnectionGraph from "./AppConnectionGraph";

export default {
  components: {
    AppConnectionGraph,
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
      messages: [],
      usersArray: [],
      userLinks: [],
    }
  },
  methods: {
    openChat(user) {
      this.chatOnline = true;
      this.messageTo = user;
      this.socket.emit('open_chat_session', {source: this.username, target: user});
    },
    newMessage(message) {
      this.messages.push(message);
    },
    saveUsersList(list) {
      this.usersArray.length = 0
      list.forEach((user) => {
        this.usersArray.push({id: user});
      });
      this.requestGraph();
    },
    requestGraph() {
      this.$refs.graphPointer.createGraph();
    }
  },
  created() {
    this.socket.on('receiveMessage', (data) => {
      this.newMessage(data.message);
      this.openChat(data.messageFrom);
    })
    this.socket.on('updateChatSessions', (data) => {
      let active_sessions = data.data
      active_sessions.forEach((session) => {
        let session_nodes = session.split(':')
        this.userLinks.push({source: session_nodes[0], target: session_nodes[1]})
      })
      this.requestGraph();
    })
  }
}
</script>

<style scoped>

</style>