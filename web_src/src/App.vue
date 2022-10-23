<template>
  <h1>Hello from VueJS</h1>
  <h1>Hello from FastAPI: {{ serverResponse }}</h1>
</template>

<script lang="ts" setup>
import {ref} from "vue"
import axios from "axios"

const serverResponse = ref("");

axios.get("/api/hello").then((response) => {
  serverResponse.value = response.data;
});

axios.get("/api/openapi.json").then((response) => {
  window.document.title = response.data.info.title;
  localStorage.setItem("title", response.data.info.title);
});
</script>
