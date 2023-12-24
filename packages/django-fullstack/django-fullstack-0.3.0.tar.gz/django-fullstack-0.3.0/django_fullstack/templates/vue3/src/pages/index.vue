<template>
  <div>
    <a href="https://vitejs.dev" target="_blank">
      <img :src="viteLogo" class="h-24 p-6 transition duration-300 will-change filter hover:drop-shadow(0 0 2em #646cffaa)" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img :src="vueLogo" class="logo h-24 p-6 transition duration-300 will-change filter hover:drop-shadow(0 0 2em #42b883aa)" alt="Vue logo" />
    </a>
  </div>
  <HelloWorld :msg="msg" />
</template>

<script setup lang="ts">
import HelloWorld from './components/HelloWorld.vue';

const viteLogo: string = "/vite.svg";
const vueLogo: string = "./assets/vue.svg";
const msg: string = "Vite + Vue";
</script>
