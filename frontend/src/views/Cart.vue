<template>
    <h1 class='is-size-2 has-text-primary has-text-weight-medium is-family-sans-serif'> HERE IS YOUR CART WITH
        SUBTOTAL
        ₹{{ billingPrice }}</h1>
    <div class="columns is-multiline">
        <section v-for="item in items" :key="item.product.id" class="column is-3 section is-small">
            <div class="box">
                <figure class="image mb-4">
                    <img :src="item.product.get_thumbnail" alt="Oops">
                    <h6 class="is-size-5 has-text-weight-bold">{{ item.product.name }}</h6>
                    <div class="field has-addons mt-6">
                        <div class="control">
                            <a class="button is-dark has-background-success	" @click="modifyCartItem(item)">Update
                                Cart</a>
                        </div>
                        <div class="control">
                            <input type="number" class="input" min="1" v-model="item.quantity">
                        </div>
                    </div>
                    <p class="is-size-5 has-text-grey"> subtotal ₹{{ item.product.price * item.quantity }}</p>
                    <div class="wrapper">
                        <router-link v-bind:to="item.product.get_absolute_url"
                            class="button is-dark has-background-info mt-4 center">View
                            details
                        </router-link>
                        <div class="control">
                            <a class="button is-dark has-background-danger" @click="removeCartItem(item)">Remove from
                                Cart</a>
                        </div>
                    </div>
                </figure>
            </div>
        </section>
    </div>
</template>

<script>
import axios from 'axios';
import { toast } from 'bulma-toast';
export default {
    name: 'Cart',
    data() {
        return {
            cart: [],
            items: [],
        }
    },
    mounted() {
        this.cart = this.$store.state.cart
    },
    methods: {
        modifyCartItem(item) {
            this.$store.commit('modifyCartItem', item);

            toast({
                message: 'cart updated',
                type: 'is-success',
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: 'bottom-right',
            });
        },
        removeCartItem(item) {
            this.$store.commit('removeCartItem', item);

            toast({
                message: 'Item Removed',
                type: 'is-danger',
                dismissible: true,
                pauseOnHover: true,
                duration: 2000,
                position: 'bottom-right',
            });
        },
    },
    computed: {
        billingPrice() {
            this.items = this.cart.items;
            let total = 0;
            for (let j in this.cart.items) {
                total += (this.cart.items[j].quantity) * (this.cart.items[j].product.price);
            }
            return total;
        },
    },
}

</script>


