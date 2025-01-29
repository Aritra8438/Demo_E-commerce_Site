<template>
    <div class="page-sign-up">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Sign up</h1>

                <form autocomplete="off" @submit.prevent="submitForm">
                    <div class="field">
                        <label>Username</label>
                        <div class="control">
                            <input type="text" class="input" autocomplete="new-password" v-model="username">
                        </div>
                    </div>

                    <div class="field">
                        <label>Email Address</label>
                        <div class="control">
                            <input type="email" class="input" autocomplete="new-password" v-model="emailId">
                        </div>
                    </div>

                    <div class="field">
                        <label>Password</label>
                        <div class="control">
                            <input type="password" class="input" autocomplete="new-password" v-model="password">
                        </div>
                    </div>

                    <div class="field">
                        <label>Repeat password</label>
                        <div class="control">
                            <input type="password" class="input" v-model="password2">
                        </div>
                    </div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>

                    <div class="field has-text-centered">
                        <div class="control">
                            <button class="button is-light is-danger">Sign up</button>
                        </div>
                    </div>

                    <hr>

                    Or <router-link to="/login">click here</router-link> to log in!
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { toast } from 'bulma-toast';
export default {
    name: 'SignUp',
    data() {
        return {
            emailId: "",
            username: "",
            password: "",
            password2: "",
            errors: [],
        }
    },
    methods: {
        submitForm() {
            this.errors = []
            if (this.username === '') {
                this.errors.push('The username can not be empty')
            }
            if (this.password !== this.password2) {
                this.errors.push('The passwords doesn\'t match')
            }
            if (this.errors.length === 0) {
                const user = {
                    "username": this.username,
                    "password": this.password,
                    "email": this.emailId,
                }
                axios
                    .post("api/v1/users/", user)
                    .then(response => {
                        toast({
                            message: 'Account created',
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 3000,
                            position: 'bottom-right',
                        });
                        this.$router.push('/login')
                    })
                    .catch(error => {
                        if (error.response) {
                            for (const property in error.response.data) {
                                for (let i = 0; i < error.response.data[property].length; i++) {
                                    this.errors.push(`${property}: ${error.response.data[property][i]}`)
                                }
                            }
                            console.log(error)
                            console.log(JSON.stringify(error.response.data))
                        } else if (error.message) {
                            this.errors.push('Something went wrong. Please try again')

                            console.log(JSON.stringify(error))
                        }
                    })
            }
        }
    },
}
</script>
