import { createStore } from "vuex";

export default createStore({
  state: {
    cart: {
      items: [],
    },
    isAuthenticated: false,
    token: "",
    isLoading: false,
  },
  getters: {},
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem("cart")) {
        state.cart = JSON.parse(localStorage.getItem("cart"));
      } else {
        localStorage.setItem("cart", JSON.stringify(this.state.cart));
        state.cart = JSON.parse(localStorage.getItem("cart"));
      }

      if (localStorage.getItem("token")) {
        state.token = localStorage.getItem("token");
        state.isAuthenticated = true;
      } else {
        state.token = "";
        state.isAuthenticated = false;
      }
    },

    addToCart(state, item) {
      const stored = state.cart.items.filter(
        (i) => i.product.id === item.product.id
      );
      if (stored.length) {
        stored[0].quantity =
          parseInt(stored[0].quantity) + parseInt(item.quantity);
      } else {
        state.cart.items.push(item);
      }
      localStorage.setItem("cart", JSON.stringify(state.cart));
    },

    modifyCartItem(state, item) {
      const stored = state.cart.items.filter(
        (i) => i.product.id === item.product.id
      );
      stored[0].quantity = parseInt(item.quantity);
      localStorage.setItem("cart", JSON.stringify(state.cart));
    },

    removeCartItem(state, item) {
      console.log("Trying");
      state.cart.items = state.cart.items.filter(
        (i) => i.product.id !== item.product.id
      );
      localStorage.setItem("cart", JSON.stringify(state.cart));
    },

    setIsLoading(state, status) {
      state.isLoading = status;
    },

    setToken(state, token) {
      state.token = token;
      localStorage.setItem("token", state.token);
      state.isAuthenticated = true;
    },

    removeToken(state) {
      state.token = "";
      localStorage.setItem("token", state.token);
      state.isAuthenticated = false;
    },
  },
  actions: {},
  modules: {},
});
