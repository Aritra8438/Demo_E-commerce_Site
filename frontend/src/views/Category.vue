<template>
    <div class="page-category">
        <div class="columns is-multiline">
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
    name: 'category',
    data() {
        return {
            products: [],
            url: "/api/v1/products/",
        }
    },
    mounted() {
        this.getProducts()
    },
    watch: {
        $route(to, from) {
            console.log(to)
            if (to.name === 'Category') {
                this.getProducts()
            }
        }
    },
    methods: {
        async getProducts() {
            this.$store.commit('setIsLoading', true)
            const category_slug = this.$route.params.category_slug;
            const specific = this.url + category_slug;
            await axios
                .get(specific)
                .then(response => {
                    //console.log(response.data)
                    this.products = response.data;
                })
                .catch(error => {
                    console.log(error)
                })
            this.$store.commit('setIsLoading', false)

        }
    }
}
</script>