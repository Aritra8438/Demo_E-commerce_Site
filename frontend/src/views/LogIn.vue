<template>
    <div class="page-log-in">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Log In</h1>

                <form @submit.prevent="submitForm">

                    <div class="field">
                        <label>Email Address</label>
                        <div class="control">
                            <input type="email" class="input" v-model="emailId">
                        </div>
                    </div>

                    <div class="field">
                        <label>Username</label>
                        <label class="has-text-danger">*</label>
                        <div class="control">
                            <input type="text" class="input" v-model="username" required>
                        </div>
                    </div>

                    <div class="field">
                        <label>Password</label>
                        <label class="has-text-danger">*</label>
                        <div class="control">
                            <input type="password" class="input" v-model="password" required>
                        </div>
                    </div>

                    <article class="has-text-danger">* fields are mandatory</article>

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>


                    <div class="field has-text-centered">
                        <div class="control">
                            <button class="button is-light is-success">Log In</button>
                        </div>
                    </div>

                    <hr>
                    No Account? <router-link to="/signup">click here</router-link> to sign up!

                </form>
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios';
import { toast } from 'bulma-toast';
export default {
    name: "LogIn",
    data() {
        return {
            username: "",
            password: "",
            emailId: "",
            errors: [],
        }
    },
    methods: {
        async submitForm() {
            axios.defaults.headers.common["Authorization"] = ""
            localStorage.removeItem("token")
            const formData = {
                username: this.username,
                password: this.password
            }
            await axios
                .post("/api/v1/token/login/", formData)
                .then(response => {
                    const token = response.data.auth_token
                    this.$store.commit('setToken', token)
                    toast({
                        message: 'You are now logged in',
                        type: 'is-success',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 3000,
                        position: 'bottom-right',
                    });
                    axios.defaults.headers.common["Authorization"] = "Token " + token
                    localStorage.setItem("token", token)
                    const toPath = this.$route.query.to || '/'
                    this.$router.push(toPath)
                })
                .catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            for (let i = 0; i < error.response.data[property].length; i++) {
                                this.errors.push(`${property}: ${error.response.data[property][i]}`)
                            }
                        }
                    } else {
                        this.errors.push('Something went wrong. Please try again')

                        console.log(JSON.stringify(error))
                    }
                    toast({
                        message: 'Credentials mismatch. Try Again',
                        type: 'is-danger',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 3000,
                        position: 'bottom-right',
                    });
                })
        }
    },
}
</script>