import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    // {
    //   path: "/",
    //   name: "home",
    //   component: Home
    // },
    {
      path: "/",
      name: "index",
      component: () =>
        import(/* webpackChunkName: "index" */ "./views/Index.vue")
    },
    {
      path: "/template",
      name: "template",
      component: () =>
        import(/* webpackChunkName: "template" */ "./views/Template.vue")
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/About.vue")
    },
    {
      path: "/adddata",
      name: "adddata",
      component: () =>
        import(/* webpackChunkName: "adddata" */ "./views/Adddata.vue")
    },
    {
      path: "/detail",
      name: "detail",
      component: () =>
        import(/* webpackChunkName: "detail" */ "./views/Showdata.vue")
    }
  ]
});
