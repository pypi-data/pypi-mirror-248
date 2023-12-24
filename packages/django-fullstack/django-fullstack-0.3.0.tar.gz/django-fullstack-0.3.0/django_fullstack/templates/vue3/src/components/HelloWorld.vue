<script setup>
  import { ref } from 'vue'
  
  defineProps({
    msg: String,
  })
  
  const count = ref(0)
  </script>
  
  <template>
    <h1>{{ msg }}</h1>
  
    <div class="bg-white shadow-md rounded-md p-6 mb-4">
      <button type="button" @click="count++" class="py-2 px-4 bg-blue-500 text-white rounded-md">count is {{ count }}</button>
      <p class="text-gray-600">
        Edit
        <code>components/HelloWorld.vue</code> to test HMR
      </p>
    </div>
  
    <p>
      Check out
      <a href="https://vuejs.org/guide/quick-start.html#local" target="_blank"
        >create-vue</a
      >, the official Vue + Vite starter
    </p>
    <p>
      Install
      <a href="https://github.com/vuejs/language-tools" target="_blank">Volar</a>
      in your IDE for a better DX
    </p>
    <p class="text-gray-500">Click on the Vite and Vue logos to learn more</p>
  </template>