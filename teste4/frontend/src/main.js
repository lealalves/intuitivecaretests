import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'

import Pagination from 'v-pagination-3';

const app = createApp(App)
// eslint-disable-next-line vue/multi-word-component-names
app.component('pagination', Pagination);


app.mount('#app')

