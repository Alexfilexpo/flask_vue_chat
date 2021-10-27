<template>
  <div class="row justify-content-center py-4">
    <app-connection-graph
        :activeUsersList="usersArray"
        :activeUsersLink="userLinks"
        :messagePushed="messageSent"
        :username="username"
        :messageSent="messageSent"
        :messageFrom="messageFrom"
        :messageTo="messageTo"
        ref="graphPointer"
    />
    <div class="users-view col-md-4">
      <app-chat
          v-if="chatOnline"
          :username="username"
          :chatWith="chatWith"
          :socket="socket"
          :messages="messages"
          @newMessage="newMessage"
          @leaveChat="leaveChat"
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
      chatWith: null,
      messages: {},
      usersArray: [],
      userLinks: [],
      messageSent: [],
      messageFrom: [],
      messageTo: []
    }
  },
  methods: {
    openChat(user) {
      if (user == this.username) {
        alert('If you want to have chat with yourself - use mirror)')
      } else {
        this.chatOnline = true;
        this.chatWith = user;
        this.socket.emit('open_chat_session', {source: this.username, target: user});
      }
    },
    leaveChat(username, messageTo) {
      this.chatOnline = false;
      this.socket.emit('close_chat_session', {source: this.username, target: messageTo})
    },
    newMessage(message_data) {
      this.messageSent.push(true);
      this.messageFrom.push(message_data.messageFrom)
      this.messageTo.push(message_data.messageTo)
      let messageGroup = ''
      if (message_data.messageFrom == this.username) {
        messageGroup = message_data.messageFrom+'-'+message_data.messageTo
      } else {
        messageGroup = message_data.messageTo+'-'+message_data.messageFrom
      }
      if (message_data.message != null) {
        if (messageGroup in this.messages) {
          this.messages[messageGroup].push(message_data.message)
        } else {
          this.messages[messageGroup] = []
          this.messages[messageGroup].push(message_data.message)
        }
        if (this.chatOnline == false) {
          this.$refs.userListPointer.countMessages();
        }
      }
      this.resetGraph();
      this.messageSent.length = 0
      this.messageFrom.length = 0
      this.messageTo.length = 0
      setTimeout(() => {
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
      this.newMessage(data);
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
      this.resetGraph();
    })
  }
}
</script>

<style scoped>

</style>