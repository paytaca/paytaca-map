<template>
  <header class="shrink-0 border-b border-soft bg-card/85 backdrop-blur">
    <div class="mx-auto flex h-16 max-w-[1500px] items-center gap-4 px-4 md:px-8">
      <router-link to="/" class="flex items-center gap-3">
        <span class="grid h-10 w-10 place-items-center rounded-2xl bg-brand-600 text-white shadow-pop text-xl">🧭</span>
        <span class="font-display text-xl font-bold text-ink leading-none">Paytaca Map</span>
      </router-link>

      <nav class="ml-1 flex items-center gap-1 md:ml-4">
        <router-link
          v-for="link in links"
          :key="link.to"
          :to="link.to"
          custom
          v-slot="{ isActive, href, navigate }"
        >
          <a
            :href="href"
            class="rounded-full px-4 py-2 text-sm font-semibold transition-colors"
            :class="isActive ? 'bg-brand-600 text-white shadow-pop' : 'text-ink-muted hover:bg-brand-50 hover:text-brand-700 dark:hover:text-brand-300'"
            @click="navigate"
          >
            {{ link.label }}
          </a>
        </router-link>
      </nav>

      <span class="ml-auto hidden text-sm text-ink-muted lg:block">
        Find merchants that accept Bitcoin Cash near you
      </span>

      <button
        type="button"
        class="ml-auto grid h-10 w-10 place-items-center rounded-full border border-soft bg-card text-ink-muted shadow-card transition-colors hover:bg-brand-50 hover:text-brand-700 lg:ml-2"
        :aria-label="dark ? 'Switch to light mode' : 'Switch to dark mode'"
        :title="dark ? 'Switch to light mode' : 'Switch to dark mode'"
        @click="toggleTheme"
      >
        <svg v-if="dark" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1.5M12 19.5V21M4.22 4.22l1.06 1.06M18.72 18.72l1.06 1.06M3 12h1.5M19.5 12H21M4.22 19.78l1.06-1.06M18.72 5.28l1.06-1.06M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" />
        </svg>
      </button>
    </div>
  </header>
</template>

<script>
export default {
  name: 'TopNav',
  data() {
    return {
      dark: false,
      links: [
        { to: '/', label: 'Map' },
        { to: '/feed', label: 'Feed' },
      ],
    }
  },
  mounted() {
    this.dark = document.documentElement.classList.contains('dark')
  },
  methods: {
    toggleTheme() {
      this.dark = !this.dark
      this.applyTheme(this.dark)
    },
    applyTheme(dark) {
      document.documentElement.classList.toggle('dark', dark)
      try {
        localStorage.setItem('theme', dark ? 'dark' : 'light')
      } catch (e) {
        void e
      }
      const meta = document.querySelector('meta[name="theme-color"]')
      if (meta) meta.setAttribute('content', dark ? '#0B1220' : '#EFF6FF')
      window.dispatchEvent(new CustomEvent('themechange', { detail: { dark } }))
    },
  },
}
</script>
