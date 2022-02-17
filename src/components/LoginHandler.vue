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
            'existingUser': false,
            'publicPath': process.env.BASE_URL
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
    <div class="message-container" v-if="!userLoggedIn">
        <img src="../assets/spelling-bee.svg" alt="">
        <p>{{loginMessage}}</p>

        <div class="button"
        @click="toggleExistingUser()"
        :class="{'has-account': existingUser}">
            I have an account
        </div>

        <div class="input-holder">
            <p>Username:</p>
            <input
             type="text"
             v-model="enteredUserId"
             name="user-id-input"
             id="user-id-input">
        </div>

        <div class="input-holder" v-if="existingUser">
            <p>Secret word:</p>
            <input
             type="text"
             v-model="secretWord"
             name="secret-word-input"
             id="secret-word-input"
             >
        </div>

        <div
         class="button" 
         @click="$emit('login', {
             'userId': enteredUserId,
             'secretWord': secretWord,
             'createNewUser': !existingUser})">
            Submit
        </div>
    </div>
    <div class="message-container" v-else>
        <img src="../assets/spelling-bee.svg" alt="">
        <p>Welcome back, {{this.userId}}</p>
    </div>
</template>

<style scoped>
img {
    width: 150px;
}

div.message-container {
    width: 300px;
}

div.has-account {
    background-color: #f7da21;
}

div.input-holder {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

div.input-holder > p {
    margin-right: 10px;
}

input {
    height: 1.5rem;
    box-sizing: border-box;
    border: 1px solid #e2e2e2;
}

input:focus {
    outline: none;
    border: 2px solid #f7da21;
}

p {
    white-space: pre-line;
}
</style>