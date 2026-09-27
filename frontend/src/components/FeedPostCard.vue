<template>
  <a
    :href="post.link"
    target="_blank"
    rel="noopener noreferrer"
    class="group flex flex-col rounded-2xl border bg-card shadow-card transition-all duration-300 hover:-translate-y-0.5 hover:shadow-card-hover focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2"
    :class="[compact ? 'w-56 shrink-0 p-3' : 'p-5', meta.border]"
  >
    <div class="flex items-center justify-between gap-2">
      <span
        class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px] font-semibold"
        :style="{ backgroundColor: meta.chipBg, color: meta.chipText }"
      >
        <svg class="h-3.5 w-3.5" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path v-if="post.platform === 'facebook'" d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.4h-1.2c-1.2 0-1.6.8-1.6 1.5V12h2.7l-.4 2.9h-2.3v7A10 10 0 0 0 22 12z" />
          <path v-else-if="post.platform === 'tiktok'" d="M16.5 3c.3 1.9 1.6 3.4 3.5 3.7V9.2c-1.3 0-2.5-.4-3.5-1.1v5.5a5.5 5.5 0 1 1-5.5-5.5c.3 0 .6 0 .9.1v2.8c-.3-.1-.6-.2-.9-.2a2.8 2.8 0 1 0 2.8 2.8V3h2.7z" />
          <path v-else-if="post.platform === 'instagram'" d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.3 2.2.4.5.2.9.5 1.3.9.4.4.7.8.9 1.3.2.4.3 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.3 1.8-.4 2.2-.2.5-.5.9-.9 1.3-.4.4-.8.7-1.3.9-.4.2-1 .3-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.8-.3-2.2-.4-.5-.2-.9-.5-1.3-.9-.4-.4-.7-.8-.9-1.3-.2-.4-.3-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c.1-1.2.3-1.8.4-2.2.2-.5.5-.9.9-1.3.4-.4.8-.7 1.3-.9.4-.2 1-.3 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 1.8c-3.1 0-3.5 0-4.7.1-.9 0-1.4.2-1.7.3-.4.2-.7.3-1 .6-.3.3-.5.6-.6 1-.1.3-.3.8-.3 1.7-.1 1.2-.1 1.6-.1 4.7s0 3.5.1 4.7c0 .9.2 1.4.3 1.7.2.4.3.7.6 1 .3.3.6.5 1 .6.3.1.8.3 1.7.3 1.2.1 1.6.1 4.7.1s3.5 0 4.7-.1c.9 0 1.4-.2 1.7-.3.4-.2.7-.3 1-.6.3-.3.5-.6.6-1 .1-.3.3-.8.3-1.7.1-1.2.1-1.6.1-4.7s0-3.5-.1-4.7c0-.9-.2-1.4-.3-1.7-.2-.4-.3-.7-.6-1-.3-.3-.6-.5-1-.6-.3-.1-.8-.3-1.7-.3-1.2-.1-1.6-.1-4.7-.1zm0 3.1a4.9 4.9 0 1 1 0 9.8 4.9 4.9 0 0 1 0-9.8zm0 1.8a3.1 3.1 0 1 0 0 6.2 3.1 3.1 0 0 0 0-6.2zm5.1-2a1.1 1.1 0 1 1 0 2.3 1.1 1.1 0 0 1 0-2.3z" />
          <path v-else d="M18.9 2H22l-7.3 8.3L23 22h-6.8l-5.3-6.9L4.8 22H1.6l7.8-8.9L1 2h7l4.8 6.3L18.9 2zm-2.4 18h1.9L7.6 4H5.6l10.9 16z" />
        </svg>
        {{ meta.label }}
      </span>
      <span v-if="post.posted_at" class="text-[11px] font-medium text-ink-faint">{{ relativeTime }}</span>
    </div>

    <p
      class="mt-3 text-sm leading-relaxed text-ink-muted"
      :class="compact ? 'line-clamp-2' : 'line-clamp-4'"
    >
      {{ post.description || 'A Paytaca merchant moment shared online.' }}
    </p>

    <div v-if="!compact && post.merchants && post.merchants.length" class="mt-3 flex flex-wrap gap-1.5">
      <span
        v-for="merchant in post.merchants"
        :key="merchant.id"
        class="inline-flex items-center rounded-full bg-brand-50 px-2.5 py-0.5 text-[11px] font-medium text-brand-700 dark:text-brand-300"
      >
        {{ merchant.name }}
      </span>
    </div>

    <span
      class="mt-auto pt-3 inline-flex items-center gap-1 text-xs font-semibold"
      :class="compact ? 'mt-2 pt-2' : ''"
      :style="{ color: meta.accent }"
    >
      View post
      <svg class="h-3 w-3 transition-transform duration-200 group-hover:translate-x-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M7 17 17 7M7 7h10v10" />
      </svg>
    </span>
  </a>
</template>

<script>
import moment from 'moment'

const PLATFORM_META = {
  facebook: { label: 'Facebook', accent: '#1877F2', chipBg: '#E7F0FE', chipText: '#1257B8', border: 'border-[#CFE0FB]' },
  tiktok: { label: 'TikTok', accent: '#111827', chipBg: '#EAEAEA', chipText: '#111827', border: 'border-[#DCDCDC]' },
  instagram: { label: 'Instagram', accent: '#DD2A7B', chipBg: '#FCE7F1', chipText: '#B0176A', border: 'border-[#F6CFE2]' },
  x: { label: 'X', accent: '#14171A', chipBg: '#E9EAEB', chipText: '#14171A', border: 'border-[#DBDDDE]' },
}

const DEFAULT_META = { label: 'Post', accent: '#0AA76C', chipBg: '#E7FBF1', chipText: '#088455', border: 'border-soft' }

export default {
  name: 'FeedPostCard',
  props: {
    post: {
      type: Object,
      required: true,
    },
    compact: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    meta() {
      return PLATFORM_META[this.post.platform] || DEFAULT_META
    },
    relativeTime() {
      if (!this.post.posted_at) {
        return ''
      }
      return moment(this.post.posted_at).fromNow()
    },
  },
}
</script>
