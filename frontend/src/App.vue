<template>
  <div id="wrapper" :style="myStyle">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>Bookish</strong></router-link>

        <a class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbar-menu"
          @click="showMobileMenu = !showMobileMenu">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div class="navbar-menu" id="navbar-menu" v-bind:class="{ 'is-active': showMobileMenu }">
        <div class="navbar-start">
          <div class="navbar-item">
            <form method="get" action="/search">
              <div class="field has-addons">
                <div class="dropdown">
                  <input type="text" class="dropdown-input" placeholder="What are you looking for?" name="query"
                    v-model="search" @input="getSearch()" autocomplete="off">
                  <div class="dropdown-content" v-show="dropdown">
                    <div class="dropdown-item" v-for="(obj, index) in querySet" :key="index"
                      @mousedown="selectOption(obj)">
                      {{ obj }}
                    </div>
                  </div>
                </div>
                <div class="control">
                  <button class="button is-success test" @click="goToProduct">
                    <span class="icon">
                      <i class="fas fa-search"></i>
                    </span>
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>

        <div class="navbar-end">
          <router-link to="/romance" class="navbar-item">Romance</router-link>
          <router-link to="/thriller" class="navbar-item">Thriller</router-link>

          <div class="navbar-item">
            <div class="buttons">
              <template v-if="$store.state.isAuthenticated">
                <router-link to="/" class="button is-light is-info">My account</router-link>
                <router-link to="/" class="button is-light is-danger" @click="logOut">Log Out</router-link>
              </template>

              <template v-else>
                <router-link to="/signup" class="button is-light is-success">Sign Up</router-link>
                <router-link to="/login" class="button is-light is-danger">Log in</router-link>
              </template>


              <router-link to="/cart" class="button is-success">
                <span class="icon"><i class="fas fa-shopping-cart"></i></span>
                <span>Cart ({{ cartTotalLength }})</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <div class="is-loading-bar has-text-centered" v-bind:class="{ 'is-loading': $store.state.isLoading }">
      <div class="lds-dual-ring"></div>
    </div>

    <section class="section">
      <router-view />
    </section>

    <footer class="footer" :style="myStyle">
      <p class="has-text-centered">Copyright (c) 2021</p>
    </footer>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      myStyle: {
        backgroundColor: "#e8e0d5"
      },
      showMobileMenu: false,
      search: "",
      querySet: [],
      dropdown: false,
      url: "/api/v1/auto?query=",
      cart: {
        items: [],
      }
    }
  },
  beforeCreate() {
    this.$store.commit('initializeStore')
    const token = this.$store.state.token
    if (token) {
      axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
      axios.defaults.headers.common['Authorization'] = ""
    }
  },
  mounted() {
    this.cart = this.$store.state.cart
  },
  updated() {
  },
  methods: {
    getSearch() {
      this.dropdown = false
      this.checkEmptySearch();
      if (this.search === '') {
        return;
      }
      else {
        this.getJson();
        this.getElastic();
      }
    },
    getElastic() {
      this.checkEmptySearch();
      axios
        .get("/api/v1/search/" + this.search + "/")
        .then(response => {
          for (let i = 0; i < response.data.length; i++) {
            this.querySet.push(response.data[i].name)
          }
          this.querySet = this.removeDuplicates(this.querySet)
          if (this.querySet.length === 0) this.dropdown = false;
          else this.dropdown = true;
        })
        .catch(error => {
          console.log(error)
        })
    },
    getJson() {
      this.checkEmptySearch();
      this.querySet = [];
      axios
        .get(this.url + this.search)
        .then(response => {
          for (let i = 0; i < response.data.length; i++) {
            this.querySet.push(response.data[i])
          }
          this.querySet = this.removeDuplicates(this.querySet)
        })
        .catch(error => {
          console.log(error)
        })
    },
    removeDuplicates(arr) {
      return [...new Set(arr)];
    },
    toggleDropdown() {
      this.dropdown = !this.dropdown
    },
    checkEmptySearch() {
      if (this.search == "") {
        this.dropdown = false;
      }
    },
    selectOption(string) {
      this.search = string;
      this.dropdown = false;
    },
    goToProduct() {
      console.log(this.search)
    },
    logOut() {
      this.$store.commit('removeToken')
    }
  },
  computed: {
    cartTotalLength() {
      let totalLength = 0;
      for (let i = 0; i < this.cart.items.length; i++) {
        totalLength += this.cart.items[i].quantity;
      }
      return totalLength;
    }
  }
}
</script>

<style lang="scss">
@import '../node_modules/bulma';

.lds-dual-ring {
  display: inline-block;
  width: 80px;
  height: 80px;
}

.lds-dual-ring:after {
  content: " ";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid #ccc;
  border-color: #ccc transparent #ccc transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}

@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.is-loading-bar {
  height: 0;
  overflow: hidden;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;

  &.is-loading {
    height: 80px;
  }
}
</style>
<style lang="scss" scoped>
.test {
  height: 30px;
  width: 30px;
}

.dropdown {
  position: relative;
  display: block;
  margin: auto;

  .dropdown-input {
    background: #fff;
    cursor: pointer;
    border: 1px solid #e7ecf5;
    border-radius: 3px;
    color: #333;
    display: block;
    font-size: .8em;
    padding: 6px;
    min-width: 250px;
    max-width: 250px;

    &:hover {
      background: #f8f8fa;
    }
  }

  .dropdown-content {
    position: absolute;
    background-color: #fff;
    min-width: 248px;
    max-width: 248px;
    max-height: 248px;
    border: 1px solid #e7ecf5;
    box-shadow: 0px -8px 34px 0px rgba(0, 0, 0, 0.05);
    overflow: auto;
    z-index: 1;

    .dropdown-item {
      color: black;
      font-size: .7em;
      line-height: 1em;
      padding: 8px;
      text-decoration: none;
      display: block;
      cursor: pointer;

      &:hover {
        background-color: #e7ecf5;
      }
    }
  }

  .dropdown:hover .dropdowncontent {
    display: block;
  }
}
</style>