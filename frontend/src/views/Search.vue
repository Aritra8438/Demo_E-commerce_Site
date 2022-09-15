<template>
    <div class="page-search">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Search</h1>

                <h2 class="is-size-5 has-text-grey">Search term: "{{ query }}"</h2>
            </div>
            <section v-for="product in products" :key="product.id" class="column is-3 section is-small">
                <div class="box">
                    <figure class="image mb-4">
                        <img :src="product.get_thumbnail" alt="Oops">
                        <h6 class="is-size-5 has-text-weight-bold">{{ product.name }}</h6>
                        <p class="is-size-5 has-text-grey">₹{{ product.price }}</p>
                        <router-link v-bind:to="product.get_absolute_url" class="button is-dark mt-4 center">View
                            details
                        </router-link>
                    </figure>
                </div>
            </section>

        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    export default {
        name: 'Search',
        data() {
            return {
                products: [],                                
                query: '',
                url: 'http://127.0.0.1:8000/api/v1/products/search/'
            }
        },
        mounted() {                        
            let post = window.location.search.substring(1)
            let params = new URLSearchParams(post)              
            if(params.get('query')){
                this.query = params.get('query')
                this.performSearch()
            }
        },
        methods: {         
            async performSearch(){
                this.$store.commit('setIsLoading', true)                
                await axios
                .post(this.url,{'query':this.query})                 
                .then(response=>{                    
                    console.log(response.data)
                    this.products = response.data
                })
                .catch(error=>{
                    console.log(error)
                })                
                this.$store.commit('setIsLoading', false)                
            }            
        }
    };
</script>