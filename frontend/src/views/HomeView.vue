<template>
  <div class="home">
    <section class="hero is-small has-background-link mb-6">
      <div class="hero-body has-text-centered">
        <p class="title mb-6 has-text-white">
          Welcome to Bookish
        </p>
        <p class="subtitle has-text-white">
          A demo E-commerce website for shopping books
        </p>
      </div>
    </section>

    <div class="columns is-multiline">
      <div class="column is-12">
        <h2 class="is-size-2 has-text-centered">Latest products</h2>
      </div>
    </div>

    <div class="columns is-multiline">
      <section v-for="product in latestProducts" :key="product.id" class="column is-3 section is-small">
        <div class="box">
          <figure class="image mb-4">
            <img :src="product.get_thumbnail" alt="Oops">
            <h6 class="is-size-5 has-text-weight-bold">{{ product.name }}</h6>
            <p class="is-size-5 has-text-grey">₹{{ product.price }}</p>
            <router-link v-bind:to="product.get_absolute_url"
              class="button is-dark mt-4 center is-link has-text-centered">View details
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
  name: 'HomeView',
  data() {
    return {
      latestProducts: [],
    }
  },
  components: {
  },
  mounted() {
    this.getLatestProducts()
  },
  methods: {
    async getLatestProducts() {
      this.$store.commit('setIsLoading', true)
      await axios
        .get("/api/v1/latest-products/")
        .then(response => {
          this.latestProducts = response.data
        })
        .catch(error => {
          console.log(error)
        })
      this.$store.commit('setIsLoading', false)
    }
  }
}
</script>

<style scoped>
.image {
  margin-top: -1.25rem;
  margin-left: -1.25rem;
  margin-right: -1.25rem;
}

.center {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 50%;
}
</style>
