import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import '@mdi/font/css/materialdesignicons.css'


import "vuetify/styles";
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";

const vuetify = createVuetify({
  ssr:true,
  components,
  directives,
});

createApp(App).use(vuetify).use(store).use(router).mount("#app");
