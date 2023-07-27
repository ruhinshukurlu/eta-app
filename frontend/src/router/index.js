import {createRouter, createWebHistory} from "vue-router";
import HomeView from "../views/HomeView.vue";
import ActiveETAsView from "../views/ActiveETAsView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomeView,
    meta: {requiresAuth: true}
  },
  {
    path: "/active-etas",
    name: "activeEtas",
    component: ActiveETAsView,
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
    meta: {requiresGuest: true}
  },
  {
    path: "/register",
    name: "register",
    component: RegisterView,
    meta: {requiresGuest: true}
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach(async (to) => {
  const token = localStorage.getItem("token");
  // midlware to prevent user to see home page without login
  if (to.meta.requiresAuth && !token) {
    return {name: "login"};
  }

  // after login user can't see login page
  if (to.meta.requiresGuest && token) {
    return {name: "Home"};
  }
});


export default router;
