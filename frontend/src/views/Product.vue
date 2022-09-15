<template>
    <div class="page-product">
        <div class="columns is-multiline">
            <div class="column is-9">
                <figure class="image mb-6 center">
                    <img v-bind:src="product.get_image">
                </figure>

                <h1 class="title">{{ product.name }}</h1>

                <p>{{ product.description }}</p>
            </div>

            <div class="column is-3">
                <h2 class="subtitle">Information</h2>

                <p><strong>Price: </strong>₹{{ product.price }}</p>

                <div class="field has-addons mt-6">
                    <div class="control">
                        <input type="number" class="input" min="1" v-model="quantity">
                    </div>

                    <div class="control">
                        <a class="button is-dark" @click="addToCart">Add to cart</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { toast } from 'bulma-toast';

export default {
    name: 'Product',
    data() {
        return {
            product: {},
            quantity: 1,
            url: 'api/v1/products/'
        }

    },
    mounted() {
        this.getProduct();
    },
    methods: {
        async getProduct() {
            this.$store.commit('setIsLoading', true)
            const category_slug = this.$route.params.category_slug
            const product_slug = this.$route.params.product_slug
            const specific = this.url + category_slug + '/' + product_slug + '/'
            await axios
                .get(specific)
                .then(response => {
                    this.product = response.data
                })
                .catch(error => {
                    console.log(error)
                })
            this.$store.commit('setIsLoading', false)
        },
        addToCart() {
            const item = {
                product: this.product,
                quantity: this.quantity,
            }
            this.$store.commit('addToCart', item);

            toast({
                message: 'The product is added to the cart',
                type: 'is-success',
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: 'bottom-right',
            });
        },
    }
}
</script>

<style scoped>
.image {
    margin-top: -1.25rem;
    margin-left: -1.25rem;
    margin-right: -1.25rem;
    max-width: 200px;
}

.center {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 50%;
}
</style>


