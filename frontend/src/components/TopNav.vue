<template>
  <header class="shrink-0 border-b border-soft bg-white/85 backdrop-blur">
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
            :class="isActive ? 'bg-brand-600 text-white shadow-pop' : 'text-ink-muted hover:bg-brand-50 hover:text-brand-700'"
            @click="navigate"
          >
            {{ link.label }}
          </a>
        </router-link>
      </nav>

      <span class="ml-auto hidden text-sm text-ink-muted lg:block">
        Find merchants that accept Bitcoin Cash near you
      </span>
    </div>
  </header>
</template>

<script>
export default {
  name: 'TopNav',
  data() {
    return {
      links: [
        { to: '/', label: 'Map' },
        { to: '/feed', label: 'Feed' },
      ],
    }
  },
}
</script>
