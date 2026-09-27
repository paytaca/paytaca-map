<template>
  <div class="h-full overflow-y-auto bg-cloud">
    <div class="mx-auto max-w-6xl px-6 py-10 sm:py-14">
      <header class="text-center sm:text-left">
        <span class="inline-flex items-center gap-2 rounded-full bg-brand-100 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-brand-700">
          Community
        </span>
        <h1 class="mt-4 font-display text-3xl font-bold text-ink sm:text-4xl">Paying with BCH, in the wild</h1>
        <p class="mt-3 max-w-2xl text-ink-muted">
          Real posts from people spending Bitcoin Cash through Paytaca at partner merchants.
        </p>
      </header>

      <div v-if="isLoading" class="mt-10 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <div v-for="n in 6" :key="n" class="animate-pulse rounded-2xl border border-soft bg-card p-5">
          <div class="flex items-center justify-between">
            <div class="h-6 w-24 rounded-full bg-cloud-deep"></div>
            <div class="h-4 w-16 rounded-full bg-cloud-deep"></div>
          </div>
          <div class="mt-4 space-y-2">
            <div class="h-4 w-full rounded-full bg-cloud-deep"></div>
            <div class="h-4 w-5/6 rounded-full bg-cloud-deep"></div>
            <div class="h-4 w-2/3 rounded-full bg-cloud-deep"></div>
          </div>
        </div>
      </div>

      <div v-else-if="error" class="mt-10 rounded-2xl border border-soft bg-card p-10 text-center shadow-card">
        <span class="mx-auto grid h-14 w-14 place-items-center rounded-2xl bg-coral-100 text-2xl">⚠️</span>
        <p class="mt-4 font-semibold text-ink">We couldn't load the feed.</p>
        <p class="mt-1 text-sm text-ink-muted">Please try again in a moment.</p>
        <button
          type="button"
          class="mt-6 inline-flex items-center rounded-full bg-brand-600 px-5 py-2.5 text-sm font-semibold text-white shadow-pop hover:bg-brand-700"
          @click="fetchFeedPosts"
        >
          Retry
        </button>
      </div>

      <div v-else-if="!posts.length" class="mt-10 rounded-2xl border border-soft bg-card p-10 text-center shadow-card">
        <span class="mx-auto grid h-14 w-14 place-items-center rounded-2xl bg-brand-100 text-2xl">📸</span>
        <p class="mt-4 font-semibold text-ink">No posts yet.</p>
        <p class="mt-1 text-sm text-ink-muted">Check back soon — merchants are sharing their BCH moments.</p>
        <router-link
          to="/"
          class="mt-6 inline-flex items-center rounded-full bg-brand-600 px-5 py-2.5 text-sm font-semibold text-white shadow-pop hover:bg-brand-700"
        >
          Explore the map
        </router-link>
      </div>

      <div v-else class="mt-10 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <FeedPostCard v-for="post in posts" :key="post.id" :post="post" />
      </div>
    </div>
  </div>
</template>

<script>
import FeedPostCard from '../components/FeedPostCard.vue'

const DOMAIN = 'https://map.paytaca.com'

export default {
  name: 'FeedView',
  components: {
    FeedPostCard,
  },
  data() {
    return {
      posts: [],
      isLoading: false,
      error: false,
    }
  },
  mounted() {
    this.fetchFeedPosts()
  },
  methods: {
    async fetchFeedPosts() {
      this.isLoading = true
      this.error = false
      try {
        const response = await fetch(`${DOMAIN}/api/feed/`)
        if (!response.ok) {
          throw new Error(`Request failed with status ${response.status}`)
        }
        const data = await response.json()
        const list = Array.isArray(data) ? data : data.results || []
        this.posts = list
      } catch (err) {
        this.error = true
        this.posts = []
      } finally {
        this.isLoading = false
      }
    },
  },
}
</script>
