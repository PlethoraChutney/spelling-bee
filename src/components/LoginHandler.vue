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
    }
}
</script>

<template>
    <div v-if="!userLoggedIn">
        <p>{{loginMessage}}</p>

        <input
         type="checkbox"
         name="existing-user-check" 
         v-model="existingUser" 
         id="existing-user-check">

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
        <p>Welcome back</p>
    </div>
</template>

<style scoped>

</style>