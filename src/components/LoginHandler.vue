<script>
export default {
    props: {
        'userLoggedIn': Boolean,
        'userId': String,
        'loginMessage': String
    },
    data() {
        return {
            'enteredUserId': '',
            'secretWord': '',
            'existingUser': false
        }
    },
    methods: {
        toggleExistingUser() {
            this.existingUser = !this.existingUser;
        }
    }
}
</script>

<template>
    <div v-if="!userLoggedIn">
        <p>{{loginMessage}}</p>

        <div class="button"
        @click="toggleExistingUser()"
        :class="{'has-account': existingUser}">
            I have an account
        </div>

        <input
         type="text" 
         v-model="enteredUserId" 
         name="user-id-input" 
         id="user-id-input">

        <input
         type="text" 
         v-model="secretWord" 
         name="secret-word-input" 
         id="secret-word-input" 
         v-if="existingUser">

        <div
         class="button" 
         @click="$emit('login', {
             'userId': enteredUserId,
             'secretWord': secretWord,
             'createNewUser': !existingUser})">
            Submit
        </div>
    </div>
    <div v-else>
        <p>Welcome back, {{this.userId}}</p>
    </div>
</template>

<style scoped>
div.has-account {
    background-color: #f7da21;
}
</style>