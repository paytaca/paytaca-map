<template>
  <div class="flex h-screen flex-col overflow-hidden bg-cloud supports-[height:100dvh]:h-dvh">
    <TopNav />
    <main class="min-h-0 flex-1">
      <router-view />
    </main>
  </div>
</template>

<script>
import TopNav from './components/TopNav.vue'

export default {
  name: 'App',
  components: { TopNav },
}
</script>
