<template>
  <div class="h-full overflow-y-auto bg-cloud">
    <div class="mx-auto max-w-2xl px-6 py-16 text-center">
      <span class="mx-auto grid h-16 w-16 place-items-center rounded-3xl bg-brand-100 text-3xl shadow-card">📸</span>
      <h1 class="mt-6 font-display text-3xl font-bold text-ink">Feed</h1>
      <p class="mt-3 inline-flex items-center rounded-full border border-mango-300 bg-mango-100 px-4 py-1.5 text-xs font-semibold uppercase tracking-wide text-mango-700 dark:text-mango-300">
        Coming Soon
      </p>
      <p class="mt-3 text-ink-muted">
        A feed of posts from people spending Bitcoin Cash at these merchants is on the way.
      </p>
      <router-link
        to="/"
        class="mt-8 inline-flex items-center rounded-full bg-brand-600 px-5 py-2.5 text-sm font-semibold text-white shadow-pop hover:bg-brand-700"
      >
        Explore the map
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FeedView',
}
</script>
