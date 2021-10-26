<template>
  <div class="row justify-content-center py-4">
    <app-connection-graph
        :activeUsersList="usersArray"
        :activeUsersLink="userLinks"
        :messagePushed="messageSent"
        :username="username"
        :messageSent="messageSent"
        :messageFrom="messageFrom"
        ref="graphPointer"
    />
    <div class="users-view col-md-4">
      <app-chat
          v-if="chatOnline"
          :username="username"
          :messageTo="messageTo"
          :socket="socket"
          :messages="messages"
          @newMessage="newMessage"
          @leaveChat="leaveChat"
          ref="chatPointer"
      />
      <app-users-list
          v-else
          :username="username"
          :socket="socket"
          :messages="messages"
          @newChat="openChat"
          @sendUsersList="saveUsersList"
          ref="userListPointer"
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
  props: ['username', 'socket'],
  data() {
    return {
      chatOnline: false,
      messageTo: null,
      messages: [],
      usersArray: [],
      userLinks: [],
      messageSent: [],
      messageFrom: []
    }
  },
  methods: {
    openChat(user) {
      if (user == this.username) {
        alert('If you want to have chat with yourself - use mirror)')
      } else {
        this.chatOnline = true;
        this.messageTo = user;
        this.socket.emit('open_chat_session', {source: this.username, target: user});
      }
    },
    leaveChat(username, messageTo) {
      this.chatOnline = false;
      this.socket.emit('close_chat_session', {source: this.username, target: messageTo})
    },
    newMessage(message) {
      this.messages.push(message);
      this.messageSent.push(true);
      this.messageFrom.push(message.split(":")[0])
      if (this.chatOnline == false) {
        this.$refs.userListPointer.countMessages();
      } else {
        this.$refs.chatPointer.filterMessages()
      }
      this.resetGraph();
      setTimeout(() => {
        this.messageSent.length = 0
        this.messageFrom.length = 0
        this.resetGraph();
      }, 3000);
    },
    saveUsersList(list) {
      this.usersArray.length = 0
      list.forEach((user) => {
        this.usersArray.push({id: user});
      });
      this.resetGraph();
    },
    resetGraph() {
      this.$refs.graphPointer.createGraph();
    }
  },
  created() {
    this.socket.on('receiveMessage', (data) => {
      this.newMessage(data.message);
      this.messageFrom.push(data.messageFrom)
      this.resetGraph();
      setTimeout(() => {
        this.messageSent.length = 0
        this.messageFrom.length = 0
        this.resetGraph();
      }, 3000);
    })
    this.socket.on('updateChatSessions', (data) => {
      let active_sessions = data.data
      if (active_sessions.length > 0) {
        this.userLinks.length = 0
        active_sessions.forEach((session) => {
          let session_nodes = session.split(':')
          this.userLinks.push({source: session_nodes[0], target: session_nodes[1]})
        })
      } else {
        this.userLinks.length = 0
      }
      if (this.chatOnline == true) {
        this.$refs.chatPointer.filterMessages()
      }
      this.resetGraph();
    })
  }
}
</script>

<style scoped>

</style>