import {createApp} from 'vue'
import App from '@/App.vue'
import '@/index.css'
import {setDefaultOptions} from "date-fns"
import {vi} from "date-fns/locale"

setDefaultOptions({locale: vi})
const app = createApp(App)
app.mount('#app')
