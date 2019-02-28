import "@babel/polyfill";
import Vue from "vue";
import "./plugins/axios";
import "./plugins/bootstrap-vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "./plugins/element.js";

Vue.config.productionTip = false;

// router.beforeResolve((to, from, next) => {
//   // to and from are both route objects. must call `next`.
//   if ("development" != process.env.NODE_ENV){
//     // to.path = "/clinical" + to.path;
//   }
//   // console.log(process.env.NODE_ENV);
//   // console.log(`Route: from:${from}\tto:${to}`);
//   // console.log(from);
//   // console.log(to);
//   next();
// })

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
